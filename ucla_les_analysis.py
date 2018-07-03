#!/usr/bin/python


import os ; import numpy as np ; import netCDF4 as nf ; import datetime as dt ;  from dateutil import rrule ; import pandas as pd ; 

import matplotlib.pyplot as plt; from pylab import savefig ;  from matplotlib import cm ; import matplotlib.colors as mcolors
#########################################################################


les_file='/home/vkvalappil/Data/modelWRF/LES/UCLALES-SALSA/bin/2017122200/2017122200.ps.nc'

nc_f=nf.Dataset(les_file)

tim=nc_f.variables['time'][:] ; 
#tim_unit=nc_f.variables['time'].units #date_list=[d.strftime('%Y%m%d%H') for d in nf.num2date(tim,units = tim_unit)] ; 

z=nc_f.variables['zm'][:]
#x=nc_f.variables['xt'][:]  ;  y=nc_f.variables['yt'][:]
u0=nc_f.variables['u0'][:] ; v0=nc_f.variables['v0'][:]
dn0=nc_f.variables['dn0'][:] 
#ftim=nc_f.variales['fsttm'][:] ; ltim=nc_f.variales['lsttm'][:]

theta=nc_f.variables['theta'][:] ; pres=nc_f.variables['p'][:]
tot_mrio=nc_f.variables['q'][:] ; lqd_mrio=nc_f.variables['l'][:]
rflx=nc_f.variables['rflx'][:]
#cdnc=nc_f.variales['Nc'][:]
#cwmr=nc_f.variales['P_rl'][:]
#wvmr=nc_f.variales['P_rv'][:]
p_rh=nc_f.variables['P_RH'][:] 
u=nc_f.variables['u'][:] ; v=nc_f.variables['v'][:] ; #w=nc_f.variables['w'][:] ; 


