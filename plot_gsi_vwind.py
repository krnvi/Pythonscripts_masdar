#!/usr/bin/python

import numpy as np ; import netCDF4 as nf ; import datetime as dt ;  
from dateutil import rrule ; from scipy.interpolate import interp2d  
import matplotlib.pyplot as plt; from pylab import * ; from matplotlib import *
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, maskoceans, interp, shapefile
import pygrib as pg ; from matplotlib.colors import from_levels_and_colors ;
import matplotlib.colors as mcolors

gsi_file='/home/vkvalappil/Data/modelWRF/GSI/gsiout/2016122006_hybrid_02/wrf_inout'
wrf_file='/home/vkvalappil/Data/modelWRF/GSI/gsiout/2016122006_hybrid_02/wrfinput_d02'

gsi_f=nf.Dataset(gsi_file, mode='r')

lat=(np.squeeze(gsi_f.variables['XLAT'][:]))  ; lat1=np.vstack(lat[:,0]) ; 
lon=(np.squeeze(gsi_f.variables['XLONG'][:])) ; lon1=np.vstack(lon[0,:])

wrf_f=nf.Dataset(wrf_file, mode='r')
g_v_s=np.squeeze(gsi_f.variables['V'][:])  ; g_v=0.5*(g_v_s[:,:-1,:] + g_v_s[:,1:,:])  #destager according  NCL
w_v_s=np.squeeze(wrf_f.variables['V'][:])  ; w_v=0.5*(w_v_s[:,:-1,:] + w_v_s[:,1:,:])
d_v=g_v.mean(axis=0)-w_v.mean(axis=0)    ; 
for lev in range(0,44):
    lev_1=lev+1
    g_vv=g_v[lev,:,:] ;  w_vv=w_v[lev,:,:] ; d_vv=g_vv-w_vv ; 
############################################################################################################################################
    fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
    m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
    lons, data = m.shiftdata(lon, datain=g_vv, lon_0=None)
    x, y=m(lon,lat) 

    nice_cmap=plt.get_cmap('ocean_r')
    nice_cmap=plt.get_cmap('RdYlGn')
    #nice_cmap= plt.get_cmap(mymap)
    #clevs=[-15,-10,-5,-0,5,10,15,20,25,30,35,40,45,50,55,60,70]
    clevs=[-9,-6,-3,-0,3,6,9,12,15,18,21,24,27,30,33,36,39]
         
    #cs = (m.contourf(x,y,data,leves=clevs,cmap=cmap,norm=norml,extend='both'))
    cs = (m.contourf(x,y,data,clevs,cmap=nice_cmap,extended='both')) 
    (m.readshapefile('/home/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
    m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
    m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
    (m.drawmapboundary(fill_color='white')) 
    (m.drawcoastlines(linewidth=0.25)) ; 
    (m.drawcountries(linewidth=0.25));
    (m.drawstates(linewidth=0.25)) 
    cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])
    #(cbar.set_label('m/s')) ;
    (plt.title('GSI V wind at model level '+ str(lev_1),fontsize=12,color='k')); 
    savefig('/home/vkvalappil/Data/modelWRF/GSI/gsiout/2016122006_hybrid_02/vwind/vwind_gsi_'+str(lev_1)+'.png', dpi=100);
    plt.close()
