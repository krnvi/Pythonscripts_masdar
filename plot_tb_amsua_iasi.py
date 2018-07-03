#/usr/bin/python


import netCDF4 as nf ; import numpy as np ; 
import matplotlib.pyplot as plt; #from pylab import savefig ;
from matplotlib.ticker import FixedLocator ; from mpl_toolkits.basemap import Basemap 


main='/home/vkvalappil/Data/modelWRF/input/' ; 

file_nc_i=main+'iasi_18.nc' ;

ncfile_i=nf.Dataset(file_nc_i,'r') ; 
lat_i=ncfile_i.variables['lat'][:]  ; lon_i=ncfile_i.variables['lon'][:]   #[0::616] ; 
#time=ncfile.variables['yyyymmddhhmmss'][:]    ;
#sat_id=ncfile.variables['sat_id'][:]
#sensor_id=ncfile.variables['sensor_id'][:]
#lsh=ncfile.variables['land_surface_height'][:]
#fov=ncfile.variables['field_of_view_number'][:]
#zth=ncfile.variables['sat_zenith_angle'][:]
#sza=ncfile.variables['solar_zenith_angle'][:]
#saza=ncfile.variables['solar_azimuth_angle'][:]
#laza=ncfile.variables['local_azimuth_angle'][:]
#chn_i=ncfile_i.variables['channel_number'][:][0::616] 
#tb_i=ncfile_i.variables['tb'][:][0::616]
#tb_mod=ncfile.variables['tb_model'][:]

#tb_i[np.where(tb_i==9.9999998e+10)]=np.nan
#lon1=lon[1::616] ; lat1=lat[1::616] ; tb1=tb[1::616] ; chn1=chn[1::616]
ncfile_i.close()
file_nc=main+'amsua_06.nc' ;
ncfile=nf.Dataset(file_nc,'r') ; 
lat=ncfile.variables['lat'][:]  ; lon=ncfile.variables['lon'][:] ; 
chn=ncfile.variables['channel_number'][:]
tb=ncfile.variables['tb'][:]
ncfile.close()


tb[np.where(tb==9.9999998e+10)]=np.nan
lon1=lon[14::15] ; lat1=lat[14::15] ; tb1=tb[14::15]
skip=(slice(5),slice(5))
fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
llat=15 ; ulat=45 ; llon=25 ; ulon = 80 ;
#m = Basemap( projection = 'cyl',llcrnrlon =llon , urcrnrlon = ulon,llcrnrlat = llat, urcrnrlat = ulat, resolution = 'l'  , suppress_ticks   = False)
m = Basemap(projection='mill',llcrnrlat=llat,urcrnrlat=ulat,llcrnrlon=llon,urcrnrlon=ulon,resolution='l')
x, y = m(lon1, lat1)
cs=m.scatter(x, y, s=3.0, c='r', marker='o', edgecolor='none',alpha=1.0)

x1, y1 = m(lon_i, lat_i)
cs=m.scatter(x1, y1, s=2.0, c='b', marker='D',edgecolor='none',alpha=0.7)

m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8')
m.drawcoastlines(linewidth=0.7, color='black')
#ax.xaxis.set_major_locator(FixedLocator(np.arange(llon, ulon+5, 5)))
#ax.yaxis.set_major_locator(FixedLocator(np.arange(llat, ulat+5, 5)))


m.drawparallels(np.arange(llat,ulat+10,15), labels=[1,0,0,0])
m.drawmeridians(np.arange(llon,ulon+10,15.), labels=[0,0,0,1])
#m.drawmapboundary(fill_color='white'
m.drawcoastlines(linewidth=0.25) ; 
#m.drawcountries(linewidth=0.25);
#m.drawstates(linewidth=0.25)


#ax.set_xticklabels(['180W', '120W', '60W', '0', '60E', '120E', '180E'])
#ax.set_yticklabels(['90S', '60S', '30S', 'EQ', '30N', '60N', '90N'])

#plt.colorbar(shrink=0.5)
plt.savefig('/home/vkvalappil/Data/modelWRF/input/TB_Distribution_amsua_iasi06_18.png')
#plt.close()



