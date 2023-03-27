import requests
import sys
from datetime import datetime

change = sys.argv
time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
authkey = "Basic Z2l0aHViLjRiYWE1Ni5tcC1zZXJ2aWNlLWFjY291bnQ6N1VyZ2tmZmNYaEJMZGN2SVVYeEtYMmF4VFZuWEYxclY="
description = str(change[1]) +" "+ str(change[2])

url = "https://eu.mixpanel.com/api/app/projects/2949603/annotations"

payload = {
    "date": time,
    "description": description ,
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authkey
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
