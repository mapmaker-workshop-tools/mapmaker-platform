import json
import os
import time

status = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
status = json.loads(status)
initial_version = status['deployments'][0]['version']
initial_state = status['deployments'][0]['state']

print(initial_version)
print(initial_state)

old_version_detected = True
attempts = 10

while old_version_detected:
    print("sleeping 60 seconds")
    time.sleep(60)
    x = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
    x = json.loads(x)
    new_version = x['deployments'][0]['version']
    new_state = status['deployments'][0]['state']
    if new_version > old_version_detected and new_state == 'ACTIVE':
        print("New version Detected")
        exit(0)
    else:
        attempts = attempts - 1
        print("Attempted 1 time")
    if attempts == 0:
        print("No new version found")
        exit(1)
    
        