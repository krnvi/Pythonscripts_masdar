
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
g_u_s=np.squeeze(gsi_f.variables['U'][:])  ; g_u=0.5*(g_u_s[:,:,:-1] + g_u_s[:,:,1:])  #destager according  NCL
w_u_s=np.squeeze(wrf_f.variables['U'][:])  ; w_u=0.5*(w_u_s[:,:,:-1] + w_u_s[:,:,1:])

g_v_s=np.squeeze(gsi_f.variables['V'][:])  ; g_v=0.5*(g_v_s[:,:-1,:] + g_v_s[:,1:,:])  #destager according  NCL
w_v_s=np.squeeze(wrf_f.variables['V'][:])  ; w_v=0.5*(w_v_s[:,:-1,:] + w_v_s[:,1:,:])


g_vv=g_v[1,:,:] ;  w_vv=w_v[1,:,:] ;  
g_uu=g_u[1,:,:] ;  w_uu=w_u[1,:,:] ;  


fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
m = Basemap(projection='mill',llcrnrlat=lat.min(),urcrnrlat=lat.max(),llcrnrlon=lon.min(),urcrnrlon=lon.max(),resolution='l')
x, y=m(lon,lat)    

nice_cmap=plt.get_cmap('RdYlGn')

skip=(slice(None,None,5),slice(None,None,5))
ua, va, xv, yv = m.transform_vector(g_uu,g_vv,lon1,lat1,lon1.shape[0],lon1.shape[0],returnxy=True)
m.barbs(xv[skip],yv[skip],ua[skip],va[skip],cmap=nice_cmap,length=5,sizes=dict(emptybarb=0.25, spacing=0.05, height=0.5),barbcolor='b',flagcolor='r')




 # ,barbcolor='r',linewidth=0.5)















