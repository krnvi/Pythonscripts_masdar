#!/usr/bin/python

import os ; import sys ; import urllib2 as urll2 ; import datetime as dt ; import re ; import bs4 ; 
import json ; import numpy as np ; 


url="https://api.data.gov.in/resource/948c3169-fb6f-451f-bda5-4d0d782f756c?format=json&api-key=579b464db66ec23bdd0000012a682ea0155844f84bfbd72f9693214b&limit=2000" 

#&filters[stn_code]=205&fields=field1,field2,field3&sort[field1]=asc"



web=urll2.Request(url) ; htm = urll2.urlopen(web).read() ; 
data=np.matrix([[ln.get('stn_code'),ln.get('state'), ln.get('location_of_monitoring_station'),ln.get('type_of_location'),\
                   ln.get('agency'),ln.get('city_town_village_area'),ln.get('sampling_date'),ln.get('rspm_pm10'),ln.get('pm_2_5'),\
                   ln.get('so2'), ln.get('no2')] for ln in json.loads(htm)['records']])


 https://api.data.gov.in/resource/948c3169-fb6f-451f-bda5-4d0d782f756c?format=json&api-key=
  https://api.data.gov.in/resource/c8a9ab7d-1704-4e4f-8599-9cc35e5f53ad?format=json&api-key=
  
  https://data.gov.in/resources/location-wise-daily-ambient-air-quality-gujarat-year-2010