import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import json
import multiprocessing as mp

source_directory = "books"
data_directory = "bookdata"

source_files = [f.split(".")[0] for f in os.listdir(source_directory)]
done_files = [f.split(".")[0] for f in os.listdir(data_directory)]
files = []
gfile = open("custom_stopwords.txt","r")

to_remove = [l.strip() for l in gfile.readlines()]
stopwords = stopwords.words('english')
stopwords.extend(to_remove)

# Creating a list of already done files in case the process gets interrupted
for file in source_files:
    if file not in done_files:
        files.append(file)
file_count = len(files)

def process(i):
    data = {}
    file = open(f"{source_directory}/{files[i]}.txt","r")
    print(f"Starting {i}: {files[i]}")
    text = file.read()
    tokens = word_tokenize(text)
    ## Not doing text.lower() to maintain the case of the words
    for word in tokens:
        if word not in stopwords and word.isalpha() and word.title() not in stopwords and word.lower() not in stopwords:   
            if word in data.keys():
                data[word] += 1
            else:
                data[word] = 1

    print(f"Done {i}/{file_count}")
    data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1],reverse=True)}
    json.dump(data,open(f"{data_directory}/{files[i]}.json","w"))

pool = mp.Pool(mp.cpu_count())
results = [pool.map(process,range(file_count))]
pool.close()

