#usr/bin/python

import os ; import sys ; import numpy as np ; import datetime as dt ;  from scipy.interpolate import interp1d ; from dateutil import rrule ;

main='/home/vkvalappil/Data/radiometerAnalysis/'  ; scripts=main+'/scripts/' ; outpath=main+'/output/'
date=str(sys.argv[1]) ; 

rso_file='/home/vkvalappil/Data/masdar_station_data/wyoming/'+date[0:6]+'/AbuDhabi_upperair_'+date+'.csv'
met_file='/home/vkvalappil/Data/metarData/_data_mr/'+date[0:4]+'/'+date[0:6]+'/AbuDhabi_'+date[0:8]+'.csv'
print(rso_file)
rso_data=np.genfromtxt(rso_file,delimiter=',',dtype='S') ;
met_data=np.genfromtxt(met_file,delimiter=',',dtype='S') ;
_date=(dt.datetime.strptime(date,'%Y%m%d%H')).strftime('%Y-%m-%d %H:00')

met_data_1=met_data[np.where(np.in1d(met_data[:,2],_date))[0],:]

pres=1013.0 ; hgt=2.0 ; tmp=met_data_1[0,5] ; dpt=met_data_1[0,6] ;  rh =met_data_1[0,7] ; mxr =str(met_data_1[0,11].astype(float)*1000)
ws=met_data_1[0,9] ; wd=met_data_1[0,8]
new_data=np.vstack([pres,hgt,tmp,dpt,rh,mxr,ws,wd,0,0,0]).T
rso_data_1=np.concatenate([rso_data[0:2,:],new_data],axis=0)
rso_data_2=np.concatenate([rso_data_1,rso_data[2:,:]])

outFile='/home/vkvalappil/Data/masdar_station_data/wyoming/metar+rs/'+date[0:6]+'/AbuDhabi_upperair_'+date+'.csv'
np.savetxt(outFile,rso_data_2,delimiter=',',fmt='%s')