###################################################################################################################################
    fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
    m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
    lons, data = m.shiftdata(lon, datain=w_vv, lon_0=None)
    x, y=m(lon,lat) 

    nice_cmap=plt.get_cmap('ocean_r')
    nice_cmap=plt.get_cmap('RdYlGn')
    #nice_cmap= plt.get_cmap(mymap)
    #clevs=[-15,-10,-5,-0,5,10,15,20,25,30,35,40,45,50,55,60,70]
    clevs=[-9,-6,-3,-0,3,6,9,12,15,18,21,24,27,30,33,36,39]
    #cs = (m.contourf(x,y,data,leves=clevs,cmap=cmap,norm=norml,extend='both'))
    cs = (m.contourf(x,y,data,clevs,cmap=nice_cmap,extended='both')) 
    (m.readshapefile('/home/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
    m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
    m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
    (m.drawmapboundary(fill_color='white')) 
    (m.drawcoastlines(linewidth=0.25)) ; 
    (m.drawcountries(linewidth=0.25));
    (m.drawstates(linewidth=0.25)) 
    cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])
    #(cbar.set_label('m/s')) ;
    (plt.title('WRF V wind at model level '+ str(lev_1),fontsize=12,color='k')); 
    savefig('/home/vkvalappil/Data/modelWRF/GSI/gsiout/2016122006_hybrid_02/vwind/vwind_wrf_'+str(lev_1)+'.png', dpi=100);
    plt.close()  
#########################################################################################################################################    
    fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
    m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
    lons, data = m.shiftdata(lon, datain=d_vv, lon_0=None)
    x, y=m(lon,lat) 


    mymap = mcolors.ListedColormap(['white','lime','limegreen','greenyellow','yellow','gold','orange','indianred','firebrick', \
                                'darkred','lightskyblue','deepskyblue','royalblue','blue'])    
    nice_cmap= plt.get_cmap(mymap)
    clevs=[-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8]    
    colors = nice_cmap([13,12,11,10,0,0,1, 2, 3, 4])
    cmap, norm = from_levels_and_colors(clevs, colors, extend='both')
#    #cs=m.pcolormesh(x,y,data, cmap=cmap, norm=norm)
    norml = mcolors.BoundaryNorm(clevs, ncolors=cmap.N, clip=True)

    cs = (m.contourf(x,y,data,clevs,cmap=cmap,norm=norm,extend='both'))
    #cs = (m.contourf(x,y,data,clevs,cmap=cmap,extended='both')) 
    (m.readshapefile('/home/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
    m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
    m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
    (m.drawmapboundary(fill_color='white')) 
    (m.drawcoastlines(linewidth=0.25)) ; 
    (m.drawcountries(linewidth=0.25));
    (m.drawstates(linewidth=0.25)) 
    cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])
    #(cbar.set_label('m/s')) ;
    (plt.title('DIF V wind at model level '+ str(lev_1),fontsize=12,color='k')); 
    savefig('/home/vkvalappil/Data/modelWRF/GSI/gsiout/2016122006_hybrid_02/vwind/vwind_dif_'+str(lev_1)+'.png', dpi=100);
    plt.close()      
#########################################################################################################################################################################    
    
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
lons, data = m.shiftdata(lon, datain=d_v, lon_0=None)
x, y=m(lon,lat) 


mymap = mcolors.ListedColormap(['white','lime','limegreen','greenyellow','yellow','gold','orange','indianred','firebrick', \
                                'darkred','lightskyblue','deepskyblue','royalblue','blue'])    
nice_cmap= plt.get_cmap(mymap)
clevs=[-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8]    
 
colors = nice_cmap([13,12,11,10,0,0,1, 2, 3, 4])
cmap, norm = from_levels_and_colors(clevs, colors, extend='both')
#    #cs=m.pcolormesh(x,y,data, cmap=cmap, norm=norm)
norml = mcolors.BoundaryNorm(clevs, ncolors=cmap.N, clip=True)

cs = (m.contourf(x,y,data,clevs,cmap=cmap,norm=norm,extend='both'))
#cs = (m.contourf(x,y,data,clevs,cmap=cmap,extended='both')) 
(m.readshapefile('/home/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
(m.drawmapboundary(fill_color='white')) 
(m.drawcoastlines(linewidth=0.25)) ; 
(m.drawcountries(linewidth=0.25));
(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])
#(cbar.set_label('m/s')) ;
(plt.title('DIF V wind at all model level ',fontsize=12,color='k')); 
savefig('/home/vkvalappil/Data/modelWRF/GSI/gsiout/2016122006_hybrid_02/vwind/vwind_adif_.png', dpi=100);
plt.close()       
    
   
#########################################################################################################################################   
    