import pull_data as gcp
import os
import time
import class_metrics as wm
import class_metricfire as mf
import json
import pyrebase
# create directory to store data
data_dir = 'data/'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

metric_dir = 'metrics/'
if not os.path.exists(metric_dir):
    os.makedirs(metric_dir)

# ANCHOR Get farm info
# import list of active farms from firebase
def get_all_data():
    metrics_config = {    
        "apiKey": os.environ.get("METRICS_APIKEY"),
        "authDomain": os.environ.get("METRICS_AUTHDOMAIN"),
        "databaseURL": os.environ.get("METRICS_DBURL"),
        "projectId": os.environ.get("METRICS_PROJECTID"),
        "storageBucket": os.environ.get("METRICS_BUCKET"),
        "messagingSenderId": os.environ.get("METRICS_MESSAGEID")
    }
    firebase = pyrebase.initialize_app(metrics_config)
    db = firebase.database()
    return db.get().val()

previous_data = get_all_data()

li_farms = []
for user in previous_data:
    for farm in previous_data[user]:
        farmtype = user
        print(user,farm)
        try:
            fieldz = previous_data[user][farm]['fields']
            fieldKeys = [i for i, _ in enumerate(fieldz)]
            newfarm = {
                'name': farm,
                'user': user, # AB or LW or other
                'fields': list(fieldKeys)
            }
            li_farms.append(newfarm)
        except: 
            continue

