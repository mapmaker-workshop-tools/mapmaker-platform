import requests
import sys
from datetime import datetime

change = sys.argv
time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
print(time)
authkey = change[3]
description = str(change[1]) + str(change[2])

url = "https://eu.mixpanel.com/api/app/projects/2949603/annotations"

payload = {
    "date": "2022-02-15 12:00:00",
    "description": description 
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authkey
}

response = requests.post(url, json=payload, headers=headers)
print(response)
