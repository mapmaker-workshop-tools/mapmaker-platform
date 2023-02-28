import json
import os
import time

status = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
status = json.loads(status)
initial_version = status['deployments'][0]['version']
initial_state = status['deployments'][0]['state']
print("\n###   Start   ###")
print("Current version detected:")
print(initial_version)
print(initial_state)

attempts = 100
print("\nStarting in 60 seconds")
time.sleep(60)

print("\n###   Starting   ###")
while True:
    print("\nNew attempt: #" + str(100 - attempts))
    x = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
    x = json.loads(x)
    
    print("\nIn this attempt we checked detecte: \n")
    new_version = x['deployments'][0]['version']
    new_state = x['deployments'][0]['state']
    print(new_version)
    print(new_state)
    if new_version >= initial_version and new_state == 'ACTIVE':
        print("\n###   DONE   ###")
        print("New version live and active. ")
        exit(0)
    else:
        attempts = attempts - 1
        print("\nNo new version detected or not yet active")
        print("Trying again in 10 seconds.")
        print("remaining attempts: " + str(attempts))
        
    if attempts == 0:
        print("\n###   ERROR   ###")
        print("No new version found -- No more attempts")
        exit(1)
    time.sleep(10)
        