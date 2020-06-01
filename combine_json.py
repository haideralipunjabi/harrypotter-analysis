import json
import os

data = {}
count = 0
directory = "bookdata"
for f in os.listdir(directory):
    file = open(directory+"/"+f,"r")
    try:
        d = json.load(file)
    except json.JSONDecodeError:
        print("Error: "+ f)
        break
    for key in d:
        if key in data:
            data[key] += d[key]
        else:
            data[key] = d[key]
    count += 1
    print(f"Done: {count}/{len(os.listdir(directory))}")

data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1],reverse=True)}
json.dump(data,open(directory+".json","w"))