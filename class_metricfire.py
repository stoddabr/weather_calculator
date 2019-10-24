import pyrebase
import json


class Metricfire:
    def __init__(self, 
            user, farm, fieldKey, metricKey, 
            currentVal, delta, description, xmax, xmin, ymax, 
            ymin, labelOne, labelTwo, text, xlabel, ylabel, 
            dataOne=[], dataTwo=[]):
        self.farmKey = farm
        self.metricKey = metricKey
        self.currentVal = currentVal
        self.dataOne = dataOne
        self.dataTwo = dataTwo
        self.delta = delta
        self.description = description
        self.domain = {
            'xmax' : xmax,
            'xmin' : xmin,
            'ymax' : ymax,
            'ymin' : ymin
        }
        self.labelOne = labelOne
        self.labelTwo = labelTwo
        self.text = text
        self.xlabel = xlabel
        self.ylabel = ylabel
        # auth firebase
        metrics_config = {    
            "apiKey": os.environ.get("METRICS_APIKEY"),
            "authDomain": os.environ.get("METRICS_AUTHDOMAIN"),
            "databaseURL": os.environ.get("METRICS_DBURL"),
            "projectId": os.environ.get("METRICS_PROJECTID"),
            "storageBucket": os.environ.get("METRICS_BUCKET"),
            "messagingSenderId": os.environ.get("METRICS_MESSAGEID")
        }
        firebase = pyrebase.initialize_app(metrics_config)
        self.db = firebase.database()

    def add_dataOnePoint(self,numDate,value):
        self.dataOne.append(
            {
                'x':numDate,
                'y':value,
            }
        )

    def add_dataTwoPoint(self,numDate,value):
        self.dataTwo.append(
            {
                'x':numDate,
                'y':value,
            }
        )

    def updateFirebase(self):
        metricData = {
            'currentVal':self.currentVal,
            'dataOne':self.dataOne,
            'dataTwo':self.dataTwo,
            'delta':self.delta,
            'description':self.description,
            'domain':self.domain,
            'labelOne':self.labelOne,
            'labelTwo':self.labelTwo,
            'text':self.text,
            'xlabel':self.xlabel,
            'ylabel':self.ylabel,
        }
        self.db.child(self.user).child(self.farmKey).child('fields').child(self.fieldKey).\
            child("metrics").child(self.metricKey).set(metricData)

    def returnStruct(self):
        metricData = {
            'currentVal':self.currentVal,
            'dataOne':self.dataOne,
            'dataTwo':self.dataTwo,
            'delta':self.delta,
            'description':self.description,
            'domain':self.domain,
            'labelOne':self.labelOne,
            'labelTwo':self.labelTwo,
            'text':self.text,
            'xlabel':self.xlabel,
            'ylabel':self.ylabel,
        }
        return metricData

'''
user = 'Test'
farm = 'metricfire class test'
metricKey = 'test'
currentVal = 3
delta = -2
description = "this is a description"
xmax = 20190111 # date
xmin = 20190101
ymax = 5
ymin = 0
labelOne = 'Historical'
labelTwo = 'Forecast'
text = 'text displayed below the graph'
xlabel = 'time'
ylabel = 'metric'

testclass = Metricfire(
    user, farm, metricKey, 
    currentVal, delta, description, xmax, xmin, ymax, 
    ymin, labelOne, labelTwo, text, xlabel, ylabel, 
)

testclass.add_dataOnePoint(20190101,4)
testclass.add_dataOnePoint(20190103,4)
testclass.add_dataTwoPoint(20190103,4)
testclass.add_dataTwoPoint(20190105,2)
testclass.add_dataTwoPoint(20190107,2)
testclass.add_dataTwoPoint(20190109,4)
testclass.add_dataTwoPoint(20190111,2)
print('updating')
testclass.updateFirebase()
print('done updating')
'''