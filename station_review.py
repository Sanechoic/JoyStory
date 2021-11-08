import json
import requests
from googleAPI import Credentials, Places
import re
import csv

'''
Construct the dataset of all the uk stations + google reviews
Refer to url for more info on Google maps places API:
"https://developers.google.com/places/web-service/search"
'''
def station_query(station, disambig_re):
    if re.search(disambig_re, station):
        query_parts = re.split(disambig_re, station)
        query = query_parts[0]+' railway station '+query_parts[1]
    else:
        query = station+' railway station'

    return query


def find_place(input, parameters=None, uri='https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'):
    params = {
                'key':Credentials.places_api_key,
                'input':input,
                'inputtype':'textquery',
                }

    if parameters:
        params.update(parameters)


    url = uri+'&'.join([k+'='+v for k, v in params.items()])

    return requests.get(url)

def find_place_details(place_id, parameters=None, uri='https://maps.googleapis.com/maps/api/place/details/json?'):
    params = {
                'key':Credentials.places_api_key,
                'place_id':place_id,
                'fields':'rating,reviews'
                }

    if parameters:
        params.update(parameters)

    url = uri+'&'.join([k+'='+v for k, v in params.items()])

    return requests.get(url)

def main(csv_path):
    not_found = {}
    disambig_re = re.compile('(\(\w+\))')

    with open(csv_path, newline='') as csvfile:
        filereader = list(csv.reader(csvfile, delimiter=','))
        headers = [header.replace('\ufeff', '') for header in filereader[0]]
        stations = [dict(zip(headers,row)) for row in filereader[1:]]

    for i, station in enumerate(stations):
        with open('station_reviews.json', 'r+') as infile:
            station_reviews = json.load(infile)

        place = station_query(station['name'], disambig_re)

        print(i, place)

        r = dict(find_place(place).json())
        # Check if anything returned
        if not r['candidates']:
            print('No location found')
            place_obj = {station['name']:'no location found'}
            not_found.update(place_obj)
        else:
            #print(r['candidates'])
            # if there is more than one candidate
            if len(r['candidates']) != 1:
                print('Multiple candidates discovered, please retry with more parameters')
                place_obj = {station['name']:'Multiple candidates discovered'}
                not_found.update(place_obj)
            else:

                # Get Rating and review
                place_id = r['candidates'][0]['place_id']
                place_details = find_place_details(place_id).json()
                Places.store_results(place_details, station['name'])
                place_details = dict(place_details)
                if place_details['result']:
                    place_obj = {station['name']:
                                    {
                                    'rating':place_details['result']['rating'],
                                    'reviews':[{'rating':review['rating'],'text':review['text'],'time':review['time']} for review in place_details['result']['reviews']]
                                    }
                                }
                else:
                    place_obj = {station['name']:'No ratings or reviews found'}
                    not_found.update(place_obj)

        station_reviews.update(place_obj)

        print(len(station_reviews))

        with open('station_reviews.json', 'w+') as outfile:
            json.dump(station_reviews, outfile)

        #print('place stored')

    with open('unresolved_station_reviews.json', 'w+') as outfile:
        json.dump(not_found, outfile)

    return

if __name__ == '__main__':
    main('railmap.csv')
