import os
import json
import time
from statistics import mean
import pandas as pd
from datetime import datetime

"""
This script helps you get the CPU and MEMORY usage of AWS lightsail container services. 
From there it can scale up or down the capacity.

Source: https://docs.aws.amazon.com/cli/latest/reference/lightsail/get-container-service-metric-data.html

"""


"""SETUP"""
DATA_INTERVAL = 3600 #sets how far you want to look back for capacity (In seconds)
REFRESH_INTERVAL = 15 #Set's the frequency at which we check the capacity (in seconds)
N_ITEMS_TO_EVALUATE = 5 #How many datapoints do we use to make a decision (We take the average load over those points)
MIN_NUMBER_INSTANCES = 1 # Define how many instances you want
MAX_NUMBER_INSTANCES = 2 #Define the maximum number of instances you want
ENABLE_AUTOSCALING = True
SCALE_UP_IF_CPU = 70
SCALE_UP_IF_MEM = 70
SCALE_DOWN_IF_CPU = 2
SCALE_DOWN_IF_MEM = 30
SCALE_PREFERENCE = 'both' # 'horizontal', 'vertical' or 'both' for aggressive scaling


#Sanity check
if SCALE_DOWN_IF_CPU > SCALE_UP_IF_CPU:
    raise Exception("ERROR Lower threshold not met")
if SCALE_DOWN_IF_MEM > SCALE_UP_IF_MEM:
    raise Exception("ERROR Lower threshold not met")

def get_average_CPU(since_seconds):
    print("getting CPU")
    now = round(time.time())
    since = now - since_seconds
    now = str(now)
    since = str(since)
    unit = os.popen("aws lightsail get-container-service-metric-data --service-name mapmaker --metric-name CPUUtilization --period 300 --start-time "+since+" --end-time "+now+" --statistics Average --output json").read()
    unit = json.loads(unit)
    average_load = [d['average'] for d in unit['metricData']]
    average_load = mean(average_load)
    return round(average_load)

def get_average_Memory(since_seconds):
    print("getting MEM")
    now = round(time.time())
    since = now - since_seconds
    now = str(now)
    since = str(since)
    unit = os.popen("aws lightsail get-container-service-metric-data --service-name mapmaker --metric-name MemoryUtilization --period 300 --start-time "+since+" --end-time "+now+" --statistics Average --output json").read()
    unit = json.loads(unit)
    average_load = [d['average'] for d in unit['metricData']]
    average_load = mean(average_load)
    return round(average_load)

def get_current_configuration():
    print("getting current config")
    unit = os.popen("aws lightsail get-container-services --service-name mapmaker --output json").read()
    unit = json.loads(unit)
    power = unit['containerServices'][0]['power']
    scale = unit['containerServices'][0]['scale']
    state = unit['containerServices'][0]['state']
    return scale, power, state 

def scale_to(scale, power):
    if scale == 0:
        scale = 1
    print("\n\n###### RESULT #######")
    print(scale)
    print(power)


def evaluate(CPU, MEM, SCALE, POWER):
    print("evaluate")
    if CPU > SCALE_UP_IF_CPU or MEM > SCALE_UP_IF_MEM:
        if SCALE_PREFERENCE == 'horizontal':
            power = POWER
            scale = SCALE + 1
            scale_to(scale, power)
            return 'scaling up horizontally'
        if SCALE_PREFERENCE == 'vertical':
            power = find_capacity(POWER, 'up')
            scale = SCALE
            scale_to(scale, power)
            return 'scaling up vertically'
        if SCALE_PREFERENCE == 'both':
            power = find_capacity(POWER, 'up')
            scale = SCALE + 1
            scale_to(scale, power)
            return 'scaling up vertically and horizontally'
    elif CPU > SCALE_DOWN_IF_CPU or MEM > SCALE_DOWN_IF_MEM:
        if SCALE_PREFERENCE == 'horizontal':
            power = POWER
            scale = SCALE + 1
            scale_to(scale, power)
            return 'scaling down horizontally'
        if SCALE_PREFERENCE == 'vertical':
            power = find_capacity(POWER, 'down')
            scale = SCALE
            scale_to(scale, power)
            return 'scaling down vertically'
        if SCALE_PREFERENCE == 'both':
            power = find_capacity(POWER, 'down')
            scale = SCALE - 1
            scale_to(scale, power)
            return 'scaling down vertically and horizontally'
    else:
        return "Load within specification"
        
def find_capacity(current, upordown):
    print("Finding capacity")
    options = ['nano' , 'micro' , 'small' , 'medium' , 'large' , 'xlarge']
    index = options.index(current)
    if upordown == 'up':
        if index == 5:
            return options[index]
        return options[index+1]
    if upordown == 'down':
        if index == 0:
            return options[index]
        return options[index-1]
    



# Initialize empty dataframe
data = {'Timestamp': [0],
        'CPU': [0],
        'Memory': [0],
        'Period (Sec)': [0],
        'Capacity': [0],
        'Power': [''],
        'Decicion': [''],
        'State': ['']}
df = pd.DataFrame(data)
 

while ENABLE_AUTOSCALING:
    current_scale, current_power, current_state = get_current_configuration()
    df = df.tail(N_ITEMS_TO_EVALUATE)
    CPU = get_average_CPU(DATA_INTERVAL)
    MEMORY = get_average_Memory(DATA_INTERVAL)
    if current_state == "UPDATING":
        print("Capacity is already updating - no need to evaluate")
        decision = "Do nothing"
    else:
        decision = evaluate(CPU, MEMORY, current_scale, current_power)

    now = datetime.now()  
    new_row = {'Timestamp': now, 
            'CPU': CPU, 
            'Memory': MEMORY, 
            'Period (Sec)':DATA_INTERVAL, 
            'Capacity': current_scale, 
            'Power':current_power, 
            'State': current_state, 
            'Decicion':decision}
    df.loc[len(df)] = new_row
    df = df.tail(N_ITEMS_TO_EVALUATE)
    print(df)
    time.sleep(REFRESH_INTERVAL)
