#/usr/bin/python


import netCDF4 as nf ; import numpy as np ; 
import matplotlib.pyplot as plt; #from pylab import savefig ;
from matplotlib.ticker import FixedLocator ; from mpl_toolkits.basemap import Basemap 


main='/home/vkvalappil/Data/modelWRF/input/' ; 

file_nc=main+'amsua_18.nc' ;

ncfile=nf.Dataset(file_nc,'r') ; 
lat=ncfile.variables['lat'][:]  ; lon=ncfile.variables['lon'][:] ; 
time=ncfile.variables['yyyymmddhhmmss'][:]    ;
sat_id=ncfile.variables['sat_id'][:]
sensor_id=ncfile.variables['sensor_id'][:]
lsh=ncfile.variables['land_surface_height'][:]
fov=ncfile.variables['field_of_view_number'][:]
zth=ncfile.variables['sat_zenith_angle'][:]
sza=ncfile.variables['solar_zenith_angle'][:]
saza=ncfile.variables['solar_azimuth_angle'][:]
laza=ncfile.variables['local_azimuth_angle'][:]
chn=ncfile.variables['channel_number'][:]
tb=ncfile.variables['tb'][:]
tb_mod=ncfile.variables['tb_model'][:]

tb[np.where(tb==9.9999998e+10)]=np.nan
lon1=lon[14::15] ; lat1=lat[14::15] ; tb1=tb[14::15]

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
llat=15 ; ulat=45 ; llon=25 ; ulon = 80 ;
m = Basemap( projection = 'cyl',llcrnrlon =llon , urcrnrlon = ulon,llcrnrlat = llat, urcrnrlat = ulat, resolution = 'l'  , suppress_ticks   = False)
#m = Basemap(projection='mill',llcrnrlat=llat,urcrnrlat=ulat,llcrnrlon=llon,urcrnrlon=ulon,resolution='l')
x, y = m(lon1, lat1)
cs=m.scatter(x, y, s=8.0, c=tb1, marker='o',edgecolor='none', cmap='RdYlBu_r')
m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8')
m.drawcoastlines(linewidth=0.7, color='black')
ax.xaxis.set_major_locator(FixedLocator(np.arange(llon, ulon+5, 5)))
ax.yaxis.set_major_locator(FixedLocator(np.arange(llat, ulat+5, 5)))

#ax.set_xticklabels(['180W', '120W', '60W', '0', '60E', '120E', '180E'])
#ax.set_yticklabels(['90S', '60S', '30S', 'EQ', '30N', '60N', '90N'])

#plt.colorbar(shrink=0.5)
plt.savefig('/home/vkvalappil/Data/modelWRF/input/TB_Distribution_amsua18.png')
plt.close()

