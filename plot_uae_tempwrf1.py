import numpy as np ; import netCDF4 as nf ; import datetime as dt ;  
from dateutil import rrule ; from scipy.interpolate import interp2d  
import matplotlib.pyplot as plt; from pylab import * ; from matplotlib import *
from mpl_toolkits.basemap import Basemap, cm, shiftgrid, maskoceans, interp, shapefile
import pygrib as pg ; from matplotlib.colors import from_levels_and_colors ;
import matplotlib.colors as mcolors

files='/home/OldData/modelWRF/NMMV3.7/wrf_output/2016021906/wrfout_d02_2016-02-19_12:00:00'
f=nf.Dataset(files, mode='r')
lat=(np.squeeze(f.variables['XLAT'][:]))  ; lat1=np.vstack(lat[:,0]) ; 
lon=(np.squeeze(f.variables['XLONG'][:])) ; lon1=np.vstack(lon[0,:])
temp=np.squeeze(f.variables['T2'][:])-273.15

fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
lons, data = m.shiftdata(lon, datain=temp, lon_0=None)
x, y=m(lon,lat)
#Z=maskoceans(lons,lat,data,inlands=True, resolution='c', grid=2.5)
clevs=[1, 5, 10, 15 ,18, 21 ,22, 23, 24, 25, 26 , 27, 28] ; 
mymap = mcolors.ListedColormap(['white','lime','limegreen','greenyellow','yellow','gold','orange','indianred','firebrick', \
                                'darkred','lightskyblue','deepskyblue','royalblue','blue']) 

#    colors1 = plt.get_cmap('ocean_r')  ; colors1=colors1(np.linspace(0., 1, 128))
#    colors2 = plt.get_cmap('RdYlGn') ; colors2=colors2(np.linspace(0.,1 , 128))
#    colors = np.vstack(( colors1,colors2))
#    mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)    
    

nice_cmap= plt.get_cmap(mymap)
colors = nice_cmap([0,1, 2, 3, 4, 5,6,7,8,9,10,11,12,13]) 
cmap, norm = from_levels_and_colors(clevs, colors, extend='both') 
#    #cs=m.pcolormesh(x,y,data, cmap=cmap, norm=norm)
norml = mcolors.BoundaryNorm(clevs, ncolors=cmap.N, clip=True)

#cs = (m.contourf(x,y,data,leves=clevs,cmap=cmap,norm=norml,extend='both'))
cs = (m.contourf(x,y,data)) 
#(m.readshapefile('/home/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8'))
m.drawparallels(np.arange(20.,30.,5.), labels=[1,0,0,0])
m.drawmeridians(np.arange(50.,60.,5.), labels=[0,0,0,1])
(m.drawmapboundary(fill_color='white')) 
(m.drawcoastlines(linewidth=0.25)) ; 
(m.drawcountries(linewidth=0.25));
(m.drawstates(linewidth=0.25)) 
cbar=m.colorbar(cs,location='right', pad='5%') ; #cbar.set_ticks([clevs])
(cbar.set_label('degC')) ;
(plt.title('temperature',fontsize=12,color='k')); 
savefig('/home/OldData/modelWRF/NMMV3.7/wrf_output/2016021906/temp1.png', dpi=100);
   
    
    
    
    
    
    