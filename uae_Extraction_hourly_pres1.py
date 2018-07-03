#!/usr/bin/python
############################## National 3Hourly Data Extraction ##################################################################
#importing necessary modules
import sys ; import numpy as np ; import scipy as sp ; from scipy.interpolate import interp2d ; import datetime as dt
from scipy.interpolate import griddata ; import datetime ; import time ; import pygrib as pg ;from dateutil import rrule, tz

start_time = time.time()
#### path and input files are defined
main='/home/OldData/modelWRF/NMMV3.7/' ; scripts=main+'/scripts/' ; output=main+'/output/'
date=str(sys.argv[1]) ; fcs_leaddays=3 ; 
fcs_st_date=dt.datetime.strptime(date,'%Y%m%d%H') ; fcs_ed_date=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=fcs_leaddays));

lstFle=main+'/scripts/master_uae.csv'
modFile=main+'/UPPV3.0/run/poutpost/' + date +'/wrfpost_d02.'+date

outFile=output+'hourly_pres'+date+'.csv' ; 
############ Required data is read from the wrf output
grb_f=pg.open(modFile) ; 
lst_f=np.genfromtxt(lstFle,delimiter=',', dtype="S") ; lst_f=lst_f[lst_f[:,0].argsort(kind='mergesort')]  
points=lst_f[:,1:3].astype(float) ; noloc=points.shape[0] 
tmp=(np.array(grb_f.select(name="Temperature",typeOfLevel='isobaricInhPa')))[150:175] 
RH=(np.array(grb_f.select(name="Relative humidity",typeOfLevel='isobaricInhPa')))[150:175]
dtmp=(np.array(grb_f.select(name="Dew point temperature",typeOfLevel='isobaricInhPa')))[150:175] 
ugrd=(np.array(grb_f.select(name="U component of wind",typeOfLevel='isobaricInhPa')))[150:175]
vgrd=(np.array(grb_f.select(name="V component of wind",typeOfLevel='isobaricInhPa')))[150:175]

grb_f.close()

lat=tmp[0].data()[1] ; lon=tmp[0].data()[2] ; 
s_indx=-1 ; e_indx=24 ; tint=1

#day_list=np.array(range(0,fcs_leaddays)) ; day_seq=np.vstack(np.tile(np.repeat(day_list,24),noloc)) 
#####  date day seq and time are arranged in req format #######################

#tim_list=(np.array(range(06,24,1) + range(00,06,1))) ; tim_list=[str(k).rjust(2, '0')for k in tim_list] 
#tim_seq=np.vstack(np.tile(tim_list,3*noloc)) ;
c_date=np.vstack(np.repeat(fcs_st_date.strftime('%Y-%m-%d-%H'),noloc*25))

c_date1=np.vstack(np.repeat((dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(hours=6)).strftime('%Y-%m-%d-%H'),noloc*25))

from_zone = tz.gettz('UTC') ; to_zone = tz.gettz('Asia/Dubai') ; 
date_list=[(x.replace(tzinfo=from_zone)).astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)]
date_list=date_list[6] ; f_date=np.vstack(np.tile(date_list,noloc*25)) ; 

outFile=output+'Pres_'+date+'_'+date_list[0:10]+'_12UTC.csv' ; 

tid=np.vstack(np.repeat(lst_f[:,0],25))  ; pre_mat=np.concatenate([tid,c_date,c_date1,f_date],axis=1)

lon=np.vstack(lon[0,:]) ; lat=np.vstack(lat[:,0]) ; #lat=lat[::-1] 
temp=np.empty((0,noloc)) ; rhum=np.empty((0,noloc)) ;uwnd=np.empty((0,noloc)) ; vwnd=np.empty((0,noloc)) ; dtemp=np.empty((0,noloc))
levs=np.empty((25,1)) ;
###### Interpolating to each location 
for i in range(e_indx,s_indx,-1):
    tmp1=tmp[i].data()
    tmp_f=interp2d(lon,lat, tmp1[0]-273.15,kind='linear',copy=False,bounds_error=True ) ; 
    #temp=np.concatenate([temp,(np.array([tmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)

    dtmp1=dtmp[i].data() ; levs[24-i]=tmp[i].level ;  
    dtmp_f=interp2d(lon,lat, dtmp1[0]-273.15,kind='linear',copy=False,bounds_error=True ) ; 

    rhum1=RH[i].data() ;
    rhum_f=interp2d(lon,lat, rhum1[0],kind='linear',copy=False,bounds_error=True ) ;
    
    ugrd1=ugrd[i].data()    
    ugrd_f=interp2d(lon,lat, ugrd1[0],kind='linear',copy=False,bounds_error=True ) ; 
    
    vgrd1=vgrd[i].data()    
    vgrd_f=interp2d(lon,lat, vgrd1[0],kind='linear',copy=False,bounds_error=True ) ; 
    
    temp=np.concatenate([temp,(np.array([tmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    dtemp=np.concatenate([dtemp,(np.array([dtmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    rhum=np.concatenate([rhum,(np.array([rhum_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  
    uwnd=np.concatenate([uwnd,(np.array([ugrd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    vwnd=np.concatenate([vwnd,(np.array([vgrd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  

levs=np.vstack(np.tile(levs,noloc).flatten('F'))    
wdir=np.round(270-(np.arctan2(vwnd,uwnd))*(180/3.14)).astype(int)   ; wdir[wdir>360]=wdir[wdir>360]-360 
wspd=np.round(np.sqrt(np.square(uwnd)+np.square(vwnd))*3.6).astype(int) ; 

#### data is arranged in req format
temp=np.round(temp[0::tint]).astype(int) ; temp=np.vstack(temp.flatten('F'))
#temp=np.round(temp.reshape(fcs_leaddays,8,noloc)).astype(int) ;
dtemp=np.round(dtemp[0::tint]).astype(int) ; dtemp=np.vstack(dtemp.flatten('F'))
rhum=np.round(rhum[0::tint]).astype(int) ; rhum=np.vstack(rhum.flatten('F'))
#rhum=np.round(rhum.reshape(fcs_leaddays,tint,noloc)).astype(int) ;
wdir=np.round(wdir[0::tint]).astype(int) ; wdir=np.vstack(wdir.flatten('F'))
wspd=np.round(wspd[0::tint]).astype(int) ; wspd=np.vstack(wspd.flatten('F'))

header='TEHSILID,DATE,DATE(GMT),DATE(local),Pres_level,TEMP,DTEMP,RH,WSPD,WDIR'
header=np.vstack(np.array(header.split(","))).T

fin_mat1=np.concatenate([pre_mat,levs,temp,dtemp,rhum,wdir,wspd],axis=1)
fin_mat=np.concatenate([header,fin_mat1],axis=0)
## saving file
np.savetxt(outFile,fin_mat,fmt="%s",delimiter=',')

print("--- %s seconds ---" % (time.time() - start_time))
quit() 
