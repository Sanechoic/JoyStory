# Language Processing
import nltk
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

import json

unresolved = ["No ratings or reviews found", "Multiple candidates discovered", "no location found"]
def analyse_review(review):
    analysis = TextBlob(review)
    return(analysis.sentiment.polarity, analysis.sentiment.subjectivity)

def main(review_file):
    j = 0
    with open('station_reviews.json', 'r+') as infile:
        station_reviews = json.load(infile)

    for i, station in enumerate(station_reviews.keys()):
        if i < 0:
            continue
        if station_reviews[station] in unresolved:
            print('{} is unresolved'.format(station))
            continue
        for review in station_reviews[station]['reviews']:
            j = j+1
            if not review['text']:
                continue
            pol, sub = analyse_review(review['text'])
            review.update({'polarity':pol,'subjectivity':sub})

        print(j)

        polarities = [review['polarity'] for review in station_reviews[station]['reviews'] if review['text']]
        subjectivities = [review['subjectivity'] for review in station_reviews[station]['reviews'] if review['text']]

        if polarities and subjectivities:
            avg_polarity = round(sum(polarities)/len(polarities),2)
            avg_subjectivity = round(sum(subjectivities)/len(subjectivities),2)
        else:
            avg_polarity = 'no reviews'
            avg_subjectivity = 'no reviews'

        station_reviews[station].update({'avg_polarity':avg_polarity,'avg_subjectivity':avg_subjectivity})

        print('{} - {} : rating: {}, polarity: {}, subjectivity: {}'.format(i, station, station_reviews[station]['rating'], avg_polarity, avg_subjectivity))

        with open('station_reviews.json', 'w+') as outfile:
            json.dump(station_reviews, outfile)

    return

if __name__ == '__main__':
    main('station_reviews.json')