year=2017; month=12 ; day=22
date_list=[ (dt.datetime(year,month,day,int(d % (24 * 3600)//3600),int((d % 3600)//60),int(d%60))).strftime('%Y-%m-%d %H:%M:%S') for d in tim ] ;  

#time = 120.133644
#day = int(time // (24 * 3600))
#time = time % (24 * 3600)
#hour = int(time // 3600)
#time %= 3600
#minutes = int(time // 60)
#time %= 60
#seconds = int(time)
#print("d:h:m:s-> %d:%d:%d:%d" % (day, hour, minutes, seconds))
#(dt.datetime(year,month,day,int(time % (24 * 3600)//3600),int((time % 3600)//60),int(time%60))).strftime('%Y-%m-%d %H:%M:%S')




########### Theta  
vert_prof=theta       
fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
x =np.arange(0,vert_prof[:,:].shape[0],1) ;   y = np.arange(0,vert_prof[:,:].shape[1])
X, Y = np.meshgrid(x, y)

clevs=np.arange(vert_prof.min()-1,vert_prof.max()+1,2)        #colors1 = plt.cm.binary(np.linspace(0., 1, 128))
colors2 = plt.cm.Blues(np.linspace(0., 1, 128))
colors3 = plt.cm.Reds(np.linspace(0, 1, 128))

# combine them and build a new colormap
colors = np.vstack((colors2,colors3))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
cs =plt.contourf(X,Y,vert_prof.T,levels=clevs,cmap=mymap)
#cs =plt.contourf(X,Y,vert_prof.T,cmap=mymap) 
#plt.clabel(cs1, inline=1, fontsize=16)
cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; #cbar.ax.invert_yaxis()

ax.set_xticks(x[::7]) ; 
xTickMarks=date_list[::7]
xtickNames = ax.set_xticklabels(xTickMarks)            
plt.setp(xtickNames, rotation=90, fontsize=12,family='sans-serif')
            
ax.set_yticks(y[::5]) ; 
yTickMarks=z[::5]
ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Potential Temperature'
plt.title(titl,color='black',fontsize=18,y=1.05)                             
plt.tight_layout(h_pad=3) ; 

outpath='/home/vkvalappil/Data/modelWRF/LES/UCLALES-SALSA/bin/2017122200/'
if not os.path.exists(outpath+'/FogAnalysis/'):
        os.makedirs(outpath+'/FogAnalysis/')

outFile=outpath+'/FogAnalysis/theta_vertical_profile.png'
savefig(outFile);
plt.close(fig) ; fig.clf(fig)  

###########################################################################################################
p_rh[p_rh>100]=100
vert_prof=p_rh       
fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
x =np.arange(0,vert_prof[:,:].shape[0],1) ;   y = np.arange(0,vert_prof[:,:].shape[1])
X, Y = np.meshgrid(x, y)

clevs=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,82,84,86,88,90,92,94,96,98,100]        #colors1 = plt.cm.binary(np.linspace(0., 1, 128))
colors2 = plt.cm.Blues(np.linspace(0., 1, 128))
colors3 = plt.cm.Reds(np.linspace(0, 1, 128))

# combine them and build a new colormap
colors = np.vstack((colors2,colors3))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
cs =plt.contourf(X,Y,vert_prof.T,levels=clevs,cmap=mymap)
#cs =plt.contourf(X,Y,vert_prof.T,cmap=mymap) 
#plt.clabel(cs1, inline=1, fontsize=16)
cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; #cbar.ax.invert_yaxis()

ax.set_xticks(x[::7]) ; 
xTickMarks=date_list[::7]
xtickNames = ax.set_xticklabels(xTickMarks)            
plt.setp(xtickNames, rotation=90, fontsize=12,family='sans-serif')
            
ax.set_yticks(y[::5]) ; 
yTickMarks=z[::5]
ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Relative Humidity'
plt.title(titl,color='black',fontsize=18,y=1.05)                             
plt.tight_layout(h_pad=3) ; 
outpath='/home/vkvalappil/Data/modelWRF/LES/UCLALES-SALSA/bin/2017122200/'
if not os.path.exists(outpath+'/FogAnalysis/'):
        os.makedirs(outpath+'/FogAnalysis/')

outFile=outpath+'/FogAnalysis/rh_vertical_profile.png'
savefig(outFile);
plt.close(fig) ; fig.clf(fig)  

############################################################################################################ 
vert_prof=tot_mrio
fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
x =np.arange(0,vert_prof[:,:].shape[0],1) ;   y = np.arange(0,vert_prof[:,:].shape[1])
X, Y = np.meshgrid(x, y)

clevs=[0.005,0.006,0.007,0.008,0.009,0.010,0.012,0.013,0.014,0.015]        #colors1 = plt.cm.binary(np.linspace(0., 1, 128))
colors2 = plt.cm.Blues(np.linspace(0., 1, 128))
colors3 = plt.cm.Reds(np.linspace(0, 1, 128))

# combine them and build a new colormap
colors = np.vstack((colors2,colors3))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
#cs =plt.contourf(X,Y,vert_prof.T,cmap=mymap) 

cs =plt.contourf(X,Y,vert_prof.T,levels=clevs,cmap=mymap)
#plt.clabel(cs1, inline=1, fontsize=16)
cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; #cbar.ax.invert_yaxis()

ax.set_xticks(x[::7]) ; 
xTickMarks=date_list[::7]
xtickNames = ax.set_xticklabels(xTickMarks)            
plt.setp(xtickNames, rotation=90, fontsize=12,family='sans-serif')
            
ax.set_yticks(y[::5]) ; 
yTickMarks=z[::5]
ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Total Mixing Ratio'
plt.title(titl,color='black',fontsize=18,y=1.05)                             
plt.tight_layout(h_pad=3) ; 

outpath='/home/vkvalappil/Data/modelWRF/LES/UCLALES-SALSA/bin/2017122200/'
if not os.path.exists(outpath+'/FogAnalysis/'):
        os.makedirs(outpath+'/FogAnalysis/')

outFile=outpath+'/FogAnalysis/tmrio_vertical_profile.png'
savefig(outFile);
plt.close(fig) ; fig.clf(fig)

###############################################################################################################
vert_prof=lqd_mrio
fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
x =np.arange(0,vert_prof[:,:].shape[0],1) ;   y = np.arange(0,vert_prof[:,:].shape[1])
X, Y = np.meshgrid(x, y)

clevs=[0.0000,0.0002,0.0004,0.0006,0.0008,0.0010,0.0012,0.0014,0.0016]        #colors1 = plt.cm.binary(np.linspace(0., 1, 128))
colors2 = plt.cm.Blues(np.linspace(0., 1, 128))
colors3 = plt.cm.Reds(np.linspace(0, 1, 128))

# combine them and build a new colormap
colors = np.vstack((colors2,colors3))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
#cs =plt.contourf(X,Y,vert_prof.T,cmap=mymap) 

cs =plt.contourf(X,Y,vert_prof.T,levels=clevs,cmap=mymap)
#plt.clabel(cs1, inline=1, fontsize=16)
cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; #cbar.ax.invert_yaxis()

ax.set_xticks(x[::7]) ; 
xTickMarks=date_list[::7]
xtickNames = ax.set_xticklabels(xTickMarks)            
plt.setp(xtickNames, rotation=90, fontsize=12,family='sans-serif')
            
ax.set_yticks(y[::5]) ; 
yTickMarks=z[::5]
ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Liquid Mixing Ratio'
plt.title(titl,color='black',fontsize=18,y=1.05)                             
plt.tight_layout(h_pad=3) ; 

outpath='/home/vkvalappil/Data/modelWRF/LES/UCLALES-SALSA/bin/2017122200/'
if not os.path.exists(outpath+'/FogAnalysis/'):
        os.makedirs(outpath+'/FogAnalysis/')

outFile=outpath+'/FogAnalysis/lmrio_vertical_profile.png'
savefig(outFile);
plt.close(fig) ; fig.clf(fig)
##############################################################################
vert_prof=rflx
fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
x =np.arange(0,vert_prof[:,:].shape[0],1) ;   y = np.arange(0,vert_prof[:,:].shape[1])
X, Y = np.meshgrid(x, y)

clevs=np.arange(vert_prof.min(),vert_prof.max()+5,5)
colors2 = plt.cm.Blues(np.linspace(0., 1, 128))
colors3 = plt.cm.Reds(np.linspace(0, 1, 128))

# combine them and build a new colormap
colors = np.vstack((colors2,colors3))
mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
#cs =plt.contourf(X,Y,vert_prof.T,cmap=mymap) 

cs =plt.contourf(X,Y,vert_prof.T,levels=clevs,cmap=mymap)
#plt.clabel(cs1, inline=1, fontsize=16)
cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; #cbar.ax.invert_yaxis()

ax.set_xticks(x[::7]) ; 
xTickMarks=date_list[::7]
xtickNames = ax.set_xticklabels(xTickMarks)            
plt.setp(xtickNames, rotation=90, fontsize=12,family='sans-serif')
            
ax.set_yticks(y[::5]) ; 
yTickMarks=z[::5]
ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Radiative Flux'
plt.title(titl,color='black',fontsize=18,y=1.05)                             
plt.tight_layout(h_pad=3) ; 

outpath='/home/vkvalappil/Data/modelWRF/LES/UCLALES-SALSA/bin/2017122200/'
if not os.path.exists(outpath+'/FogAnalysis/'):
        os.makedirs(outpath+'/FogAnalysis/')

outFile=outpath+'/FogAnalysis/rflx_vertical_profile.png'
savefig(outFile);
plt.close(fig) ; fig.clf(fig)

########################################################################################################
















