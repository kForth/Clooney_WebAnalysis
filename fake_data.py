import json
import random

import requests

if __name__ == "__main__":
    event_key = '2017onham'
    db = json.load(open('db/db.json'))
    sheet = list(db['sheets']['sheets'][1]["data"])
    matches = db['events'][event_key]['matches']

    for match in matches:
        for alliance in sorted(match['alliances'].keys()):
            for team in match['alliances'][alliance]['team_keys']:
                team = team[3:]
                data = {
                    'team': int(team),
                    'match': match['match_number'],
                    'pos': match['alliances'][alliance]['team_keys'].index('frc' + team) + (3 if alliance == 'blue' else 0)
                }
                print(team)
                for field in sheet:
                    if field['type'] == 'HorizontalOptions':
                        value = random.choice(field['options'].split(" "))
                    elif field['type'] == 'Numbers':
                        max = field['ones'] + 10 * field['tens']
                        value = random.randint(0, max)
                    elif field['type'] == 'Boolean':
                        value = True if random.randint(0, 1) == 1 else False
                    else:
                        continue
                    data[field['key']] = value
                payload = {
                    'event': event_key,
                    'data': data,
                    'filename': 'sheet_1.jpg'
                }
                resp = requests.post('http://0.0.0.0:5002/add/entry', json=payload)
                print(resp)
