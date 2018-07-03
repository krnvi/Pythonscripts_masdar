#!/usr/bin/python
import sys; import numpy as np ; import netCDF4 as nf ; import datetime as dt ;  
from scipy.interpolate import interp2d ; from dateutil import rrule, tz 

main='/home/vkvalappil/Data/modelWRF/' ; scripts=main+'/scripts/' ; output=main+'ARW/output/'
date=str(sys.argv[1]) ;  fcs_leaddays=3 ; #provide date as argument, forecast start and end date defined
fcs_st_date=dt.datetime.strptime(date,'%Y%m%d%H') ; fcs_ed_date=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=fcs_leaddays));  

lstFle=main+'/scripts/master_uae.csv'  ; outFile=output+'hourly'+date+'_wrf.csv' ; 

# Reading data from lst file and model output files
lst_f=np.genfromtxt(lstFle,delimiter=',', dtype="S") ; lst_f=lst_f[lst_f[:,0].argsort(kind='mergesort')]  
points=lst_f[:,1:3].astype(float) ; noloc=points.shape[0] 

file_date_list=[x.strftime('%Y-%m-%d_%H:%S:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)] ; #forecast start and end datelist 
file_date_list=file_date_list[6]

day_list=np.array(range(0,fcs_leaddays)) ; day_seq=np.vstack(np.tile(np.repeat(day_list,24),noloc)) 

c_date=np.vstack(np.repeat(fcs_st_date.strftime('%Y-%m-%d'),noloc*44))
c_date1=np.vstack(np.repeat((dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(hours=6)).strftime('%Y-%m-%d-%H'),noloc*44))

tint=1 ; slev=0 ; elev=44 #len(file_date_list)-1 ; #tmp.shape[0]-1 

from_zone = tz.gettz('UTC') ; to_zone = tz.gettz('Asia/Dubai') ; 
date_list=[(x.replace(tzinfo=from_zone)).astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)]
date_list=date_list[0::tint] ; 


date_list=date_list[6] ; f_date=np.vstack(np.tile(date_list,noloc*44)) ; 

tid=np.vstack(np.repeat(lst_f[:,0],44))  ; pre_mat=np.concatenate([tid,c_date,c_date1,f_date],axis=1)

#time intervel, start time and end time defined. 

temp=np.empty((0,noloc)) ; mrio=np.empty((0,noloc)) ; 
for i in range(slev,elev):
    files=main+'ARW/wrf_output/'+date+'/wrfout_d02_'+file_date_list 
    f=nf.Dataset(files, mode='r')

    lat=(np.squeeze(f.variables['XLAT'][:]))  ; lat1=np.vstack(lat[:,0]) ; 
    lon=(np.squeeze(f.variables['XLONG'][:])) ; lon1=np.vstack(lon[0,:])

    tmp=np.squeeze(f.variables['T'][:]) -300
    #rh=np.squeeze(f.variables['RH2'][:])
    MR=np.squeeze(f.variables['QVAPOR'][:])

    
    tmp_f=interp2d(lon1,lat1, tmp[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    mrio_f=interp2d(lon1,lat1, MR[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 


    temp=np.concatenate([temp,(np.array([tmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    mrio=np.concatenate([mrio,(np.array([mrio_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      


#### data is arranged in req format
temp=np.round(temp[0::tint]).astype(int) ; temp=np.vstack(temp.flatten('F'))
#temp=np.round(temp.reshape(fcs_leaddays,8,noloc)).astype(int) ;
mrio=(mrio[0::tint]).astype(float)       ; mrio=np.vstack(mrio.flatten('F'))


header='TEHSILID,DATE,DATE(GMT),DATE(UAE),TEMP,MXRATIO'
header=np.vstack(np.array(header.split(","))).T

fin_mat1=np.concatenate([pre_mat,temp,mrio],axis=1)
fin_mat=np.concatenate([header,fin_mat1],axis=0)
## saving file
np.savetxt(outFile,fin_mat,fmt="%s",delimiter=',')


quit()

