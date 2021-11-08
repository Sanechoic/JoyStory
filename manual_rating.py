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

def main():
    place = 'Clapham Junction'

    r = dict(find_place(place).json())
    #print(r)

    # Get Rating and review
    place_id = r['candidates'][0]['place_id']
    place_details = find_place_details(place_id).json()
    #print(place_details)
    place_details = dict(place_details)



    place_obj = {place:
                    {
                    'rating':place_details['result']['rating'],
                    'reviews':[{'rating':review['rating'],'text':review['text'],'time':review['time']} for review in place_details['result']['reviews']]
                    }
                }


    print(json.dumps(place_obj))

    return

if __name__ == '__main__':
    main()
