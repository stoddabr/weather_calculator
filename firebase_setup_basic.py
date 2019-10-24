import pyrebase
import json
import os

metrics_config = {    
    "apiKey": os.environ.get("METRICS_APIKEY"),
    "authDomain": os.environ.get("METRICS_AUTHDOMAIN"),
    "databaseURL": os.environ.get("METRICS_DBURL"),
    "projectId": os.environ.get("METRICS_PROJECTID"),
    "storageBucket": os.environ.get("METRICS_BUCKET"),
    "messagingSenderId": os.environ.get("METRICS_MESSAGEID")
}
farms_config = {    
    "apiKey": os.environ.get("FARMS_APIKEY"),
    "authDomain": os.environ.get("FARMS_AUTHDOMAIN"),
    "databaseURL": os.environ.get("FARMS_DBURL"),
    "projectId": os.environ.get("FARMS_PROJECTID"),
    "storageBucket": os.environ.get("FARMS_BUCKET"),
    "messagingSenderId": os.environ.get("FARMS_MESSAGEID")
}
fields_config = {    
    "apiKey": os.environ.get("FIELDS_APIKEY"),
    "authDomain": os.environ.get("FIELDS_AUTHDOMAIN"),
    "databaseURL": os.environ.get("FIELDS_DBURL"),
    "projectId": os.environ.get("FIELDS_PROJECTID"),
    "storageBucket": os.environ.get("FIELDS_BUCKET"),
    "messagingSenderId": os.environ.get("FIELDS_MESSAGEID")
}

fb_metrics = pyrebase.initialize_app(metrics_config)
db_metrics = fb_metrics.database()
data_metrics = db_metrics.get().val()

fb_farms = pyrebase.initialize_app(farms_config)
db_farms = fb_farms.database()
data_farms = db_farms.get().val()
data_devfarms = db_farms.child('devtest').get().val()

fb_fields = pyrebase.initialize_app(fields_config)
db_fields = fb_fields.database()
data_fields = db_fields.child().get().val()

''' [TEST] 
ab_fields = [{"farm name": "Tavern", "TA id": "none", "lat": 48.992206, "lon": -116.525117, "field name": "Field 51"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.993072, "lon": -116.519451, "field name": "Field 41"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.992926, "lon": -116.513062, "field name": "Field 31"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.993454, "lon": -116.506592, "field name": "Field 21"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.989227, "lon": -116.524565, "field name": "Field 52"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.989863, "lon": -116.518636, "field name": "Field 42"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.989049, "lon": -116.511978, "field name": "Field 32"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.989852, "lon": -116.505716, "field name": "Field 22"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.986377, "lon": -116.52385, "field name": "Field 53"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.986829, "lon": -116.517766, "field name": "Field 43"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.986274, "lon": -116.511089, "field name": "Field 33"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.986664, "lon": -116.504957, "field name": "Field 23"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.995712, "lon": -116.500899, "field name": "Field 11"}, {"farm name": "Tavern", "TA id": "none", "lat": 48.986805, "lon": -116.498311, "field name": "Field 12"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.888313, "lon": -116.430153, "field name": "Field 60"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.882665, "lon": -116.430733, "field name": "Field 61"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.885369, "lon": -116.427361, "field name": "Field 50"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.88193, "lon": -116.426226, "field name": "Field 51"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.884727, "lon": -116.421681, "field name": "Field 40"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.877939, "lon": -116.427341, "field name": "Field 62"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.874562, "lon": -116.427684, "field name": "Field 63"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.873332, "lon": -116.43157, "field name": "Field 70"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.871171, "lon": -116.428533, "field name": "Field 64"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.868348, "lon": -116.427678, "field name": "Field 65"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.86643, "lon": -116.427244, "field name": "Field 66"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.870928, "lon": -116.424547, "field name": "Field 52"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.870509, "lon": -116.418626, "field name": "Field 41"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.870296, "lon": -116.414387, "field name": "Field 31"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.873433, "lon": -116.414165, "field name": "Field 30"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.843025, "lon": -116.418491, "field name": "Field 59"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.847001, "lon": -116.420517, "field name": "Field 58"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.850308, "lon": -116.421115, "field name": "Field 57"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.853286, "lon": -116.421473, "field name": "Field 56"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.848658, "lon": -116.417048, "field name": "Field 48"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.850845, "lon": -116.417303, "field name": "Field 47"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.853728, "lon": -116.41751, "field name": "Field 46"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.850344, "lon": -116.411841, "field name": "Field 37"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.850245, "lon": -116.406717, "field name": "Field 24"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.853495, "lon": -116.400846, "field name": "Field 12"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.852981, "lon": -116.406459, "field name": "Field 23"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.852878, "lon": -116.412507, "field name": "Field 36"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.857339, "lon": -116.401339, "field name": "Field 11"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.859873, "lon": -116.406793, "field name": "Field 21"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.85695, "lon": -116.406652, "field name": "Field 22"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.860387, "lon": -116.412536, "field name": "Field 34"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.856832, "lon": -116.412198, "field name": "Field 35"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.860219, "lon": -116.418247, "field name": "Field 44"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.856754, "lon": -116.417863, "field name": "Field 45"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.858736, "lon": -116.422916, "field name": "Field 55"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.863893, "lon": -116.412484, "field name": "Field 33"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.867449, "lon": -116.413755, "field name": "Field 32"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.867303, "lon": -116.418767, "field name": "Field 42"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.863749, "lon": -116.418599, "field name": "Field 43"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.867172, "lon": -116.42397, "field name": "Field 53"}, {"farm name": "Backwoods", "TA id": "none", "lat": 48.863672, "lon": -116.42379, "field name": "Field 54"}]
li_backwood_fields = []
li_tavern_fields = []
for i in ab_fields:
    fielddata = {}
    li_items = ['farmType','variety','icons','metrics']
    for j in li_items:
        fielddata[j] = newmetric[j]
    fielddata['lat'] = i['lat']
    fielddata['lon'] = i['lon']
    fielddata['name'] = i['field name']
    fielddata['criticalpoints'] = [
{
"stressType": "PvY",
"diseaseLatitude": i['lat']+0.0001,
"diseaseLongitude": i['lon']+0.0001,
"diseaseSeverity": 1.0
}
    ]
    if i['farm name'] == 'Backwoods':
        li_backwood_fields.append(fielddata)
    elif i['farm name'] == 'Tavern':
        li_tavern_fields.append(fielddata)
    else:
        raise Exception('not found')
[/TEST]
'''
