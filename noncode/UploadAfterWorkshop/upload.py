
from zipfile import ZipFile
import requests
import os
from time import sleep

print("\n\n\n###### UPLOADING ARCHIVE TO MAPMAKER ######")
print("Preparing first image - hang in tight...")

def send_to_mapmaker(image):
    url = "http://127.0.0.1:8000/api/v1/importcards/3/"
    payload={}
    files=[
    ('file',(image ,open(image,'rb'),'image/png'))
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print("Response from server:")
    print(response.text)


with ZipFile("Archief.zip", 'r') as zObject:
    zObject.extractall(path='temp')

length = len(zObject.namelist())


directory = 'temp'

of_total = 100 / length
i = 0 
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        send_to_mapmaker(f)
        sleep(1)
        i += 1
        print(i * of_total, "% Done")
        
        


