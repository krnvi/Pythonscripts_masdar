import numpy as np ; import netCDF4 as nf ; import datetime as dt ;  


import matplotlib.pyplot as plt; from pylab import * ; from matplotlib import *
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, maskoceans, interp, shapefile
import pygrib as pg ; from matplotlib.colors import from_levels_and_colors ;
import matplotlib.colors as mcolors

dom='d02'
aster_file='/home/vkvalappil/Data/modelWRF/Domains/DEM/aster_dem/geo_em.'+dom+'.nc'
srtm_file='/home/vkvalappil/Data/modelWRF/Domains/DEM/srtm/geo_em.'+dom+'.nc'
gtopo_file='/home/vkvalappil/Data/modelWRF/Domains/DEM/opp_config_domain/geo_em.'+dom+'.nc'

srtm_f=nf.Dataset(srtm_file, mode='r')

lat=(np.squeeze(srtm_f.variables['CLAT'][:]))  ; lat1=np.vstack(lat[:,0]) ; 
lon=(np.squeeze(srtm_f.variables['CLONG'][:])) ; lon1=np.vstack(lon[0,:])
hgt_srtm=np.squeeze(srtm_f.variables['HGT_M'][:])

gtopo_f=nf.Dataset(gtopo_file, mode='r')
hgt_gtopo=np.squeeze(gtopo_f.variables['HGT_M'][:])

ast_f=nf.Dataset(aster_file, mode='r')
hgt_ast=np.squeeze(ast_f.variables['HGT_M'][:])

##########################################################################################################
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
#m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
m = Basemap(projection='lcc',lat_1=24,lat_0=24,lon_0=54,llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')

x, y=m(lon,lat) 


nice_cmap=plt.get_cmap('RdYlGn_r')


clevs=np.arange(hgt_srtm.min(),hgt_srtm.max(),200)
clevs=np.arange(-4200,4400,10)
       
#cs = (m.contourf(x,y,data,leves=clevs,cmap=cmap,norm=norml,extend='both'))
cs = (m.contourf(x,y,hgt_srtm,clevs,cmap=nice_cmap,extended='both')) 
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
(m.drawmapboundary(fill_color='white')) 
(m.drawcoastlines(linewidth=0.25)) ; 
(m.drawcountries(linewidth=0.25));
(m.drawstates(linewidth=0.25)) 

clevs=np.arange(-4200,4400,500)
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])
    #(cbar.set_label('m/s')) ;
(plt.title('SRTM 1 arc sec topographic height')); 
savefig('/home/vkvalappil/Data/modelWRF/Domains/DEM/srtm/geo_em.'+dom+'_HGT_M.png', dpi=100);
plt.close()
#####################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
#m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
m = Basemap(projection='lcc',lat_1=24,lat_0=24,lon_0=54,llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')

x, y=m(lon,lat) 

nice_cmap=plt.get_cmap('ocean_r')
nice_cmap=plt.get_cmap('RdYlGn_r')
#nice_cmap= plt.get_cmap(mymap)

clevs=np.arange(-4200,4400,10)
       
#cs = (m.contourf(x,y,data,leves=clevs,cmap=cmap,norm=norml,extend='both'))
cs = (m.contourf(x,y,hgt_ast,clevs,cmap=nice_cmap,extended='both')) 
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
(m.drawmapboundary(fill_color='white')) 
(m.drawcoastlines(linewidth=0.25)) ; 
(m.drawcountries(linewidth=0.25));
(m.drawstates(linewidth=0.25)) 

clevs=np.arange(-4200,4400,500)
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])
#(cbar.set_label('m/s')) ;
(plt.title('Aster 1 arc sec topographic height')); 
savefig('/home/vkvalappil/Data/modelWRF/Domains/DEM/aster_dem/geo_em.'+dom+'_HGT_M.png', dpi=100);
plt.close()

###########################################
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
#m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
m = Basemap(projection='lcc',lat_1=24,lat_0=24,lon_0=54,llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')

x, y=m(lon,lat) 

nice_cmap=plt.get_cmap('RdYlGn_r')


clevs=np.arange(-4200,4400,10)
       
cs = (m.contourf(x,y,hgt_gtopo,clevs,cmap=nice_cmap,extended='both')) 
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
(m.drawmapboundary(fill_color='white')) 
(m.drawcoastlines(linewidth=0.25)) ; 
(m.drawcountries(linewidth=0.25));
(m.drawstates(linewidth=0.25)) 

clevs=np.arange(-4200,4400,500)
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])

(plt.title('gtopo 30 arc sec topographic height')); 
savefig('/home/vkvalappil/Data/modelWRF/Domains/DEM/opp_config_domain/geo_em.'+dom+'_HGT_M.png', dpi=100);
plt.close()
######################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
#m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
m = Basemap(projection='lcc',lat_1=24,lat_0=24,lon_0=54,llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')

x, y=m(lon,lat) 


nice_cmap=plt.get_cmap('RdYlGn_r')


dif_hgt=(hgt_srtm-hgt_gtopo)

clevs=np.arange(dif_hgt.min(),dif_hgt.max()+100,10)
       
cs = (m.contourf(x,y,dif_hgt,clevs,cmap=nice_cmap,extended='both')) 
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
(m.drawmapboundary(fill_color='white')) 
(m.drawcoastlines(linewidth=0.25)) ; 
(m.drawcountries(linewidth=0.25));
(m.drawstates(linewidth=0.25))

clevs=np.arange(dif_hgt.min(),dif_hgt.max()+100,100)
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])
    #(cbar.set_label('m/s')) ;
(plt.title('difference SRTM and gtopo topographic height')); 
savefig('/home/vkvalappil/Data/modelWRF/Domains/DEM/srtm/srtm-gtopo_HGT_M'+dom+'.png', dpi=100);
plt.close()
###################################################################################################################

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
#m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
m = Basemap(projection='lcc',lat_1=24,lat_0=24,lon_0=54,llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')

x, y=m(lon,lat) 

nice_cmap=plt.get_cmap('ocean_r')
nice_cmap=plt.get_cmap('RdYlGn')
#nice_cmap= plt.get_cmap(mymap)

dif_hgt=(hgt_ast-hgt_gtopo)

clevs=np.arange(dif_hgt.min(),dif_hgt.max()+100,10)
       
#cs = (m.contourf(x,y,data,leves=clevs,cmap=cmap,norm=norml,extend='both'))
cs = (m.contourf(x,y,dif_hgt,clevs,cmap=nice_cmap,extended='both')) 
(m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
(m.drawmapboundary(fill_color='white')) 
(m.drawcoastlines(linewidth=0.25)) ; 
(m.drawcountries(linewidth=0.25));
(m.drawstates(linewidth=0.25)) 

clevs=np.arange(dif_hgt.min(),dif_hgt.max()+100,100)
cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs])
    #(cbar.set_label('m/s')) ;
(plt.title('difference Aster and gtopo topographic height')); 
savefig('/home/vkvalappil/Data/modelWRF/Domains/DEM/aster_dem/aster-gtopo_HGT_M'+dom+'.png', dpi=100);
plt.close()

######################################################






