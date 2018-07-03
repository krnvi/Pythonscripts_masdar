#!/usr/bin/python
import sys; import numpy as np ; import netCDF4 as nf ; import datetime as dt ;  
from scipy.interpolate import interp2d ; from dateutil import rrule, tz 

main='/home/OldData/modelWRF/NMMV3.7/' ; scripts=main+'/scripts/' ; output=main+'/output/'
date=str(sys.argv[1]) ;  fcs_leaddays=3 ; #provide date as argument, forecast start and end date defined
fcs_st_date=dt.datetime.strptime(date,'%Y%m%d%H') ; fcs_ed_date=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=fcs_leaddays));  

lstFle=main+'/scripts/master_uae.csv'  ; outFile=output+'hourly'+date+'_wrf.csv' ; 

# Reading data from lst file and model output files
lst_f=np.genfromtxt(lstFle,delimiter=',', dtype="S") ; lst_f=lst_f[lst_f[:,0].argsort(kind='mergesort')]  
points=lst_f[:,1:3].astype(float) ; noloc=points.shape[0] 

file_date_list=[x.strftime('%Y-%m-%d_%H:%S:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)] ; #forecast start and end datelist 


day_list=np.array(range(0,fcs_leaddays)) ; day_seq=np.vstack(np.tile(np.repeat(day_list,24),noloc)) 
tim_list=(np.array(range(06,24,1) + range(00,06,1))) ; tim_list=[str(k).rjust(2, '0')for k in tim_list] 
tim_seq=np.vstack(np.tile(tim_list,3*noloc)) ;
c_date=np.vstack(np.repeat(fcs_st_date.strftime('%Y-%m-%d'),noloc*72))

tint=1 ; stim=0 ; etim=len(file_date_list)-1 ; #tmp.shape[0]-1 

from_zone = tz.gettz('UTC') ; to_zone = tz.gettz('Asia/Dubai') ; 
date_list=[(x.replace(tzinfo=from_zone)).astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)]
date_list=date_list[0::tint] ; date_list=np.delete(date_list,-1) ; f_date=np.vstack(np.tile(date_list,noloc)) ; 
tid=np.vstack(np.repeat(lst_f[:,0],72))  ; pre_mat=np.concatenate([tid,c_date,tim_seq,f_date,day_seq],axis=1)

#time intervel, start time and end time defined. 

temp=np.empty((0,noloc)) ; mrio=np.empty((0,noloc)) ; spsf=np.empty((0,noloc)) ; uwnd=np.empty((0,noloc)) ; 
vwnd=np.empty((0,noloc)) ; vis=np.empty((0,noloc)) ; visd=np.empty((0,noloc)) ; cldf=np.empty((0,noloc)) ; 

for i in range(stim,etim):
    files=main+'/wrf_output/'+date+'/wrfout_d02_'+file_date_list[i]
    f=nf.Dataset(files, mode='r')
    lat=(np.squeeze(f.variables['XLAT'][:]))  ; lat1=np.vstack(lat[:,0]) ; 
    lon=(np.squeeze(f.variables['XLONG'][:])) ; lon1=np.vstack(lon[0,:])

    tmp=np.squeeze(f.variables['T2'][:])-273.15
    #rh=np.squeeze(f.variables['RH2'][:])
    MR=np.squeeze(f.variables['Q2'][:])
    ugrd=np.squeeze(f.variables['U10'][:])
    vgrd=np.squeeze(f.variables['V10'][:])
    PS=np.squeeze(f.variables['PSFC'][:])
#    VIS=np.squeeze(f.variables['AFWA_VIS'][:])
#    VISD=np.squeeze(f.variables['AFWA_VIS_DUST'][:])
#    CLD=np.squeeze(f.variables['AFWA_CLOUD'][:])
    VIS=np.squeeze(f.variables['FGDP'][:])
    VISD=np.squeeze(f.variables['VDFG'][:])
    CLD=np.squeeze(f.variables['DFGDP'][:])
    
    tmp_f=interp2d(lon1,lat1, tmp,kind='linear',copy=False,bounds_error=True ) ; 
    mrio_f=interp2d(lon1,lat1, MR,kind='linear',copy=False,bounds_error=True ) ; 
    ugrd_f=interp2d(lon1,lat1, ugrd,kind='linear',copy=False,bounds_error=True ) ; 
    vgrd_f=interp2d(lon1,lat1, vgrd,kind='linear',copy=False,bounds_error=True ) ; 
    spsf_f=interp2d(lon1,lat1, PS,kind='linear',copy=False,bounds_error=True ) ; 
    vis_f=interp2d(lon1,lat1, VIS,kind='linear',copy=False,bounds_error=True ) ; 
    visd_f=interp2d(lon1,lat1, VISD,kind='linear',copy=False,bounds_error=True ) ; 
    cld_f=interp2d(lon1,lat1, CLD,kind='linear',copy=False,bounds_error=True ) ; 

    temp=np.concatenate([temp,(np.array([tmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    mrio=np.concatenate([mrio,(np.array([mrio_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      
    uwnd=np.concatenate([uwnd,(np.array([ugrd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    vwnd=np.concatenate([vwnd,(np.array([vgrd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  
    spsf=np.concatenate([spsf,(np.array([spsf_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      
    vis=np.concatenate([vis,(np.array([vis_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      
    visd=np.concatenate([visd,(np.array([visd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      
    cldf=np.concatenate([cldf,(np.array([cld_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      
    
wdir=np.round(270-(np.arctan2(vwnd,uwnd))*(180/3.14)).astype(int)   ; wdir[wdir>360]=wdir[wdir>360]-360 
wspd=np.round(np.sqrt(np.square(uwnd)+np.square(vwnd))*3.6).astype(int) ; 

#### data is arranged in req format
temp=np.round(temp[0::tint]).astype(int) ; temp=np.vstack(temp.flatten('F'))
#temp=np.round(temp.reshape(fcs_leaddays,8,noloc)).astype(int) ;
spsf=np.round(spsf[0::tint]).astype(int) ; spsf=np.vstack(spsf.flatten('F'))
mrio=(mrio[0::tint]).astype(float)       ; mrio=np.vstack(mrio.flatten('F'))
wdir=np.round(wdir[0::tint]).astype(int) ; wdir=np.vstack(wdir.flatten('F'))
wspd=np.round(wspd[0::tint]).astype(int) ; wspd=np.vstack(wspd.flatten('F'))
vis=(vis[0::tint]).astype(float)   ; vis=np.vstack(vis.flatten('F'))
visd=(visd[0::tint]).astype(float) ; visd=np.vstack(visd.flatten('F'))
cldf=(vis[0::tint]).astype(float)  ; cldf=np.vstack(vis.flatten('F'))

header='TEHSILID,DATE,TIME(GMT),TIME(UAE),DAY_SEQUENCE,TEMP,DFGDP,MXRATIO,SURFPRES,WSPD,WDIR,FGDP,VDFG'
header=np.vstack(np.array(header.split(","))).T

fin_mat1=np.concatenate([pre_mat,temp,cldf,mrio,spsf,wspd,wdir,vis,visd],axis=1)
fin_mat=np.concatenate([header,fin_mat1],axis=0)
## saving file
np.savetxt(outFile,fin_mat,fmt="%s",delimiter=',')


quit()

