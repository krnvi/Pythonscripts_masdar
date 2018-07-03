#/usr/bin/python

import os ; import sys; import numpy as np ; import netCDF4 as nf ; import datetime as dt ;  
from scipy.interpolate import interp2d ; from dateutil import rrule, tz ; import wrf

#from matplotlib.cm import get_cmap ; import cartopy.crs as crs
#from cartopy.feature import NaturalEarthFeature, LAND,OCEAN 

import matplotlib.pyplot as plt ; from mpl_toolkits.basemap import  maskoceans ; import matplotlib.colors as mcolors

main='/home/vkvalappil/Data/modelWRF/' ; scripts=main+'/scripts/' ; output=main+'ARW/output/'

date=str(sys.argv[1]) ;  fcs_leaddays=3 ; #provide date as argument, forecast start and end date defined




fcs_st_date=dt.datetime.strptime(date,'%Y%m%d%H') ; fcs_ed_date=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=fcs_leaddays));  

file_date_list=[x.strftime('%Y-%m-%d_%H:%S:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)] ;
tint=1 ; stim=0 ; etim=len(file_date_list)-1 ; #tmp.shape[0]-1 


###########################################################################################################

svp1=0.6112 ; svp2=17.67 ; svp3=29.65 ; svpt0=273.15 ; r_d=287. ; r_v=461.6 ; ep_2=r_d/r_v  ; ep_3=0.622

COEFLC = 144.7 ; COEFLP = 2.24 ; COEFFC = 327.8 ; COEFFP = 10.36 ; EXPLC  = 0.88
EXPLP  = 0.75 ; EXPFC  = 1. ; EXPFP  = 0.7776


###############################################################################################################

files=main+'ARW/wrf_output/'+date+'/wrfout_d02_' ; 
wrf_list=[nf.Dataset(files+ii) for ii in file_date_list[:]]

p = wrf.getvar(wrf_list, "pres", timeidx=wrf.ALL_TIMES, method="cat")
u= wrf.getvar(wrf_list,"ua",timeidx=wrf.ALL_TIMES,method="cat")
v= wrf.getvar(wrf_list,"va",timeidx=wrf.ALL_TIMES,method="cat")
tmp=wrf.getvar(wrf_list,"tk",timeidx=wrf.ALL_TIMES,method="cat")
rh=wrf.getvar(wrf_list,"rh",timeidx=wrf.ALL_TIMES,method="cat")
td=wrf.getvar(wrf_list,"td",timeidx=wrf.ALL_TIMES,method="cat",units='K')
qvap=wrf.getvar(wrf_list,"QVAPOR",timeidx=wrf.ALL_TIMES,method="cat")
qcld=wrf.getvar(wrf_list,"QCLOUD",timeidx=wrf.ALL_TIMES,method="cat")
qran=wrf.getvar(wrf_list,"QRAIN",timeidx=wrf.ALL_TIMES,method="cat")
lat=wrf.getvar(wrf_list,"lat",timeidx=wrf.ALL_TIMES,method="cat")
lon=wrf.getvar(wrf_list,"lon",timeidx=wrf.ALL_TIMES,method="cat")
tmp_v=wrf.getvar(wrf_list,"tv",timeidx=wrf.ALL_TIMES,method="cat")

cil=wrf.getvar(wrf_list,"AFWA_CLOUD_CEIL",timeidx=wrf.ALL_TIMES,method="cat") 
cfr=wrf.getvar(wrf_list,"AFWA_CLOUD",timeidx=wrf.ALL_TIMES,method="cat")
af_vis=wrf.getvar(wrf_list,"AFWA_VIS",timeidx=wrf.ALL_TIMES,method="cat")

ws=np.sqrt(u*u+v*v)

p=p[:,0,:,:] ; tmp=tmp[:,0,:,:] ; rh=rh[:,0,:,:] ; td=td[:,0,:,:] ; qran=qran[:,0,:,:] ;  tmp_v=tmp_v[:,0,:,:] ; 
qvap=qvap[:,0,:,:] ; qcld=qcld[:,0,:,:] ; ws=ws[:,0,:,:] #rh1=rh[:,0,:,:] ; rh2=rh[:,1,:,:] ; drh=np.fmax(rh1,rh2)

td1           = np.where(td.data>tmp.data,tmp.data,td.data)
#############################################################################################################################


rhoa = p/(r_d*tmp_v) # Air density [kg m^-3]
rhow = 1e3       # Water density [kg m^-3]
rhoi = 0.917e3   # Ice density [kg m^-3]

vovmd = (1+qvap)/rhoa + (qcld+qran)/rhow  
conc_lc = 1e3*qcld/vovmd ; conc_lp = 1e3*qran/vovmd
# Make sure all concentrations are positive
conc_lc.data[conc_lc.data < 0] = 0 ; conc_lp.data[conc_lp.data < 0] = 0
betav = COEFLC*conc_lc**EXPLC + COEFLP*conc_lp**EXPLP+1E-10
vis_upp = -np.log(0.02)/betav ; vis_upp.data[vis_upp.data >10]=10

##3##################################################################
af_vis=af_vis/1000 ; af_vis.data[af_vis.data >10]=10
cil=cil/1000

###############################################################################################################################

vis_ruc=np.empty((rh.shape)) ; 
indx1=np.where(rh.data<50) ;  indx2=np.where((rh.data >=50) & (rh.data <=85)) ; 
indx3=np.where((rh.data >85) & (rh.data <=100))

#indx1=rh.where(rh<50) ; indx2=rh.where((rh>=50) & (rh <=85)) ; indx3=rh.where((rh>85) & (rh <=100))

vis_ruc[indx1]=60*np.exp(-2.5*((rh.data[indx1]-15)/80))  
vis_ruc[indx2]=50*np.exp(-2.5*((rh.data[indx2]-10)/85))  
vis_ruc[indx3]=50*np.exp(-2.5*((rh.data[indx3]-15)/85))  
vis_ruc[vis_ruc>10]=10


#vis_ruc1=60*np.exp(-2.5*((rh-15)/80))          

vis_fsl=6000*1.609344*((tmp-td1)/rh**1.75)    

vis_fsl.data[vis_fsl.data>10]=10 
#vis_aml=29190.39-(162.96*ws)-(908.59*(tmp-td1))-272.06*rh ; vis_aml=vis_aml/1000
vis_avg=(vis_ruc+vis_upp.data)/2

############################################# Visibility Liquid water content and droplets concentration #####################

a=(qcld+qran)/rhow
a=(((qcld.data+qran.data)*500)**0.6473)
vis_lwc=1.02/a




################################################################################################################################

#vis_upp.to_netcdf(files+'visibility_upp_'+file_date_list[0],'w')
#vis_ruc.to_netcdf(files+'visibility_ruc_'+file_date_list[0],'w')
#vis_fsl.to_netcdf(files+'visibility_fsl_'+file_date_list[0],'w')

#for ii in range(0,vis_ruc.shape[0]):
#    fig = plt.figure(figsize=(12,9))
#    cart_proj =wrf.get_cartopy(tmp)  #crs.PlateCarree()
#    ax = plt.axes(projection=cart_proj) 
#    vis=vis_fsl  ; 
#    lats, lons = wrf.latlon_coords(vis)
#    states = NaturalEarthFeature(category='cultural', scale='50m', facecolor='none',
#                             name='admin_1_states_provinces_shp')
#    ax.add_feature(states, linewidth=.5)
#    #ax.add_feature(OCEAN, zorder=100, edgecolor='b')
#    ax.coastlines('50m', linewidth=0.8)
#
#    clevs=[1,2,3,4,5,6,7,8,9,10]
#
#    # Make the contour outlines and filled contours for the smoothed sea level pressure.
#    plt.contour(wrf.to_np(lons), wrf.to_np(lats), wrf.to_np(vis)[ii,:,:],clevs, colors="black",
#            transform=crs.PlateCarree())
#    plt.contourf(wrf.to_np(lons), wrf.to_np(lats), wrf.to_np(vis)[ii,:,:], clevs, transform=crs.PlateCarree(),
#             cmap=get_cmap("jet"))
#
#    # Add a color bar
#    plt.colorbar(ax=ax, shrink=.62)
#
#    # Set the map limits.  Not really necessary, but used for demonstration.
#    ax.set_xlim(wrf.cartopy_xlim(tmp))
#    ax.set_ylim(wrf.cartopy_ylim(tmp))
#
#    # Add the gridlines
#    ax.gridlines(color="black", linestyle="dotted",draw_labels=False,linewidth=0.7, alpha=1)
#
#    plt.title("Visibility (FSL method)",fontsize=12,color='k')
#    fileName=main+'ARW/wrf_output/'+date+'/plots/wrfout_d02_'
#    plt.savefig(fileName+'visibility_fsl_'+file_date_list[ii]+'.png',dpi=100)   

vis=vis_avg ; 
for ii in range(0,vis.shape[0]):
    fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) 
    #lats, lons = wrf.latlon_coords(vis)

    lons=np.array(wrf.to_np(lon.data[0,:,:])) ; lats=np.array(wrf.to_np(lat.data[0,:,:]))
    #lons=lons[0,:]; lats=lats[:,0]
    #lons,lats=np.meshgrid(lons,lats)
    #m =Basemap(projection='mill',llcrnrlat=lats.min(),urcrnrlat=lats.max(),llcrnrlon=lons.min(),urcrnrlon=lons.max(),resolution='l') #wrf.get_basemap(vis)

    m = wrf.get_basemap(tmp) ;     x, y = m(wrf.to_np(lons), wrf.to_np(lats))
    Z=maskoceans(lons,lats,wrf.to_np(vis)[ii,:,:],inlands=False)#, resolution='c', grid=2.5)
    #Z=wrf.to_np(vis)[ii,:,:]
    #nice_cmap=plt.get_cmap('RdYlGn_r') ;     
    clevs=[0,1,2,3,4,5,6,7,8,9,10]    
    
    #['white 0 ','lime 1','limegreen 2','greenyellow 3','yellow 4','gold 5','orange 6','indianred 7',
    #'firebrick 8', 'darkred 9','lightskyblue 10','deepskyblue 11','royalblue 12 ','blue 13']
    
    mymap = mcolors.ListedColormap(['white','ghostwhite','floralwhite','greenyellow','yellow','gold','orange','indianred','firebrick', \
                                'darkred','lightskyblue','deepskyblue','royalblue','blue'])    
    nice_cmap= plt.get_cmap(mymap)
    #colors = nice_cmap([0,1, 2, 3, 4, 5,6,7,8,9,10,11,12,13])
    colors = nice_cmap([13,11,12,9,8,7,6,4,3,2,0,1])

    cmap, norm = mcolors.from_levels_and_colors(clevs, colors, extend='both')
    norml = mcolors.BoundaryNorm(clevs, ncolors=cmap.N, clip=True)

    
    #m.contour(x, y, wrf.to_np(vis)[ii,:,:], 10, colors="black")
    cs=m.contourf(x, y,Z , levels=clevs,cmap=cmap,norm=norml,extended='both')

    m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8')
    #m.drawlsmask(land_color='0.8',ocean_color='w',lsmask=True)
    #m.drawlsmask(land_color=(0, 0, 0, 0), ocean_color='deeppink', lakes=True)
    m.drawcoastlines(linewidth=0.25,ax=ax) ; m.drawcountries(linewidth=0.25,ax=ax) ; m.drawstates(linewidth=0.25,ax=ax)     

    parallels = np.arange(np.amin(lats), np.amax(lats), 2.5) ; m.drawparallels(parallels, ax=ax, color="k", labels=[1,0,0,0]) 
    merids = np.arange(np.amin(lons), np.amax(lons), 2.5)    ; m.drawmeridians(merids, ax=ax, color="k", labels=[0,0,0,1])
    #m.drawmapboundary(fill_color='white') ; 
    #plt.colorbar(shrink=.62) location='right', pad='5%')
    
    cbar=m.colorbar(cs,location='right', pad='5%') ;  cbar.set_ticks([clevs])
    ax.set_title("visibility (avg method) "+ file_date_list[ii], {"fontsize" : 12, "color": 'k'})

    #plt.title("Visibility (FSL method)",fontsize=12,color='k')
    fileName='/home/vkvalappil/Data/oppModel/wrf_output/'+date
    plt.savefig(fileName+'/visibility_avg_'+file_date_list[ii]+'.png',dpi=100) 
    plt.close()



############################################################################################################################
lstFle=main+'/scripts/master_uae.csv'  ; outFle=main+'ARW/wrf_output/'+date+'/plots/visibility_'+date+'.csv'
lst_f=np.genfromtxt(lstFle,delimiter=',', dtype="S") ; lst_f=lst_f[lst_f[:,0].argsort(kind='mergesort')]  
points=lst_f[:,1:3].astype(float) ; noloc=points.shape[0] 

#x_y = wrf.ll_to_xy(wrf_list[0], points[:,0],points[:,1], as_int=True)

day_list=np.array(range(0,fcs_leaddays)) ; day_seq=np.vstack(np.tile(np.repeat(day_list,24),noloc)) 
tim_list=(np.array(range(06,24,1) + range(00,06,1))) ; tim_list=[str(k).rjust(2, '0')for k in tim_list] 
tim_seq=np.vstack(np.tile(tim_list,3*noloc)) ;
c_date=np.vstack(np.repeat(fcs_st_date.strftime('%Y-%m-%d'),noloc*72))

from_zone = tz.gettz('UTC') ; to_zone = tz.gettz('Asia/Dubai') ; 
date_list=[(xx.replace(tzinfo=from_zone)).astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S') for xx in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)]
date_list=date_list[0::tint] ; date_list=np.delete(date_list,-1) ; f_date=np.vstack(np.tile(date_list,noloc)) ; 
tid=np.vstack(np.repeat(lst_f[:,0],72))  ; pre_mat=np.concatenate([tid,c_date,tim_seq,f_date,day_seq],axis=1)


lat1=np.vstack(lat[0,:,0]) ; lon1=np.vstack(lon[0,0,:])  
vis_1=np.empty((0,noloc)) ; vis_2=np.empty((0,noloc)) ;    vis_3=np.empty((0,noloc)) ; vis_4=np.empty((0,noloc)) ;
vis_5=np.empty((0,noloc)) ; cld_cil=np.empty((0,noloc)) ; cld_cfr=np.empty((0,noloc)) ;
for i in range(0,(vis_upp.shape[0]-1)) :
    vis_1_f=interp2d(lon1,lat1, vis_upp.data[i,:,:],kind='linear',copy=False,bounds_error=True ) ;    
    vis_2_f=interp2d(lon1,lat1, vis_ruc[i,:,:],kind='linear',copy=False,bounds_error=True ) ;    
    vis_3_f=interp2d(lon1,lat1, vis_fsl.data[i,:,:],kind='linear',copy=False,bounds_error=True ) ;    
    vis_4_f=interp2d(lon1,lat1, vis_avg[i,:,:],kind='linear',copy=False,bounds_error=True ) ;    
    vis_5_f=interp2d(lon1,lat1, af_vis.data[i,:,:],kind='linear',copy=False,bounds_error=True ) ;    
    cfr_f=interp2d(lon1,lat1, cfr.data[i,:,:],kind='linear',copy=False,bounds_error=True ) ;    
    cil_f=interp2d(lon1,lat1, cil.data[i,:,:],kind='linear',copy=False,bounds_error=True ) ;    
    
    
    vis_1=np.concatenate([vis_1,(np.array([vis_1_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    vis_2=np.concatenate([vis_2,(np.array([vis_2_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    vis_3=np.concatenate([vis_3,(np.array([vis_3_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    vis_4=np.concatenate([vis_4,(np.array([vis_4_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)

    vis_5=np.concatenate([vis_5,(np.array([vis_5_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    cld_cil=np.concatenate([cld_cil,(np.array([cil_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    cld_cfr=np.concatenate([cld_cfr,(np.array([cfr_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)

    
vis_1=np.round(vis_1[0::tint]).astype(int) ; vis_1=np.vstack(vis_1.flatten('F'))
vis_2=np.round(vis_2[0::tint]).astype(int) ; vis_2=np.vstack(vis_2.flatten('F'))
vis_3=np.round(vis_3[0::tint]).astype(int) ; vis_3=np.vstack(vis_3.flatten('F'))
vis_4=np.round(vis_4[0::tint]).astype(int) ; vis_4=np.vstack(vis_4.flatten('F'))

vis_5=np.round(vis_5[0::tint]).astype(int) ; vis_5=np.vstack(vis_5.flatten('F'))
cld_cfr=(cld_cfr[0::tint]) ; cld_cfr=np.vstack(cld_cfr.flatten('F'))
cld_cil=np.round(cld_cil[0::tint]).astype(int) ; cld_cil=np.vstack(cld_cil.flatten('F'))

   
header='TEHSILID,DATE,TIME(GMT),TIME(UAE),DAY_SEQUENCE,VIS_UPP,VIS_RUC,VIS_FSL,VIS_avg,vis_awfa,cldfr,ceiling'
header=np.vstack(np.array(header.split(","))).T

fin_mat1=np.concatenate([pre_mat,vis_1,vis_2,vis_3,vis_4,vis_5,cld_cfr,cld_cil],axis=1)
fin_mat=np.concatenate([header,fin_mat1],axis=0)
## saving file
np.savetxt(outFle,fin_mat,fmt="%s",delimiter=',')



    
    