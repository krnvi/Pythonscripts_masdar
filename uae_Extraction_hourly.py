#!/usr/bin/python
############################## National 3Hourly Data Extraction ##################################################################
#importing necessary modules
import sys ; import numpy as np ; import scipy as sp ; from scipy.interpolate import interp2d ; import datetime as dt
from scipy.interpolate import griddata ; import datetime ; import time ; from dateutil import rrule, tz ; import netCDF4 as nf ; 

start_time = time.time()
#### path and input files are defined
main='/home/vkvalappil/Data/modelWRF/' ; scripts=main+'/scripts/' ; output='/home/vkvalappil/Data/oppModel/ARW/output/'
date=str(sys.argv[1]) ; fcs_leaddays=3 ; 
fcs_st_date=dt.datetime.strptime(date,'%Y%m%d%H') ; fcs_ed_date=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=fcs_leaddays));

lstFle='/home/vkvalappil/Data/oppModel/scripts/master_uae2.csv'
#modFile='/research/cesam/vineeth/modelWRF/ARW/wrf_output/'+date+'/wrfpost_d02.'+date+'.nc'
modFile='/home/oceanColor/Fog/WRFmodel_forecast/wrfouput_weatherforcast/Archivewrffogmaskwithbackground/wrfpost_'+date+'.nc'
outFile=output+'hourly'+date+'.csv' ; 

############ Required data is read from the wrf output
lst_f=np.genfromtxt(lstFle,delimiter=',', dtype="S") ; lst_f=lst_f[lst_f[:,0].argsort(kind='mergesort')]  
points=lst_f[:,1:3].astype(float) ; noloc=points.shape[0] 

nc_file=nf.Dataset(modFile,'r')
lat=nc_file.variables['lat'][:]    ; lon=nc_file.variables['lon'][:]
tmp=nc_file.variables['T_2m'][:]   ; RH=nc_file.variables['rh_2m'][:]
dtmp=nc_file.variables['Td_2m'][:] ; SH=nc_file.variables['q_2m'][:]
MR=nc_file.variables['r_v_2m'][:]  ; PS=nc_file.variables['p_sfc'][:]
ugrd=nc_file.variables['u_10m_tr'][:] ; vgrd=nc_file.variables['v_10m_tr'][:]
nc_file.close()

stim=0 ; etim=72 ; tint=1
day_list=np.array(range(0,fcs_leaddays)) ; day_seq=np.vstack(np.tile(np.repeat(day_list,24),noloc)) 
#####  date day seq and time are arranged in req format #######################
tim_st=dt.datetime.strptime(date,'%Y%m%d%H') ; tim_ed=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=1)
tim_list=[x.strftime('%H') for x in rrule.rrule(rrule.HOURLY,dtstart=tim_st,until=tim_ed)][0:-1]

#tim_list=(np.array(range(06,24,1) + range(00,06,1))) ; 

tim_list=[str(k).rjust(2, '0')for k in tim_list] 

tim_seq=np.vstack(np.tile(tim_list,3*noloc)) ;
c_date=np.vstack(np.repeat(fcs_st_date.strftime('%Y-%m-%d'),noloc*72))

from_zone = tz.gettz('UTC') ; to_zone = tz.gettz('Asia/Dubai') ; 
date_list=[(x.replace(tzinfo=from_zone)).astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)]
date_list=date_list[0::tint] ; date_list=np.delete(date_list,-1) ; f_date=np.vstack(np.tile(date_list,noloc)) ; 
tid=np.vstack(np.repeat(lst_f[:,0],72))  ; pre_mat=np.concatenate([tid,c_date,tim_seq,f_date,day_seq],axis=1)

