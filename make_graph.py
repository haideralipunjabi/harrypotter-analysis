import json
import os
import numpy as np
import matplotlib.pyplot as plt
import copy
ficdata = json.load(open("ficdata.json","r"))
bookdata = json.load(open("bookdata.json","r"))

ficscount=250
bookscount=7

category_names = ['Fanfiction', 'Books']

def generate_data():
    data = {}
    for key in list(ficdata.keys())[:20]:
        word_data = [ficdata[key]/ficscount,0]
        if key in bookdata.keys():
            word_data[1] = (bookdata[key]/bookscount)
        data[key] = word_data
        
    ## Graph 2
    # for key in list(bookdata.keys()):
    #     if len(data.keys()) >= 40:
    #         break
    #     if key not in data.keys():
    #         word_data = [0,bookdata[key]/bookscount]
    #         if key in ficdata.keys():
    #             word_data[0] = (ficdata[key]/ficscount)
    #         data[key] = word_data
    
    return data

def normalize_data(data):
    for key in data.keys():
        total = data[key][0] + data[key][1]
        data[key][0] = data[key][0]*100/total
        data[key][1] = data[key][1]*100/total
    return data


def survey(results, category_names, ann):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(16,16))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.8,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            if(c < 5):
                x -= 5
            ax.text(x, y, round(ann[y][i],3), ha='center', va='center',
                    color=text_color,fontsize=18)
        ax.yaxis.set_tick_params(labelsize=20)

    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize=25)
    fig.savefig("out/graph2.eps",format="eps")
    fig.savefig("out/graph2.png",format="png")





data = generate_data()

## For Graph2
# for k in list(ficdata.keys())[:20]:
#     print(k)
#     del data[k]

norm_data = normalize_data(copy.deepcopy(data))
survey(norm_data,category_names,list(data.values()))
