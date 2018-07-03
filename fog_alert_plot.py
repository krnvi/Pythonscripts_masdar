
import sys ; import numpy as np ; import datetime as dt ; import xarray as xr ; import pandas as pd ; import shapefile ;   
import matplotlib.pyplot as plt ; from mpl_toolkits.basemap import  maskoceans, Basemap ; import matplotlib.colors as mcolors

#############################################################################################################################

main='/home/vkvalappil/Data/' ; scripts=main+'workspace/pythonscripts/' ; output=main+'oppModel/output/' 
inp='/home/oceanColor/Fog/WRFmodel_forecast/wrfouput_weatherforcast/Archivewrffogmaskwithbackground/'

date=str(sys.argv[1]) 

fileNme=inp+'wrfpost_'+date+'.nc'  ; nc_file=xr.open_dataset(fileNme)
fog_mask=nc_file['fog_mask'] ; lat=nc_file.lat ; lon=nc_file.lon ; time=nc_file.time
file_date_list=np.array([dt.datetime.strptime(str(tme),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d_%H:%S:%S')  for tme in pd.to_datetime((nc_file.time.data))]) 
vis=fog_mask ; 
for ii in range(0,vis.shape[0]):
    fig=plt.figure(figsize=(8,8),dpi=100); ax = fig.add_axes([0.1,0.1,0.8,0.8]) 
       
    lats=lat.data ; lons=lon.data

    #lons=np.array(wrf.to_np(lon.data[0,:,:])) ; lats=np.array(wrf.to_np(lat.data[0,:,:]))
    #lons=lons[0,:]; lats=lats[:,0]
    #lons,lats=np.meshgrid(lons,lats)
    
    m =Basemap(projection='mill',llcrnrlat=lats.min(),urcrnrlat=lats.max(),llcrnrlon=lons.min(),urcrnrlon=lons.max(),resolution='l') #wrf.get_basemap(vis)
    x, y = m(lons, lats)
    Z=maskoceans(lons,lats,vis.data[ii,:,:],inlands=False)#, resolution='c', grid=2.5)
    #Z=wrf.to_np(vis)[ii,:,:]
    #nice_cmap=plt.get_cmap('RdYlGn_r') ;     
    clevs=[0,0.5,1]    
    
    #['white 0 ','lime 1','limegreen 2','greenyellow 3','yellow 4','gold 5','orange 6','indianred 7',
    #'firebrick 8', 'darkred 9','lightskyblue 10','deepskyblue 11','royalblue 12 ','blue 13']
    
    mymap = mcolors.ListedColormap(['white','ghostwhite','floralwhite','greenyellow','yellow','gold','orange','indianred','firebrick', \
                                'darkred','lightskyblue','deepskyblue','royalblue','blue'])    
    nice_cmap= plt.get_cmap(mymap)
    colors = nice_cmap([0,3,9,13])

    cmap, norm = mcolors.from_levels_and_colors(clevs, colors, extend='both')
    norml = mcolors.BoundaryNorm(clevs, ncolors=cmap.N, clip=True)

    
    #m.contour(x, y, wrf.to_np(vis)[ii,:,:], 10, colors="black")
    cs=m.contourf(x, y,Z , levels=clevs,cmap=cmap,norm=norml,extended='both')

    m.readshapefile('/home/vkvalappil/Data/shapeFiles/uae/ARE_adm1','uae',drawbounds=True, zorder=None, linewidth=1.0, color='k', antialiased=1, ax=None, default_encoding='utf-8')
    #m.drawlsmask(land_color='0.8',ocean_color='w',lsmask=True)
    #m.drawlsmask(land_color=(0, 0, 0, 0), ocean_color='deeppink', lakes=True)
    m.drawcoastlines(linewidth=0.25,ax=ax) ; m.drawcountries(linewidth=0.25,ax=ax) ; m.drawstates(linewidth=0.25,ax=ax)     

    parallels = np.arange(np.amin(lats), np.amax(lats), 2.5) ; m.drawparallels(parallels, ax=ax, color="k", labels=[1,0,0,0]) 
    merids = np.arange(np.amin(lons), np.amax(lons), 2.5)    ; m.drawmeridians(merids, ax=ax, color="k", labels=[0,0,0,1])
    #m.drawmapboundary(fill_color='white') ; 
    #plt.colorbar(shrink=.62) location='right', pad='5%')
    
    cbar=m.colorbar(cs,location='right', pad='5%') ;  cbar.set_ticks([clevs]) 
    titl="Fog Mask"+ file_date_list[ii]
    ax.set_title(titl, {"fontsize" : 12, "color": 'k'})

    #plt.title("Visibility (FSL method)",fontsize=12,color='k')
    fileName='/home/vkvalappil/Data/oppModel/wrf_output/'+date+'/'
    plt.savefig(fileName+'fog_mask_'+file_date_list[ii]+'.png',dpi=100) 
    plt.close()
