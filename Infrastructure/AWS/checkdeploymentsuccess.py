import json
import os
import time

status = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
status = json.loads(status)
initial_version = status['deployments'][0]['version']
initial_state = status['deployments'][0]['state']
print("\n###   Start   ###")
print("Current version:")
print(initial_version)
print(initial_state)

attempts = 100
print("\nStarting in 60 seconds - to give the CI time to send the container to AWS")
time.sleep(60)

print("\n###   Starting   ###")
while True:
    print("\nAttempt: #" + str(100 - attempts))
    x = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
    x = json.loads(x)
    
    new_version = x['deployments'][0]['version']
    new_state = x['deployments'][0]['state']
    print("   Looking for a version higher than: " + str(initial_version -1))
    print("   Current version: " +str(new_version))
    print("   Looking for a status: ACTIVE")
    print("   Current status: "+ str(new_state))
    if new_version >= initial_version and new_state == 'ACTIVE':
        print("\n###   DONE   ###")
        print("New version live and active. ")
        exit(0)
    else:
        attempts = attempts - 1
        print("\nResult -- Not yet ready")
        print("Trying again in 10 seconds." + "remaining attempts: " + str(attempts))
        
    if attempts == 0:
        print("\n###   ERROR   ###")
        print("No new version found -- No more attempts")
        exit(1)
    time.sleep(10)
        