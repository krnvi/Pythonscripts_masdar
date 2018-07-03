#!/usr/bin/python

import sys ; import numpy as np ; import datetime as dt ; from scipy.interpolate import interp2d
import netCDF4 as nf ; from pytz import timezone  ; from dateutil import rrule, tz

############################################### Defining location, files ############################################################

main='/home/vkvalappil/Data/' ; scripts=main+'oppModel/scripts/' ; output=main+'oppModel/output/'
inp='/home/oceanColor/Fog/WRFmodel_forecast/wrfouput_weatherforcast/Archivenetcdf/' ; 

date=str(sys.argv[1]) ; fcs_leaddays=3 ;
fcs_st_date=dt.datetime.strptime(date,'%Y%m%d%H') ; fcs_ed_date=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=fcs_leaddays));



outFle=output+'hourly_opp'+date+'.csv'; lstFle=scripts+'master_uae.csv'
wndFle=inp+'windspeed_'+date+'.nc';uwndFle=inp+'windUcomp_'+date+'.nc';vwndFle=inp+'windVcomp_'+date+'.nc'
tmpFle=inp+'AirTemperature_'+date+'.nc' ; rhFle=inp+'Relativehumidity_'+date+'.nc' 
dtmpFle=inp+'dewpointTemperature_'+date+'.nc'

ncfile=nf.Dataset(wndFle,'r') ; 
lat=ncfile.variables['lat'][:] ; lon=ncfile.variables['lon'][:] ; 
wspd=ncfile.variables['wspeed'][:] ; tim=ncfile.variables['time'][:] ;tim_unit=ncfile.variables['time'].units
ncfile.close()

ncfile=nf.Dataset(rhFle,'r') ; rh=ncfile.variables['relhum'][:] ;  ncfile.close()
ncfile=nf.Dataset(uwndFle,'r') ; uwnd=ncfile.variables['u10m'][:] ; ncfile.close()
ncfile=nf.Dataset(vwndFle,'r') ; vwnd=ncfile.variables['v10m'][:] ; ncfile.close()
ncfile=nf.Dataset(tmpFle,'r') ; temp=ncfile.variables['airtemp'][:] ; ncfile.close()
ncfile=nf.Dataset(dtmpFle,'r') ; dtmp=ncfile.variables['dewptemp'][:] ; ncfile.close()


lst_f=np.genfromtxt(lstFle,delimiter=',', dtype="S") ; lst_f=lst_f[lst_f[:,0].argsort(kind='mergesort')]  
points=lst_f[:,1:3].astype(float) ; noloc=points.shape[0] 

 
day_list=np.array(range(0,fcs_leaddays)) ; day_seq=np.vstack(np.tile(np.repeat(day_list,24),noloc)) 
#####  date day seq and time are arranged in req format #######################
tim_list=(np.array(range(06,24,1) + range(00,06,1))) ; tim_list=[str(k).rjust(2, '0')for k in tim_list] 
tim_seq=np.vstack(np.tile(tim_list,3*noloc)) ;
c_date=np.vstack(np.repeat(fcs_st_date.strftime('%Y-%m-%d'),noloc*72))

stim=0 ; etim=72 ; tint=1

from_zone = tz.gettz('UTC') ; to_zone = tz.gettz('Asia/Dubai') ; 
date_list=[(x.replace(tzinfo=from_zone)).astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)]
date_list=date_list[0::tint] ; date_list=np.delete(date_list,-1) ; f_date=np.vstack(np.tile(date_list,noloc)) ; 
tid=np.vstack(np.repeat(lst_f[:,0],72))  ; pre_mat=np.concatenate([tid,c_date,tim_seq,f_date,day_seq],axis=1)


ws=np.empty((0,noloc)) ; u=np.empty((0,noloc)) ; v=np.empty((0,noloc)) ; visib=np.empty((0,noloc)) ; tmp=np.empty((0,noloc))
rhum=np.empty((0,noloc)) ; dtp=np.empty((0,noloc))
for i in range(stim,etim):
    wspd_f=interp2d(lon,lat, wspd[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    uwnd_f=interp2d(lon,lat, uwnd[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    vwnd_f=interp2d(lon,lat, vwnd[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    rh_f=interp2d(lon,lat, rh[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    temp_f=interp2d(lon,lat, temp[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    dtemp_f=interp2d(lon,lat, dtmp[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    
    ws=np.concatenate([ws,(np.array([wspd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    u=np.concatenate([u,(np.array([uwnd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    v=np.concatenate([v,(np.array([vwnd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    rhum=np.concatenate([rhum,(np.array([rh_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    tmp=np.concatenate([tmp,(np.array([temp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    dtp=np.concatenate([dtp,(np.array([dtemp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    
    
wdir=np.round(270-(np.arctan2(v,u))*(180/3.14)).astype(int)   ; wdir[wdir>360]=wdir[wdir>360]-360 
ws=np.round(np.sqrt(np.square(u)+np.square(v))*3.6).astype(int) ; 

#### data is arranged in req format
tmp=np.round(tmp[0::tint]).astype(int)  ; tmp=np.vstack(tmp.flatten('F'))
dtp=np.round(dtp[0::tint]).astype(int)   ; dtp=np.vstack(dtp.flatten('F'))
rhum=np.round(rhum[0::tint]).astype(int) ; rhum=np.vstack(rhum.flatten('F'))
wdir=np.round(wdir[0::tint]).astype(int) ; wdir=np.vstack(wdir.flatten('F'))
ws=np.round(ws[0::tint]).astype(int) ; ws=np.vstack(ws.flatten('F'))

header='TEHSILID,DATE,TIME(GMT),GST,DAY_SEQUENCE,TEMP,DTEMP,RH,WSPD,WDIR'
header=np.vstack(np.array(header.split(","))).T

fin_mat1=np.concatenate([pre_mat,tmp,dtp,rhum,wdir,ws],axis=1)
fin_mat=np.concatenate([header,fin_mat1],axis=0)
## saving file
np.savetxt(outFle,fin_mat,fmt="%s",delimiter=',')



















    