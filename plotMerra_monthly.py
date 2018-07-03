#!/usr/bin/python

import sys ; import numpy as np ; import datetime as dt ; import netCDF4 as nf ; 


import matplotlib.pyplot as plt; from pylab import * ; from matplotlib import *
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, maskoceans, interp, shapefile
import pygrib as pg ; from matplotlib.colors import from_levels_and_colors ;
import matplotlib.colors as mcolors

main='/home/vkvalappil/Data/GWR_paper/' ; 

file_dec_14=main+'MERRA2_400.instM_2d_asm_Nx.201412.SUB.nc4' ; file_jan_15=main+'MERRA2_400.instM_2d_asm_Nx.201501.SUB.nc4'
file_feb_15=main+'MERRA2_400.instM_2d_asm_Nx.201502.SUB.nc4' ; file_mar_15=main+'MERRA2_400.instM_2d_asm_Nx.201503.SUB.nc4'
file_apr_15=main+'MERRA2_400.instM_2d_asm_Nx.201504.SUB.nc4' ; file_may_15=main+'MERRA2_400.instM_2d_asm_Nx.201505.SUB.nc4'
file_jun_15=main+'MERRA2_400.instM_2d_asm_Nx.201506.SUB.nc4' ; file_jul_15=main+'MERRA2_400.instM_2d_asm_Nx.201507.SUB.nc4'
file_aug_15=main+'MERRA2_400.instM_2d_asm_Nx.201508.SUB.nc4' ; file_sep_15=main+'MERRA2_400.instM_2d_asm_Nx.201509.SUB.nc4'
file_oct_15=main+'MERRA2_400.instM_2d_asm_Nx.201510.SUB.nc4' ; file_nov_15=main+'MERRA2_400.instM_2d_asm_Nx.201511.SUB.nc4'

################################################################################################################################################

def read_data(file_name):
    ncfile=nf.Dataset(file_name,'r') ; 
    lat=ncfile.variables['lat'][:]  ; lon=ncfile.variables['lon'][:] ; 
    ps=ncfile.variables['PS'][:]    ; qv=ncfile.variables['QV2M'][:] ;
    tmp=ncfile.variables['T2M'][:]  ; u=ncfile.variables['U2M'][:]   ;
    v=ncfile.variables['V2M'][:]    ; 

    tgrad=(tmp-273.16)/(tmp-35.86) ; pres=379.90516/ps ; den=pres*np.exp(17.2693882*tgrad)
    rh=(qv/den)*100 ; rh[rh>100]=100
    ws=np.sqrt(np.square(u)+np.square(v)) ; 

    es=6.112*np.exp((17.67*(tmp-273.16)/((tmp-273.16)+243.15))) 
    #es=0.611*np.exp(17.2693882*tgrad)  ;   
    #e=qv*ps/0.622  
    e=es*(rh/100)
    td=np.log(e/6.112)*(243.5/(17.67-np.log(e/6.112)))
    #td=(243.5*np.log(e)-440.8)/(19.48-np.log(e))

    ncfile.close()
    return lat, lon, tmp, ws, rh,td
    
##############################################################################################################################################    
lat, lon, tmp_dec, ws_dec, rh_dec,td_dec=read_data(file_dec_14) ; lat, lon, tmp_jan, ws_jan, rh_jan,td_jan=read_data(file_jan_15)
lat, lon, tmp_feb, ws_feb, rh_feb,td_feb=read_data(file_feb_15)

lat, lon, tmp_mar, ws_mar, rh_mar,td_mar=read_data(file_mar_15) ; lat, lon, tmp_apr, ws_apr, rh_apr,td_apr=read_data(file_apr_15)
lat, lon, tmp_may, ws_may, rh_may,td_may=read_data(file_may_15)

lat, lon, tmp_jun, ws_jun, rh_jun,td_jun=read_data(file_jun_15) ; lat, lon, tmp_jul, ws_jul, rh_jul,td_jul=read_data(file_jul_15)
lat, lon, tmp_aug, ws_aug, rh_aug,td_aug=read_data(file_aug_15)

