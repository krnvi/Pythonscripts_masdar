from osgeo import gdal
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

wrf_out_file ='/home/OldData/modelWRF/NMMV3.7/wrf_output/2016021906/wrfout_d02_2016-02-19_12:00:00'


ds_lon = gdal.Open('NETCDF:"'+wrf_out_file+'":XLONG')
ds_lat = gdal.Open('NETCDF:"'+wrf_out_file+'":XLAT')
ds_t2 = gdal.Open('NETCDF:"'+wrf_out_file+'":T2')

lon1=ds_lon.ReadAsArray() ; lat1=ds_lat.ReadAsArray() ; temp1=ds_t2.ReadAsArray()-273.15

map = Basemap(llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),projection='lcc', lat_1=21.,lat_2=27.,lat_0=27,lon_0=54.)
#map = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')

x, y = map(lon,lat)

cs=map.contourf(x, y,temp ) 
map.readshapefile('/home/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8')
map.drawcoastlines()
cbar=map.colorbar(cs,location='right', pad='5%') 
plt.savefig('/home/OldData/modelWRF/NMMV3.7/wrf_output/2016021906/temp.png', dpi=100);

plt.show()


