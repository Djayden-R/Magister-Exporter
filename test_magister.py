import requests
import json
from datetime import datetime

with open('credentials.json', 'r') as json_file:
    credentials_json = json.load(json_file)

for login in credentials_json['logins']:
    headers = {
        "Authorization": login['bearer_token'],
        "content-type": "application/json"
    }

    url = f"https://middelharnis.magister.net/api/personen/{login['user_id']}/afspraken?status=1&tot=2026-03-07&van=2026-02-26"

    r = requests.get(url, headers=headers)

    rooster = json.loads(r.text)
    lessen = rooster['Items']

    prev_day = None

    for les in lessen:
        date_str = les["Start"]
        date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        day = date.strftime("%A (%d/%m)")

        if day != prev_day:
            print(day)
            prev_day = day

        print(f"{les['LesuurVan']}e uur - {les['Omschrijving']} {les['Lokatie']}")