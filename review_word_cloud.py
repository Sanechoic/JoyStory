from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk import sent_tokenize, word_tokenize
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
import re
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import csv
from PIL import Image
import numpy as np
from os import path
import os
import ssl



unresolved = ["No ratings or reviews found", "Multiple candidates discovered", "no location found"]

rail_words = ['train','trains','railway','station','platform','platforms','london','stations']

common_words = ['thank','well','know','though','around','get','one','place','need','take','really','look','even','lot','always','going','use','much','got','getting','two','many','least','quite','especially','see','still','never','although','say','want','needs','back','way','next','side', 'good','great','nice','day']

def wc(data,bgcolor,title, mask_path):
    print(f'generating word cloud')
    plt.figure(figsize = (12,12))

    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    img_mask = np.array(Image.open(path.join(d, mask_path)))
    image_colours = ImageColorGenerator(img_mask)

    font_path = "proximanova-regular.otf"

    wc = WordCloud(background_color = bgcolor, max_words = 1000, mask=img_mask, color_func=image_colours, font_path=font_path)

    words = ' '.join(data)
    wc.generate(words)

    # create coloring from image
    wc.to_file(path.join(d, 'word_cloud.png'))


    plt.imshow(wc)
    plt.axis('off')
    plt.show()


def word_bag(review_text, stop_words, punc_re):
    r = review_text.lower()
    r = re.sub(punc_re, ' ', r)

    word_tokens = word_tokenize(r)
    r = [w for w in word_tokens if not w in stop_words]
    r = [word for word in r if len(word) > 2]
    r = [word for word in r if not word.isnumeric()]
    #print(r)
    return r

def word_dist(wb):
    word_dist = nltk.FreqDist(wb)
    rslt = pd.DataFrame(word_dist.most_common(100),
                    columns=['Word', 'Frequency'])

    plt.figure(figsize=(10,10))
    sns.set_style("whitegrid")
    ax = sns.barplot(x="Word",y="Frequency", data=rslt.head(7))
    #plt.show()

def main(review_file):
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('stopwords')
    nltk.download('punkt')
    #print(stopwords.words('english'))

    stop_words = list(get_stop_words('en'))
    nltk_words = list(stopwords.words('english'))
    stop_words.extend(nltk_words)
    stop_words.extend(rail_words)
    stop_words.extend(common_words)

    punc_re = re.compile('[^A-Za-z]+')

    with open('station_reviews_analysed.json', 'r+') as infile:
        station_reviews = json.load(infile)

    stations = {}
    with open('railmap.csv', newline='') as csvfile:
        filereader = list(csv.reader(csvfile, delimiter=','))
        headers = [header.replace('\ufeff', '') for header in filereader[0]]
        #stations = [dict(zip(headers,row)) for row in filereader[1:]]
        for row in filereader[1:]:
            stations.update({row[1]:dict(zip(headers,row))})

    wb = []
    r_num = 0
    r_count = 0
    u = 0
    nnr = 0
    print(f'processing reviews')
    for i, station in enumerate(station_reviews.keys()):
        if station_reviews[station] in unresolved:
            u += 1
            continue
        '''
        if stations[station]['owner'] != 'Network Rail':
            nnr += 1
            continue
        '''
        for review in station_reviews[station]['reviews']:
            r_count+=1
            #print(f'processing review: {r_count}')
            if not review['text']:
                continue

            r_num+=1
            r = word_bag(review['text'], stop_words, punc_re)
            if r:
                #print(r)
                wb.extend(r)
    #print(wb)

    #word_dist(wb)
    wc(wb, 'white', 'Rail Review', 'mask_colour_small.png')


if __name__ == '__main__':
    main('station_reviews_analysed.json')
