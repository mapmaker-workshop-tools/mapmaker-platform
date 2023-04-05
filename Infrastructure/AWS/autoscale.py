import os
import json
import time
from statistics import mean
import pandas as pd


"""
This script helps you get the CPU and MEMORY usage of AWS lightsail container services. 
From there it can scale up or down the capacity.

Source: https://docs.aws.amazon.com/cli/latest/reference/lightsail/get-container-service-metric-data.html

"""


"""SETUP"""
DATA_INTERVAL = 900 # Takes the average server load over that interval in seconds. e.g. 3600 means get the average over last hour
N_ITEMS_TO_EVALUATE = 5 #How many datapoints do we use to make a decision (We take the average load over those points)
MIN_NUMBER_INSTANCES = 1 # Define how many instances you want minimum
MAX_NUMBER_INSTANCES = 3 #Define the maximum number of instances you want
MIN_POWER_INSTANCE = 'nano'  #Options are: ['nano' , 'micro' , 'small' , 'medium' , 'large' , 'xlarge']
MAX_POWER_INSTANCE = 'micro' #Options are: ['nano' , 'micro' , 'small' , 'medium' , 'large' , 'xlarge']
ENABLE_AUTOSCALING = False #Disable for testing

# AUTOSCALING: integers represent % of load
SCALE_UP_IF_CPU = 20 #If the load goes above this threshold we'll scale up
SCALE_UP_IF_MEM = 20 #If the load goes above this threshold we'll scale up
SCALE_DOWN_IF_CPU = 15 #If load is below this number the server will scale down 
SCALE_DOWN_IF_MEM = 15 # If load is below this number the server will scale down 
SCALE_PREFERENCE = 'horizontal' # 'horizontal', 'vertical' or 'both' for aggressive scaling


#Sanity check lowerbound should always be higher than treshold to scale up
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
    print("\n\n #### Scaling to ####")
    print(scale, power)
    if ENABLE_AUTOSCALING:
        AWS = os.popen("aws lightsail update-container-service --service-name mapmaker --scale " +scale+" --power "+power).read()
    else: 
        print("No update because ENABLE_AUTOSCALING is False\n\n")
        print("Desired outcome: ")
        print(scale, power)

def evaluate(CPU, MEM, SCALE, POWER):
    """
    Decides if we should scale up or down
    """
    print("\n\n #### Current settings  ####")
    print(SCALE, POWER)
    #Validating if we are below minimum
    options = ['nano' , 'micro' , 'small' , 'medium' , 'large' , 'xlarge']
    current = options.index(POWER)
    minimum = options.index(MIN_POWER_INSTANCE)
    if current < minimum:
        result = "Power Under minimum"
        scale_to(scale, minimum)
    elif MIN_NUMBER_INSTANCES > SCALE:
        result = "Instance under minimum"
        scale_to(MIN_NUMBER_INSTANCES, POWER)
    elif CPU > SCALE_UP_IF_CPU or MEM > SCALE_UP_IF_MEM:
        #Validate if we reached the limits we set
        if SCALE == MAX_NUMBER_INSTANCES or SCALE > 19 :
            result = "Max. instances reached"
        #Validate if we reached the limits we set
        elif POWER == MAX_POWER_INSTANCE or POWER == 'xlarge':
            result = "Max. Power reached"
        #If we are not hitting our limits: We should scale
        else:
            if SCALE_PREFERENCE == 'horizontal':
                power = POWER
                scale = SCALE + 1
                scale_to(scale, power)
                result = "Scaling up horizontal"
            if SCALE_PREFERENCE == 'vertical':
                power = find_capacity(POWER, 'up')
                scale = SCALE
                scale_to(scale, power)
                result = "Scaling up vertical"
            if SCALE_PREFERENCE == 'both':
                power = find_capacity(POWER, 'up')
                scale = SCALE + 1
                scale_to(scale, power)
                result = "Scaling up both"
    elif CPU < SCALE_DOWN_IF_CPU or MEM < SCALE_DOWN_IF_MEM:
        #Validate if we reached the limits we set
        if SCALE == MIN_NUMBER_INSTANCES or SCALE == 1 :
            result = "Min. instances reached"
        #Validate if we reached the limits we set
        elif POWER == MIN_POWER_INSTANCE or POWER == 'nano':
            result = "Min. Power reached"
        else:
            if SCALE_PREFERENCE == 'horizontal':
                power = POWER
                scale = SCALE - 1
                scale_to(scale, power)
                result = "Scaling down horizontal"
            if SCALE_PREFERENCE == 'vertical':
                power = find_capacity(POWER, 'down')
                scale = SCALE
                scale_to(scale, power)
                result = "Scaling down vertical"
            if SCALE_PREFERENCE == 'both':
                power = find_capacity(POWER, 'down')
                scale = SCALE - 1
                scale_to(scale, power)
                result = "Scaling down both"


    else:
        result = "Load within parameters"
    return result

    
        
def find_capacity(current, upordown):
    """
    Finds the capacity we should scale to. 
    """
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
data = {'CPU': [0],
        'Memory': [0],
        'Period (Sec)': [0],
        'Capacity': [0],
        'Power': [''],
        'Decision': [''],
        'State': ['']}
df = pd.DataFrame(data)
 

"""
Main loop that checks
"""
#while True:
current_scale, current_power, current_state = get_current_configuration()
df = df.tail(N_ITEMS_TO_EVALUATE)
CPU = get_average_CPU(DATA_INTERVAL)
MEMORY = get_average_Memory(DATA_INTERVAL)

if current_state == "UPDATING":
    print("\n\nCapacity is already updating - no need to evaluate")
    decision = "Wait for new server to come live"
else:
    decision = evaluate(CPU, MEMORY, current_scale, current_power)

new_row = {'CPU': CPU, 
        'Memory': MEMORY, 
        'Period (Sec)':DATA_INTERVAL, 
        'Capacity': current_scale, 
        'Power':current_power, 
        'State': current_state, 
        'Decision':decision}
df.loc[len(df)] = new_row
df = df.tail(N_ITEMS_TO_EVALUATE)
print(df)