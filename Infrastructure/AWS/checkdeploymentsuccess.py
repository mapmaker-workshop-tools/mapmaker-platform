import json
import os
import time
import requests

status = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
status = json.loads(status)
initial_version = status['deployments'][0]['version']
initial_state = status['deployments'][0]['state']
print("\n###   Start   ###")
print("Current version:")
print(initial_version)
print(initial_state)

attempts = 250


print("\n###   Starting   ###")
while True:
    print("\nAttempt: #" + str(251 - attempts))
    x = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
    x = json.loads(x)
    
    new_version = x['deployments'][0]['version']
    new_state = x['deployments'][0]['state']
    timestamp = x['deployments'][0]['createdAt']
    print("   Looking for a version higher than: " + str(initial_version))
    print("   Current version: " +str(new_version))
    print("   Looking for a status: ACTIVE")
    print("   Current status: "+ str(new_state))
    if new_version > initial_version and new_state == 'ACTIVE':
        print("\n###   New Version found   ###")
        print("New version live and active. ")
        print("Validating if Django is running...")
        url = 'https://mapmaker.vdotvo9a4e2a6.eu-central-1.cs.amazonlightsail.com/api/v1/'
        response = requests.get(url)
        if response.status_code == 200:
            print("Django server confirmed running")
            print("DONE")
            exit(0)
        else:
            print("New version deployed but there's an error with Django")
            exit(0)
    else:
        attempts = attempts - 1
        print("\nResult:")
        print("    Not yet ready")
        print("    Remaining attempts: " + str(attempts))
        print("    Trying again in 10 seconds.")
        
    if attempts == 0:
        print("\n###   ERROR   ###")
        print("No new version found -- No more attempts")
        exit(1)
    time.sleep(10)
    