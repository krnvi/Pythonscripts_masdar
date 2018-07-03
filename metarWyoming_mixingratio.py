#usr/bin/python

import os ; import sys ; import numpy as np ; import pandas as pd ; 
import datetime as dt ;  from dateutil import rrule ;
import metpy.calc as mcalc ; from metpy.units import units

main='/home/vkvalappil/Data/masdar_station_data/'  ; scripts=main+'/scripts/' ;  
date=str(sys.argv[1]) ; 

date_1=dt.datetime.strptime(date,'%Y%m%d')+dt.timedelta(hours=0) ; date_2=dt.datetime.strptime(date,'%Y%m%d')+dt.timedelta(hours=23)
date_list=[x.strftime('%Y-%m-%d %H:%M') for x in rrule.rrule(rrule.HOURLY,dtstart=date_1,until=date_2)]

metar_file=main+'/wyoming/'+date[0:6]+'/AbuDhabi_surf_'+date[0:8]+'.csv'
outFile=main+'/wyoming/'+date[0:6]+'/AbuDhabi_surf_mr'+date[0:8]+'.csv'

metar_data=pd.read_csv(metar_file) 

metar_data=metar_data[['STN','TIME','ALTM','TMP','DEW','RH','DIR','SPD','VIS']]
#metar_data=metar_data.drop('Unnamed: 9',axis=1)
metar_data=metar_data.drop(metar_data.index[0])
metar_data['TIME']=date_list

tmp=np.array((metar_data.iloc[:,3]).apply(pd.to_numeric,errors='coerce')+273.15)*units('K')
rh=np.array((metar_data.iloc[:,5]).apply(pd.to_numeric,errors='coerce')/100.0)
press=np.array((metar_data.iloc[:,2]).apply(pd.to_numeric,errors='coerce'))*units('millibar')

mrio=mcalc.mixing_ratio_from_relative_humidity(rh,tmp,press)

metar_data['mrio']=mrio 

metar_data.to_csv(outFile)

