import json
import csv

unresolved = ["No ratings or reviews found", "Multiple candidates discovered", "no location found"]

def main():
    with open('station_reviews_analysed.json', 'r+') as infile:
        station_reviews = json.load(infile)

    with open('railmap.csv', newline='') as csvfile:
        filereader = list(csv.reader(csvfile, delimiter=','))
        headers = [header.replace('\ufeff', '') for header in filereader[0]]
        stations = [dict(zip(headers,row)) for row in filereader[1:]]

    for station in stations:
        if station_reviews[station['name']] in unresolved:
            print('{} is unresolved'.format(station['name']))
            continue
        station_rating = station_reviews[station['name']]['rating']
        station_polarity = station_reviews[station['name']]['avg_polarity']
        station_subjectivity = station_reviews[station['name']]['avg_subjectivity']

        station.update({'rating':station_rating, 'polarity':station_polarity, 'subjectivity':station_subjectivity})


        with open('station_data.csv', 'a', newline='') as csvOut:
            filewriter = csv.DictWriter(csvOut, station.keys())
            filewriter.writerow(station)


if __name__ == '__main__':
    main()