lon=np.vstack(lon[0,:]) ; lat=np.vstack(lat[:,0]) ; #lat=lat[::-1] 
temp=np.empty((0,noloc)) ; rhum=np.empty((0,noloc)) ; shum=np.empty((0,noloc)) ; cldfrn=np.empty((0,noloc)) ; 
mrio=np.empty((0,noloc)) ; spsf=np.empty((0,noloc)) ; uwnd=np.empty((0,noloc)) ; vwnd=np.empty((0,noloc)) ; dtemp=np.empty((0,noloc))
###### Interpolating to each location 
for i in range(stim,etim):
    tmp_f=interp2d(lon,lat, tmp[i],kind='linear',copy=False,bounds_error=True ) ; 
    dtmp_f=interp2d(lon,lat, dtmp[i],kind='linear',copy=False,bounds_error=True ) ; 
    #lcdc1=LCDClcl[i].data() ; mcdc1=MCDCmcl[i].data() ; hcdc1=HCDChcl[i].data()
    #cldfrn1=((lcdc1[0]+mcdc1[0]+hcdc1[0])*8)/300
    #cldfrn_f=interp2d(lon,lat, cldfrn1,kind='linear',copy=False,bounds_error=True ) ;    
    rhum_f=interp2d(lon,lat, RH[i],kind='linear',copy=False,bounds_error=True ) ;  
    shum_f=interp2d(lon,lat,SH[i],kind='linear',copy=False,bounds_error=True ) ;  
    mrio_f=interp2d(lon,lat,MR[i],kind='linear',copy=False,bounds_error=True) ;    
    spsf_f=interp2d(lon,lat,PS[i],kind='linear',copy=False,bounds_error=True) ;    
    ugrd_f=interp2d(lon,lat, ugrd[i],kind='linear',copy=False,bounds_error=True ) ;     
    vgrd_f=interp2d(lon,lat, vgrd[i],kind='linear',copy=False,bounds_error=True ) ; 
    
    temp=np.concatenate([temp,(np.array([tmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    dtemp=np.concatenate([dtemp,(np.array([dtmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    cldfrn=np.concatenate([cldfrn,(np.array([dtmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  
    rhum=np.concatenate([rhum,(np.array([rhum_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  
    shum=np.concatenate([shum,(np.array([shum_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      
    spsf=np.concatenate([spsf,(np.array([spsf_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      
    mrio=np.concatenate([mrio,(np.array([mrio_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      
    uwnd=np.concatenate([uwnd,(np.array([ugrd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    vwnd=np.concatenate([vwnd,(np.array([vgrd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  

wdir=np.round(270-(np.arctan2(vwnd,uwnd))*(180/3.14)).astype(int)   ; wdir[wdir>360]=wdir[wdir>360]-360 
wspd=np.round(np.sqrt(np.square(uwnd)+np.square(vwnd))*3.6).astype(int) ; 

#### data is arranged in req format
temp=np.round(temp[0::tint]).astype(int) ; temp=np.vstack(temp.flatten('F'))
#temp=np.round(temp.reshape(fcs_leaddays,8,noloc)).astype(int) ;
dtemp=np.round(dtemp[0::tint]).astype(int) ; dtemp=np.vstack(dtemp.flatten('F'))
rhum=np.round(rhum[0::tint]).astype(int) ; rhum=np.vstack(rhum.flatten('F'))
#rhum=np.round(rhum.reshape(fcs_leaddays,tint,noloc)).astype(int) ;
shum=(shum[0::tint]).astype(float) ; shum=np.vstack(shum.flatten('F'))
spsf=np.round(spsf[0::tint]).astype(int) ; spsf=np.vstack(spsf.flatten('F'))
mrio=(mrio[0::tint]).astype(float) ; mrio=np.vstack(mrio.flatten('F'))
wdir=np.round(wdir[0::tint]).astype(int) ; wdir=np.vstack(wdir.flatten('F'))
wspd=np.round(wspd[0::tint]).astype(int) ; wspd=np.vstack(wspd.flatten('F'))

cldfrn=(cldfrn.reshape(72,tint,noloc)) ;  
meancld=cldfrn.mean(axis=1) ; meancld[meancld>8]=8 ; meancld[(meancld>0.1) & (meancld<0.6)]=1  ; 
meancld=np.round(meancld).astype(int) ; meancld=np.vstack(meancld.flatten('F'))


header='TEHSILID,DATE,TIME(GMT),localTime,DAY_SEQUENCE,TEMP,DTEMP,RH,CLOUD,SPHUM,MXRATIO,SURFPRES,WSPD,WDIR'
header=np.vstack(np.array(header.split(","))).T

fin_mat1=np.concatenate([pre_mat,temp,dtemp,rhum,meancld,shum,mrio,spsf,wdir,wspd],axis=1)
fin_mat=np.concatenate([header,fin_mat1],axis=0)
## saving file
np.savetxt(outFile,fin_mat,fmt="%s",delimiter=',')

print("--- %s seconds ---" % (time.time() - start_time))
quit() 
