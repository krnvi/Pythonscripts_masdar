#!/usr/bin/python

import os ; import sys; import numpy as np ; import netCDF4 as nf ; import datetime as dt ;  
from scipy.interpolate import interp2d ; from dateutil import rrule, tz ; import wrf; import time


main='/home/vkvalappil/Data/modelWRF/' ; scripts=main+'/scripts/' ; output=main+'ARW/output/'
date=str(sys.argv[1]) ;  fcs_leaddays=1 ; #provide date as argument, forecast start and end date defined
fcs_st_date=dt.datetime.strptime(date,'%Y%m%d%H') ; fcs_ed_date=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=fcs_leaddays));  

file_date_list=[x.strftime('%Y-%m-%d_%H:%S:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)][::12] ;
tint=1 ; stim=0 ; etim=len(file_date_list)-1 ; #tmp.shape[0]-1 


files='/home/oceanColor/Fog/WRF_data_BE/'+date+'/wrfout_d02_'
#files=main+'ARW/wrf_output/'+date+'/wrfout_d02_' ; 
wrf_list=[nf.Dataset(files+ii) for ii in file_date_list[:]]

p_1 = wrf.getvar(wrf_list, "pres", timeidx=wrf.ALL_TIMES, method="cat")
u_1= wrf.getvar(wrf_list,"wspd_wdir",timeidx=wrf.ALL_TIMES,method="cat")
v_1= wrf.getvar(wrf_list,"va",timeidx=wrf.ALL_TIMES,method="cat")
tmp_1=wrf.getvar(wrf_list,"tk",timeidx=wrf.ALL_TIMES,method="cat")
rh_1=wrf.getvar(wrf_list,"rh",timeidx=wrf.ALL_TIMES,method="cat")
td_1=wrf.getvar(wrf_list,"td",timeidx=wrf.ALL_TIMES,method="cat",units='K')
qvap_1=wrf.getvar(wrf_list,"QVAPOR",timeidx=wrf.ALL_TIMES,method="cat")
qcld_1=wrf.getvar(wrf_list,"QCLOUD",timeidx=wrf.ALL_TIMES,method="cat")
qran_1=wrf.getvar(wrf_list,"QRAIN",timeidx=wrf.ALL_TIMES,method="cat")
thet_1=wrf.getvar(wrf_list,"theta",timeidx=wrf.ALL_TIMES,method="cat")
#cape=wrf.getvar(wrf_list,"cape_3d",timeidx=wrf.ALL_TIMES,method="cat")
hgt_1=wrf.getvar(wrf_list,"z",timeidx=wrf.ALL_TIMES,method="cat")
terhgt_1=wrf.getvar(wrf_list,"ter",timeidx=wrf.ALL_TIMES,method="cat")


lat=wrf.getvar(wrf_list,"lat",timeidx=wrf.ALL_TIMES,method="cat")
lon=wrf.getvar(wrf_list,"lon",timeidx=wrf.ALL_TIMES,method="cat")

#ws=np.sqrt(u*u+v*v)

#######################################################################################################################################

lstFle=main+'/scripts/master_uae.csv'  ; lst_f=np.genfromtxt(lstFle,delimiter=',', dtype="S") ; 
lst_f=lst_f[lst_f[:,0].argsort(kind='mergesort')]  ; points=lst_f[:,1:3].astype(float) ; noloc=points.shape[0] 
locs=np.vstack(lst_f[:,-1].T)

for tim_idx in range(0,p_1.shape[0])   :   #[00, 12, 24]  :
 
    p=p_1[tim_idx,:,:,:] ; tmp=tmp_1[tim_idx,:,:,:] ; rh=rh_1[tim_idx,:,:,:] ; td=td_1[tim_idx,:,:,:] ; qran=qran_1[tim_idx,:,:,:] ;  
    qvap=qvap_1[tim_idx,:,:,:] ; qcld=qcld_1[tim_idx,:,:,:] ; thet=thet_1[tim_idx,:,:,:] ; hgt=hgt_1[tim_idx,:,:,:] ; 
    terhgt=terhgt_1[0,:,:] ; ws=u_1[0,tim_idx,:,:,:] ; wd=u_1[1,tim_idx,:,:,:]
    
    dt=time.strftime("%Y%m%d%H", time.gmtime(p.datetime.data.astype(int)/1000000000))
    f_date=np.vstack(np.tile(dt,noloc*44)) ; 
    tloc=np.vstack(np.repeat(locs,44))  ; tid=np.vstack(np.repeat(lst_f[:,0],44))
    pre_mat=np.concatenate([tid,tloc,f_date],axis=1)
    
    x_y = wrf.ll_to_xy(wrf_list, points[:,0],points[:,1], as_int=True)
    
    pres=np.array([ p[:,i,k] for i,k in x_y.data.T]).T 
    temp=np.array([ tmp[:,i,k] for i,k in x_y.data.T]).T
    rhum=np.array([ rh[:,i,k] for i,k in x_y.data.T]).T          
    dtemp=np.array([ td[:,i,k] for i,k in x_y.data.T]).T      
    mrio=np.array([ qvap[:,i,k] for i,k in x_y.data.T]).T      
    theta=np.array([ thet[:,i,k] for i,k in x_y.data.T]).T      
    qcloud=np.array([ qcld[:,i,k] for i,k in x_y.data.T]).T                
    qrain=np.array([ qran[:,i,k] for i,k in x_y.data.T]).T            
    wspd=np.array([ ws[:,i,k] for i,k in x_y.data.T]).T
    wdir=np.array([ wd[:,i,k] for i,k in x_y.data.T]).T            
    thgt=np.array([ terhgt[i,k] for i,k in x_y.data.T]).T            
    mhgt=np.array([ hgt[:,i,k] for i,k in x_y.data.T]).T            
          
    pres=np.vstack(pres.flatten('F'))      
    temp=np.vstack(temp.flatten('F'))      
    rhum=np.vstack(rhum.flatten('F'))      
    dtemp=np.vstack(dtemp.flatten('F'))      
    mrio=np.vstack(mrio.flatten('F'))      
    theta=np.vstack(theta.flatten('F'))      
    qrain=np.vstack(qrain.flatten('F'))      
    qcloud=np.vstack(qcloud.flatten('F'))      
    wspd=np.vstack(wspd.flatten('F'))      
    wdir=np.vstack(wdir.flatten('F'))      
    thgt=np.vstack(thgt.flatten('F'))      
    mhgt=np.vstack(mhgt.flatten('F'))      
                 

    header='ID,LocName,Date(UTC),pressure,temperature,rel.Humidity,dew.Temp,mixRatio,pot.Temp,qrain,qcloud,wspd,wdir,mod.Height'
    header=np.vstack(np.array(header.split(","))).T

    fin_mat1=np.concatenate([pre_mat,pres,temp,rhum,dtemp,mrio,theta,qrain,qcloud,wspd,wdir, mhgt],axis=1)
    fin_mat=np.concatenate([header,fin_mat1],axis=0)
    ## saving file
    
    if not os.path.exists(output+date):
        os.makedirs(output+date)
    outFle=output+date+'/modelLevel_'+dt+'.csv'
    np.savetxt(outFle,fin_mat,fmt="%s",delimiter=',')          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
