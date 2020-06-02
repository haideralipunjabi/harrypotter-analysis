import os
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import json

# mask = np.array(Image.open("masks/book7.png"))
data = json.load(open("extra/genre.json","r"))

# print(f"Diffrent Words: {len(data.keys())} | Total Words: {sum(data.values())}")
wc = WordCloud(width=512,height=512,background_color="white", max_words=2000,
               max_font_size=40, random_state=42,contour_width=1)

wc.generate_from_frequencies(data)
s = wc.to_svg()
print(s,file=open("out/genre.svg","w"))


