import json
import os
import time

status = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
status = json.loads(status)
initial_version = status['deployments'][0]['version']
initial_state = status['deployments'][0]['state']

print("Current version detected:")
print(initial_version)
print(initial_state)

old_version_detected = True
attempts = 1000

while old_version_detected:
    print("\nChecking again in 10 seconds -- attempt: " + str(attempts))
    time.sleep(10)
    x = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
    x = json.loads(x)
    
    print("\nChecking for status. \nDetected:")
    new_version = x['deployments'][0]['version']
    new_state = status['deployments'][0]['state']
    print(new_version)
    print(new_state)
    if new_version >= initial_version and new_state == 'ACTIVE':
        print("New version live and active. Exiting. ")
        exit(0)
    else:
        attempts = attempts - 1
        print("No new version found, trying again.")
        print("remaining attempts: " + str(attempts))
        
    if attempts == 0:
        print("No new version found")
        exit(1)
    
        