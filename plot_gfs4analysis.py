
import sys ; import numpy as np ; import scipy as sp ; import datetime ; import time
import pygrib as pg ; import scipy.ndimage

import matplotlib.pyplot as plt; #from pylab import * ; from matplotlib import *
from mpl_toolkits.basemap import Basemap   
from matplotlib.colors import from_levels_and_colors ;

#fnme='gfs_4_20160117_0600_000'  
#fnme='gfs_4_20160119_0600_000'  
#fnme='gfs_4_20160122_0600_018'  
#fnme='gfs_4_20160216_0600_000'  
#fnme='gfs_4_20160218_0600_018'  
#fnme='gfs_4_20160310_0600_000'
#fnme='gfs_4_20160119_0600_018'  
#fnme='gfs_4_20160215_0600_000'  
#fnme='gfs_4_20160216_0600_018'  
#fnme='gfs_4_20160220_0600_000'  
#fnme='gfs_4_20160310_0600_018'
#fnme='gfs_4_20160117_0600_018'  
#fnme='gfs_4_20160122_0600_000'  
#fnme='gfs_4_20160215_0600_018'  
#fnme='gfs_4_20160218_0600_000'  
#fnme='gfs_4_20160220_0600_018'

files=np.array(['gfs_4_20160117_0600_000','gfs_4_20160119_0600_000','gfs_4_20160122_0600_018','gfs_4_20160216_0600_000','gfs_4_20160218_0600_018',\
                'gfs_4_20160310_0600_000','gfs_4_20160119_0600_018','gfs_4_20160215_0600_000','gfs_4_20160216_0600_018','gfs_4_20160220_0600_000',\
                'gfs_4_20160310_0600_018','gfs_4_20160117_0600_018','gfs_4_20160122_0600_000','gfs_4_20160215_0600_018','gfs_4_20160218_0600_000',\
                'gfs_4_20160220_0600_018'])

for fnme in files:

    grb_f=pg.open('/home/masdar-fog/_SHARED_FOLDERS/gfs_data/EGU_paper/'+fnme+'.grb2')

    mslp=(np.array(grb_f.select(name="MSLP (Eta model reduction)")))
    #mslp=(np.array(grb_f.select(name="Surface pressure")))
    u=(np.array(grb_f.select(name="10 metre U wind component")))
    v=(np.array(grb_f.select(name="10 metre V wind component")))

    lat, lon=mslp[0].latlons()
    #ps=mslp[0].values/100 ; uwnd=u[0].values ; vwnd=v[0].values
    ps=scipy.ndimage.zoom(mslp[0].values/100,5)
    uwnd=scipy.ndimage.zoom(u[0].values,5) ; 
    vwnd=scipy.ndimage.zoom(v[0].values,5) ; 
 gaussian_filter(hght_500, sigma=5, order=0)
    grb_f.close()
    lat=scipy.ndimage.zoom(lat,5) ; lon=scipy.ndimage.zoom(lon,5) ; 


    fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) ; 
    m = Basemap(projection='mill',llcrnrlat=0,urcrnrlat=45,llcrnrlon=20,urcrnrlon=80,resolution='l')
    x, y=m(lon,lat) 
    nice_cmap=plt.get_cmap('ocean_r')
    #RdYlBu
    #nice_cmap= plt.get_cmap(mymap)
    #clevs=[14,17,20,23,26,29,32,35,38,41,44,47,50]

    clevs = np.arange(980,1040,4)
    cs =m.contour(x,y,ps,clevs,colors='k',linewidths=1.3,animated=True,alpha=0.9) 
    plt.clabel(cs, inline=1, fontsize=10,colors='k',fmt='%1.0f',inline_spacing=8,rightside_up=True, use_clabeltext=True)
    #m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8')
    #m.readshapefile('/home/vkvalappil/Data/EGU_paper/continents/continent','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8')
    skip=(slice(None,None,15),slice(None,None,15))
    #urot,vrot,xv,yv = m.rotate_vector(uwnd,vwnd,lon,lat,returnxy=True)
    #Q = m.quiver(x[skip],y[skip],uwnd[skip],vwnd[skip],units='xy',color='b',headwidth=10,headlength=25)
    #Q = m.quiver(xv[skip],yv[skip],urot[skip],vrot[skip],units='xy',color='b',headwidth=10,headlength=25)
    
    #qk = plt.quiverkey(Q, 0.95, 1.05, 25, '25 m/s', labelpos='W')
    
    #ua, va, xv, yv = m.transform_vector(g_uu,g_vv,lon1,lat1,lon1.shape[0],lon1.shape[0],returnxy=True)
    #m.barbs(x[skip],y[skip],uwnd[skip],vwnd[skip], length=7, color='k',)
    m.barbs(x[skip],y[skip],uwnd[skip],vwnd[skip],length=5,sizes=dict(emptybarb=0, spacing=0.05, height=0.5,length=3),barbcolor='k',alpha=0.6)

    m.drawparallels(np.arange(0.,50.,15.), labels=[1,0,0,0], linewidth=0.1)
    m.drawmeridians(np.arange(20.,85.,15.), labels=[0,0,0,1],linewidth=0.1)
    #m.drawmapboundary(fill_color='white') 
    m.drawcoastlines(linewidth=0.5,color='r') ; 
    #m.drawcountries(linewidth=0.5,color='r')
    # m.drawstates(linewidth=0.25)
    #cbar=m.colorbar(cs,location='right', pad='5%') ; cbar.set_ticks([clevs]) ; cbar.ax.tick_params(labelsize=8) 
    #(cbar.set_label('m/s')) ;
    #(plt.title('Average Temperature DJF ',fontsize=12,color='k')); 
    plt.savefig('/home/vkvalappil/Data/EGU_paper/'+fnme+'.png', dpi=100);
    plt.close()
#################################################################################################################################
