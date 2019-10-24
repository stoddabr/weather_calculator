# development is tested here

import pull_data as gcp
import os
import time
import class_metrics as wm
import json
import evaplib
import datetime
import numpy as np
import scipy
from scipy import integrate

#TODO bug where the oldest day is truncated before 7am greatly influencing things

# declare raw string to avoid "anomalous backslash" warning
#f_forecast = '04-12-2019\Brett\'s-House,04-12-2019,history.json'
#f_history = "04-12-2019\Brett's-House,04-12-2019,history.json" 
field = { # test field id
    "format":"zip",
    "uid":"www420blazeit6669",
    "name":"Brett's-House",
    "data":"97140",
    "crop":"potato" #TODO add to deployed active-fields.json
}
date_str = '04-12-2019' #time.strftime('%m-%d-%Y', time.gmtime(time_epoch) ) 

# make directories
data_dir = 'data/'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

metric_dir = 'metrics/'
if not os.path.exists(metric_dir):
    os.makedirs(metric_dir)

# ANCHOR inside of loop metric calculator

# get data for each field
metric = wm.metric_calculator(field['name'], date_str)
errors = metric.check_errors()
if errors: print(errors) # check for errors 

# calculate chosen metrics
results = {}
results['gdd'] = metric.calculate_gdd()
results['makkink'] = metric.calculate_et_makkink()
results['powdery'] = metric.calculate_powderymildew()
results['mites'] = metric.calculate_spidermites()

# ANCHOR begin standbox
forecast = metric.forecast
history = metric.history



'''
inferior method of grouping metrics by day
#str_day = time.strftime("%m-%d-%Y",time.gmtime(forecast[0]['epoch']))

for data_hour in history[8:]: # same day of data, history is taken at 7am
    current_day = time.strftime("%m-%d-%Y",time.gmtime(data_hour['epoch']))
    if str_day == current_day:
        metric_culm = metric_culm + \
            min(data_hour['air temperature'],high-low)
    else: # new day of data
        day_metric[str_day] = metric_culm
        metric_culm = 0
        str_day = current_day
'''

#time.strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

# TODO save results as json file

# ANCHOR example result
# returned format is indexed epoch times for each metric
# forecast and history are daily values
example_result = {
    'et':{
        '04-12-2019': 6.7, # history
        '04-13-2019': 7.9, # today
        '04-14-2019': 4.2, # forecast
    },
    'spei':{
        '04-12-2019': 6.7, # history
        '04-13-2019': 7.9, # today
        '04-14-2019': 4.2, # forecast     
    }
}