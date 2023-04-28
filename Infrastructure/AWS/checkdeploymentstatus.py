import json
import os
import time

attempts = 250


print("\n###   Checking if server is ready to deploy a new version   ###")
while True:
    print("\nAttempt: #" + str(251 - attempts))
    x = os.popen("aws lightsail get-container-service-deployments --service-name mapmaker --output json").read()
    x = json.loads(x)

    new_version = x['deployments'][0]['version']
    new_state = x['deployments'][0]['state']
    timestamp = x['deployments'][0]['createdAt']
    print("   Current status: "+ str(new_state))
    if new_state == 'ACTIVE':
        print("\n###   Ready to deploy a new version ###")
        exit(0)
    else:
        attempts = attempts - 1
        print("\nResult:")
        print("    Server is not ready yet")
        print("    Remaining attempts: " + str(attempts))
        print("    Trying again in 10 seconds.")

    if attempts == 0:
        print("\n###   ERROR   ###")
        print("No new version found -- No more attempts")
        exit(1)
    time.sleep(10)