# get meta date information
time_epoch = int(time.time() //86400 * 86400)
date_str = time.strftime('%m-%d-%Y', time.gmtime(time_epoch) ) 

# ANCHOR Calculate metrics loop
metric = None
metrics_to_calculate = {
    'AB': ['ET0','GDD', 'GTR','PM','SM'],
    'LW': [],
    'trial': [],
    'inactive': ['GDD'],
}

li_results = []
for farm in li_farms: # TODO do for all farms
    metric = wm.metric_calculator(farm['name'], date_str)
    errors = metric.check_errors()
    if errors:     # check for errors 
        print(errors) 
    
    # calculate chosen metrics
    results = {
        'farm':farm['name'],
        'user':farm['user'],
        'fields':farm['fields']
    } 
    to_calc = metrics_to_calculate[farm['user']]
    if 'GDD' in to_calc: 
        results['GDD'] = metric.calculate_gdd()
    if 'GTR' in to_calc:
        results['GTR'] = metric.calculate_gdd() # TODO change to GTR
    if 'PM' in to_calc:
        results['PM'] = metric.calculate_powderymildew()
    if 'SM' in to_calc:
        results['SM'] = metric.calculate_spidermites()
    if 'ET0' in to_calc:
        results['ET0'] = metric.calculate_et0pm()
    # TODO calculate additional metrics for LW
    li_results.append( results )

# ANCHOR format and upload
spectral_placeholder = { # used as placeholder for NDVI and SIF measurements
    'delta': 3, 'text': 'Note: This is sample data',
    'ylabel': ' %', 'labelOne': 'History', 'labelTwo': 'Forecast', 
    'dataTwo': [{'x': 20190110, 'y': 1}, {'x': 20190117, 'y': 3.3}, {'x': 20190119, 'y': 2}], 
    'dataOne': [{'x': 20190101, 'y': 5}, {'x': 20190103, 'y': 3}, {'x': 20190105, 'y': 4}, {'x': 20190107, 'y': 4}, {'x': 20190109, 'y': 1}, {'x': 20190110, 'y': 1}], 
    'xlabel': 'Weeks', 'domain': {'xmax': 20190118, 'ymax': 5, 'ymin': 0, 'xmin': 20190104}, 
    'description': 'Spectral indicies, like this one, can be used as a proxy for overall plant health.', 
    'currentVal': 3, '1': {'f': 'f'}
}

def get_growth_icon(i):
    return int(min( max(list(i['GDD'].values())) / 25.0 * 100, 
        99))

def get_pest_icon(i):
    return int(min( 
        10 / max(list(i['PM'].values())) * 100,    
        max(list(i['SM'].values())) / 25.0 * 100,
        99 ))

def get_water_icon(i):
    return int(min( 
        max(list(i['SM'].values()))/ 25.0 * 100,    
        99 )) 

def history_forecast_split(li, curr_time):
    li_forecast = {}
    li_history = {}
    for i in li.keys():
        i_time = time.strptime( i, '%m-%d-%Y' )
        if i_time > curr_time:
            li_forecast[i] =  li[i]
        else:
            li_history[i] = li[i] 
    return li_forecast, li_history

def most_recent_key(li):
    li_times = []
    year = next(iter(li.keys())).split('-')[-1]
    for ti in li.keys():
        li_times.append( # append day of the year
            int(time.strftime('%j',time.strptime(ti, '%m-%d-%Y')) )
        )
    most_recent_date = time.strptime(
        str(max(li_times))+year, '%j%Y'
    )
    return time.strftime('%m-%d-%Y',most_recent_date)

def curr_value(li, curr_time):
    # returns last value
    # NOTE Won't work close to new years
    most_recent_str = most_recent_key(li)
    return li[most_recent_str]

def curr_delta(li, curr_time):
    # NOTE Won't work on January 1st
    yesterday_of_year = int(time.strftime('%j',curr_time) ) -1
    yesterday_year = time.strftime('%Y')
    yesterday_str = str(yesterday_of_year) +'-'+ yesterday_year
    yesterday_time = time.strptime(yesterday_str, '%j-%Y')
    yesterday_date = time.strftime( '%m-%d-%Y', yesterday_time  )
    curr_date = time.strftime( '%m-%d-%Y', curr_time )
    try:
        return li[curr_date] - li[yesterday_date]
    except:
        print('Key error in curr_delta(*) funcion',li, curr_time)
        return 0

def get_x_min_max(li):
    li_int = []
    for i in li.keys():
        i_time = time.strptime(i,'%m-%d-%Y')
        li_int.append(
            int(time.strftime('%Y%m%d',i_time))
        )
    xmin = min(li_int)
    xmax = max(li_int)
    return xmin, xmax

def reformat_date(x):
    x_time = time.strptime(x,'%m-%d-%Y')
    return time.strftime('%Y%m%d',x_time)

def li_to_db(user, farm, metricKey, 
        description, xlabel, ylabel,
        li, curr_time):
    dataTwo, dataOne = history_forecast_split(li, curr_time)
    currentVal = curr_value(li, curr_time)
    delta = curr_delta(li, curr_time)
    ymin = min( list(li.values()) )
    ymax = max( list(li.values()) )+1
    xmin, xmax = get_x_min_max(li)
    labelOne = 'Historical'
    labelTwo = 'Forecast'
    text = description

    if len(dataTwo) > 0:
        labelTwo = 'N/A'

    obj = mf.Metricfire(
        user, farm, farm, metricKey, 
        currentVal, delta, description, xmax, xmin, ymax, 
        ymin, labelOne, labelTwo, text, xlabel, ylabel, 
    )
    
    obj.dataOne = []
    obj.dataTwo = []

    for x,y in dataOne.items():
        obj.add_dataOnePoint(reformat_date(x), y)

    if len(dataTwo) > 0:
        for x,y in dataTwo.items():
            obj.add_dataTwoPoint(reformat_date(x), y)
    else:
        print('forecast not found', user, farm, metricKey)
        for x,y in dataOne.items():
            obj.add_dataTwoPoint(reformat_date(x), y)
    
    return obj.returnStruct()

# upload backup to firebase
def updateFirebase(user, farmkey, fieldkey, fb_struct):
    metrics_config = {    
        "apiKey": os.environ.get("METRICS_APIKEY"),
        "authDomain": os.environ.get("METRICS_AUTHDOMAIN"),
        "databaseURL": os.environ.get("METRICS_DBURL"),
        "projectId": os.environ.get("METRICS_PROJECTID"),
        "storageBucket": os.environ.get("METRICS_BUCKET"),
        "messagingSenderId": os.environ.get("METRICS_MESSAGEID")
    }
    firebase = pyrebase.initialize_app(metrics_config)
    db = firebase.database()
    return db.child(user).child(farmkey).child('fields').child(fieldkey) \
        .set( fb_struct ) # REVIEW add/remove .child('test') during testing

def backupGCP(user, farmkey, fieldkey, fb_struct):
    tmp_fname = 'metric_backup.txt'
    with open(tmp_fname,'w+') as f:
        json.dump(fb_struct,f)

    curr_date = time.strftime( '%m-%d-%Y', curr_time )
    dest_fname = user+'/'+farmkey+'/'+fieldkey+'/' \
        +user+','+farmkey+','+fieldkey+','+curr_date+'.json'
    gcp.upload('vspectral-metric-bucket-1','metric_backup.txt',dest_fname)
    
    try:
        os.remove(tmp_fname)
    except:
        print('failed to remove tempfile',user,farmkey,fieldkey)

curr_epoch = int(time.time() //86400 * 86400)
curr_time = time.gmtime(curr_epoch) 

for i in li_results:
    fb_struct = {}
    print('Processing:',i['farm'])

    # generate structs for each metric from the given lists
    metrics = ['ET0', 'GDD', 'PM', 'SM', 'GTR']
    descriptions = {
        'ET0':'Evapotranspiration is the measure of how much water is released from your field as evaporation from the ground or transpiration from your plants. It’s very important to stay ahead of this to ensure you do not encounter any drought stress - a key detractor of crop quality.',
        'GDD':'Growing degree days is a heuristic tool used to model plant metabolism. It is a calculation of the degrees of temperature between a range. We use a single sin with upper bound cuttoff method.',
        'PM':'The Powdery Mildew Index represents how condusive the weather is for the development of powdery mildew. This index was developed by Gent et. al.',
        'SM':'The spider mites index tracks the reporductive rate of spider mites based on recorded temperature data. This is a proprietary index.',
        'GTR':'GTR stands for growth temperature range. This quantity represents the total growth potential for your fields. This is a function of lower and upper temperatures specific to each variety and total amount of photosynthetically active sunlight your plants can put to work.'
    }
    ylabels = {
        'ET0': '   Inch',
        'GDD': '  DD', 
        'PM': '  Index', 
        'SM': '  Index', 
        'GTR': '  Sol'
    }

    di_data = {}
    for m in metrics:
        di_data[m] = li_to_db(
            i['user'], i['farm'], m, 
            descriptions[m], 'Date', ylabels[m], 
            i[m], curr_time,
        )
    
    # generate importance values for icon descriptors
    grow_icon = get_growth_icon(i)
    pest_icon = get_pest_icon(i)
    water_icon = get_water_icon(i)

    fb_struct = { # aka field name
        'farmType' : i['user'],
        'icons' : {
            'growth' : grow_icon,
            'pest' : pest_icon,
            'water' : water_icon,
        },
        'metrics'  : {
            'ET0' : di_data['ET0'],
            'GDD' : di_data['GDD'],
            'GTR' : di_data['GTR'],
            'PM' : di_data['PM'],
            'SM' : di_data['SM'],
            'NDVI' : spectral_placeholder,
            'SIF' : spectral_placeholder
        },
        'name' : i['farm'],
        'variety' : 'hops'
    }
    updateFirebase(i['user'], i['farm'],i['farm'], fb_struct)
    backupGCP(i['user'], i['farm'],i['farm'], fb_struct)
