# weather_metrics
Code for calculating weather metrics and pulling structured data from gcp storage

vm_script - script meant to run on the VM to automate process of calculating weather for multiple farms. Ran 
    daily from cron
pull_data.py - module with methods to pull weather data from google cloud storage bucket
class_metrics - module that contains a metric class. Functions of the class calculate various 
    weather meatrics
class_metricfire - module containing a class to gracefully push data into firebase to be used by a moble app


Open Source Module Dependancies: 
mateolib - library used to help convert climate units required by evaplib
evaplib - library used to help calculate actual evaporation from meteorological data.