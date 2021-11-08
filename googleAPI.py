from datetime import datetime
import json

class Credentials:
  places_api_key = "AIzaSyButjbROrYLfJGlq7tKBtRyCSwmvB6eZK4"


class Places:
    def store_results(json_input, q, format='%Y%m%d%H%M%S'):
        filepath = 'logs/'+datetime.strftime(datetime.now(), format)+'-'+q.lower().replace(' ','_')+'.json'
        with open(filepath, 'w+') as outfile:
            json.dump(json_input, outfile)
        return filepath