lat, lon, tmp_sep, ws_sep, rh_sep,td_sep=read_data(file_sep_15) ; lat, lon, tmp_oct, ws_oct, rh_oct,td_oct=read_data(file_oct_15)
lat, lon, tmp_nov, ws_nov, rh_nov,td_nov=read_data(file_nov_15)


avg_tmp_djf=((tmp_dec+tmp_jan+tmp_feb)/3)-273.16 ; avg_ws_djf=(ws_dec+ws_jan+ws_feb)/3 ; avg_rh_djf=(rh_dec+rh_jan+rh_feb)/3 ;

avg_tmp_mam=((tmp_mar+tmp_apr+tmp_may)/3)-273.16 ; avg_ws_mam=(ws_mar+ws_apr+ws_may)/3 ; avg_rh_mam=(rh_mar+rh_apr+rh_may)/3

avg_tmp_jja=((tmp_jun+tmp_jul+tmp_aug)/3)-273.16 ; avg_ws_jja=(ws_jun+ws_jul+ws_aug)/3 ; avg_rh_jja=(rh_jun+rh_jul+rh_aug)/3 ;

avg_tmp_son=((tmp_sep+tmp_oct+tmp_nov)/3)-273.16 ; avg_ws_son=(ws_sep+ws_oct+ws_nov)/3 ; avg_rh_son=(rh_sep+rh_oct+rh_nov)/3 ;

avg_td_djf=(td_dec+td_jan+td_feb)/3 ; avg_td_mam=(td_mar+td_apr+td_may)/3 ; avg_td_jja=(td_jun+td_jul+td_aug)/3 ; 
avg_td_son=(td_sep+td_oct+td_nov)/3 ; 


lonn,latt=np.meshgrid(lon,lat) ; #avg_tmp_djf.min()

##################################################### Plot Data ###############################################################################
############### Temperature ##########

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26]
#clevs=[14,17,20,23,26,29,32,35,38,41,44,47,50]
cs = (m.contourf(x,y,avg_tmp_djf[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Temperature DJF ',fontsize=12,color='k')); 
plt.savefig(main+'avg_temp_djf.png', dpi=100);
plt.close()
##########################################################
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
clevs=[24,24.5,25,25.5,26,26.5,27,27.5,28,28.5,29,29.5,30,30.5,31,31.5,32,32.5,33]
cs = (m.contourf(x,y,avg_tmp_mam[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Temperature MAM ',fontsize=12,color='k')); 
plt.savefig(main+'avg_temp_mam.png', dpi=100);
plt.close()
#############################################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
clevs=[32,32.5,33,33.5,34,34.5,35,35.5,36,36.5,37,37.5,38,38.5,39,39.5,40,41]
cs = (m.contourf(x,y,avg_tmp_jja[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Temperature JJA ',fontsize=12,color='k')); 
plt.savefig(main+'avg_temp_jja.png', dpi=100);
plt.close()
######################################################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
#clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]
clevs=[28,28.5,29,29.5,30,30.5,31,31.5,32,32.5,33,33.5,34]
cs = (m.contourf(x,y,avg_tmp_son[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Temperature SON ',fontsize=12,color='k')); 
plt.savefig(main+'avg_temp_son.png', dpi=100);
plt.close()
#############################################################################################################

###################################### WIND SPEED ############################################################
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('PuOr_r')
#nice_cmap= plt.get_cmap(mymap)
#clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]
clevs=[0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4]
cs = (m.contourf(x,y,avg_ws_djf[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Wind Speed DJF ',fontsize=12,color='k')); 
plt.savefig(main+'avg_wspd_djf.png', dpi=100);
plt.close()
##############################################################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('PuOr_r')
#nice_cmap= plt.get_cmap(mymap)
#clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]
clevs=[0,1,1.5,2,2.5,3,3.5,4]
clevs=[0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4]
cs = (m.contourf(x,y,avg_ws_mam[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])  ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Wind Speed MAM ',fontsize=12,color='k')); 
plt.savefig(main+'avg_wspd_mam.png', dpi=100);
plt.close()

#################################################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('PuOr_r')
#nice_cmap= plt.get_cmap(mymap)
#clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]
clevs=[0,1,1.5,2,2.5,3,3.5,4]
clevs=[0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4]

cs = (m.contourf(x,y,avg_ws_jja[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])  ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Wind Speed JJA ',fontsize=12,color='k')); 
plt.savefig(main+'avg_wspd_jja.png', dpi=100);
plt.close()

##############################################################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('PuOr_r')
#nice_cmap= plt.get_cmap(mymap)
#clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]
clevs=[0,0.5,1,1.5,2,2.5,3,3.5,4]
clevs=[0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4]

cs = (m.contourf(x,y,avg_ws_son[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Wind Speed SON ',fontsize=12,color='k')); 
plt.savefig(main+'avg_wspd_son.png', dpi=100);
plt.close()

###################################################### Relative Humidity     ###############################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
#clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]
clevs=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
cs = (m.contourf(x,y,avg_rh_djf[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Relative Humidity DJF ',fontsize=12,color='k')); 
plt.savefig(main+'avg_rh_djf.png', dpi=100);
plt.close()
########################################################################################
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
#clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]
clevs=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
cs = (m.contourf(x,y,avg_rh_mam[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Relative Humidity MAM ',fontsize=12,color='k')); 
plt.savefig(main+'avg_rh_mam.png', dpi=100);
plt.close()
########################################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
#clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]
clevs=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
cs = (m.contourf(x,y,avg_rh_jja[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Relative Humidity JJA ',fontsize=12,color='k')); 
plt.savefig(main+'avg_rh_jja.png', dpi=100);
plt.close()
########################################################################################
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
#clevs=[17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27]
clevs=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
cs = (m.contourf(x,y,avg_rh_son[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Relative Humidity SON ',fontsize=12,color='k')); 
plt.savefig(main+'avg_rh_son.png', dpi=100);
plt.close()
########################################################################################

############################################## dew point temperature #######################################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
clevs=[-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
cs = (m.contourf(x,y,avg_td_djf[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Relative Humidity SON ',fontsize=12,color='k')); 
plt.savefig(main+'avg_td_djf.png', dpi=100);
plt.close()

######################################################################################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
clevs=[-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
cs = (m.contourf(x,y,avg_td_mam[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Relative Humidity SON ',fontsize=12,color='k')); 
plt.savefig(main+'avg_td_mam.png', dpi=100);
plt.close()

######################################################################################################################################
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
clevs=[-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
cs = (m.contourf(x,y,avg_td_jja[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Relative Humidity SON ',fontsize=12,color='k')); 
plt.savefig(main+'avg_td_jja.png', dpi=100);
plt.close()

######################################################################################################################################
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=22.0,urcrnrlat=26.5,llcrnrlon=51,urcrnrlon=57,resolution='l')
x, y=m(lonn,latt) 
nice_cmap=plt.get_cmap('RdYlBu_r')
#nice_cmap= plt.get_cmap(mymap)
clevs=[-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]
cs = (m.contourf(x,y,avg_td_son[0,:,:],clevs,cmap=nice_cmap,extended='both')) 
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/domain_d02_4km_WRFChem_small','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/shp_UAE/ADMIN_domain_d01_4km_WRFChem','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
#m.drawparallels(np.arange(22.,27.,2.), labels=[1,0,0,0])
#m.drawmeridians(np.arange(51.,57.,3.), labels=[0,0,0,1])
#(m.drawmapboundary(fill_color='white')) 
#(m.drawcoastlines(linewidth=0.25)) ; 
#(m.drawcountries(linewidth=0.25));
#(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=16) 
#(cbar.set_label('m/s')) ;
#(plt.title('Average Relative Humidity SON ',fontsize=12,color='k')); 
plt.savefig(main+'avg_td_son.png', dpi=100);
plt.close()

######################################################################################################################################

















































