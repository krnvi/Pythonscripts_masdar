#!/usr/bin/env python
"""
Created on Thu Mar  8 13:07:56 2018

@author: vkvalappil
"""

import os ; import sys ; import numpy as np ; import datetime as dt ;   from dateutil import rrule ; import pandas as pd ; import pytz
from metpy.calc import dewpoint_rh,height_to_pressure_std  ; from metpy.units import units

###############################################################################################################################################################

def readRadiometerData(fnme):
              
     def plot_fsi(parm,fsi_data,_date): 
         
             import matplotlib.pyplot as plt; from pylab import savefig ;  from matplotlib import cm
             C=fsi_data         
             fig, ax1= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
             ax2 = ax1.twinx()

               
             ax1 = C.iloc[:,2].plot.line(ax=ax1,marker='o',grid=False, legend=True, style=None, rot=45,linewidth=3,color='k',)              

             ax2 = C.iloc[:,1].plot.line(ax=ax2,marker='o', grid=False, legend=True, style=None,  rot=45,linewidth=3,color='r')              
                                      
             leg1=ax1.legend(loc='upper left',fontsize=18)
             leg2=ax2.legend(loc='upper right',fontsize=18)
             
             ax1.axhline(y=25,linewidth=3, color='g')
             ax1.axhline(y=35,linewidth=3, color='b')
             ax2.axhline(y=1000,linewidth=3, color='r',linestyle='--')

             ax1.set_yticks(np.linspace(-15, ax1.get_ybound()[1]+1, 15))          
             ax2.set_yticks(np.linspace(0, ax2.get_ybound()[1]+1, 15))          
             ax1.tick_params(axis='y', colors='k',labelsize=18) ; ax1.set_ylabel('Fog Threat Index',color='k',fontsize=18) ;                                    
             ax2.tick_params(axis='y', colors='r',labelsize=18) ; ax2.set_ylabel('Visibility',color='r',fontsize=18) ;            
                                    
             plt.title('Fog Threat & Visibility',color='black',fontsize=18,y=1.05)

             plt.tight_layout(h_pad=3) ; 
         
             if not os.path.exists(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]):
                 os.makedirs(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8])
                 
             outFile=outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]+'/'+parm+'Fog_threat_visibility'+_date[0:8]+'.png'
             
             savefig(outFile);
             plt.close(fig) ; fig.clf(fig)                
     def plot_fsi_catg(parm,fsi_data,_date,catg): 
         
             import matplotlib.pyplot as plt; from pylab import savefig ;  from matplotlib import cm
             C=fsi_data         
             fig, ax1= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
             ax2 = ax1.twinx()

               
             ax1 = C.iloc[:,2].plot.line(ax=ax1,marker='o',grid=False, legend=True, style=None, rot=45,linewidth=3,color='k',)              

             ax2 = C.iloc[:,1].plot.line(ax=ax2,marker='o', grid=False, legend=True, style=None,  rot=45,linewidth=3,color='r')              
                                      
             leg1=ax1.legend(loc='upper left',fontsize=18)
             leg2=ax2.legend(loc='upper right',fontsize=18)
             
             ax1.axhline(y=25,linewidth=3, color='g')
             ax1.axhline(y=35,linewidth=3, color='b')
             ax2.axhline(y=1000,linewidth=3, color='r',linestyle='--')

             ax1.set_yticks(np.linspace(-15, ax1.get_ybound()[1]+1, 15))          
             ax2.set_yticks(np.linspace(0, ax2.get_ybound()[1]+1, 15))          
             ax1.tick_params(axis='y', colors='k',labelsize=18) ; ax1.set_ylabel('Fog Threat Index',color='k',fontsize=18) ;                                    
             ax2.tick_params(axis='y', colors='r',labelsize=18) ; ax2.set_ylabel('Visibility',color='r',fontsize=18) ;            
                                    
             plt.title('Fog Threat & Visibility',color='black',fontsize=18,y=1.05)

             plt.tight_layout(h_pad=3) ; 
         
             if not os.path.exists(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]):
                 os.makedirs(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8])
                 
             outFile=outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]+'/'+parm+'_'+catg+'_Fog_threat_visibility'+_date[0:8]+'.png'
             
             savefig(outFile);
             plt.close(fig) ; fig.clf(fig)      
              
     def plot_contour_data(parm,vert_prof,catg,xtk):
             import matplotlib.pyplot as plt; from pylab import savefig ;  from matplotlib import cm ; import matplotlib.colors as mcolors
         
             fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
             #ax4 = ax1.twinx()
             x =np.arange(0,vert_prof.iloc[:,4:41].T.shape[1],1) ; 
             y = np.arange(0,vert_prof.iloc[:,4:41].T.shape[0])
             X, Y = np.meshgrid(x, y)

             clevs=[260,262,264,266,268,270,272,274,276,278,280,282,284,285,286,287,288,289,290,291,292]
             #colors1 = plt.cm.binary(np.linspace(0., 1, 128))
             #colors1 = plt.cm.gist_heat_r(np.linspace(0, 1, 128))

             colors2 = plt.cm.Blues(np.linspace(0., 1, 128))
             colors3 = plt.cm.Reds(np.linspace(0, 1, 128))


             # combine them and build a new colormap
             colors = np.vstack((colors2,colors3))
             mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)



             cs =plt.contourf(X,Y,vert_prof.iloc[:,4:41].T,levels=clevs,cmap=mymap)
             #cs1 =plt.contour(X,Y,vert_prof.iloc[:,4:45].T,levels=clevs,colors='K',linewidths=0.3) 
             #plt.clabel(cs1, inline=1, fontsize=16)
             cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; cbar.ax.invert_yaxis()

             ax.set_xticks(x[::xtk]) ; 
             xTickMarks=vert_prof['Date'][::xtk]
             xtickNames = ax.set_xticklabels(xTickMarks)            
             plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')
            
             ax.set_yticks(y[::5]) ; 
             yTickMarks=vert_prof.columns[4:41][::5]
             ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
             ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
             ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Temperature Profile:'+_date
             plt.title(titl,color='black',fontsize=18,y=1.05)                             
             plt.tight_layout(h_pad=3) ; 
         
             if not os.path.exists(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]):
                 os.makedirs(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8])

             outFile=outpath+'/FogAnalysis/'+parm+'/'+_date[0:6]+'/'+parm+'_'+catg+'_hours_vertical_profile'+_date[0:6]+'_1km.png'
             savefig(outFile);
             plt.close(fig) ; fig.clf(fig)  
################################################################       
             fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
             #ax4 = ax1.twinx()
             x =np.arange(0,vert_prof.iloc[:,4:].T.shape[1],1) ; 
             y = np.arange(0,vert_prof.iloc[:,4:].T.shape[0])
             X, Y = np.meshgrid(x, y)
             clevs=[190,200,210,220,225,230,235,240,245,250,255,260,262,264,266,268,270,272,274,276,278,280,282,284,285,286,287,288,289,290,291,292]

             cs =plt.contourf(X,Y,vert_prof.iloc[:,4:].T,levels=clevs,cmap=cm.gist_rainbow_r )
             cs1 =plt.contour(X,Y,vert_prof.iloc[:,4:].T,levels=clevs,colors='K',linewidths=0.3) 
             plt.clabel(cs1, inline=1, fontsize=16)
             cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; cbar.ax.invert_yaxis()

             ax.set_xticks(x[::xtk]) ; 
             xTickMarks=vert_prof['Date'][::xtk]
             xtickNames = ax.set_xticklabels(xTickMarks)            
             plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')
            
             ax.set_yticks(y[::5]) ; 
             yTickMarks=vert_prof.columns[4:][::5]
             ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
             ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
             ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Temperature Profile:'+_date
             plt.title(titl,color='black',fontsize=18,y=1.05)

             plt.xticks(size=18)
    
             plt.tight_layout(h_pad=3) ; 
         
             if not os.path.exists(outpath+'/FogAnalysis/'+parm+'/'+_date[0:6]):
                 os.makedirs(outpath+'/FogAnalysis/'+parm+'/'+_date[0:6])

             outFile=outpath+'/FogAnalysis/'+parm+'/'+_date[0:6]+'/'+parm+'_'+catg+'_hours_vertical_profile'+_date[0:6]+'.png'
             savefig(outFile);
             plt.close(fig) ; fig.clf(fig)  

     def plot_contour_dailydata(parm,vert_prof,_date):
             import matplotlib.pyplot as plt; from pylab import savefig ;  from matplotlib import cm ; import matplotlib.colors as mcolors
             from matplotlib.colors import from_levels_and_colors ;
         
             fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
             #ax4 = ax1.twinx()
             x =np.arange(0,vert_prof.iloc[:,4:].T.shape[1],1) ; 
             y = np.arange(0,vert_prof.iloc[:,4:].T.shape[0])
             X, Y = np.meshgrid(x, y)
             clevs=[190,200,210,220,225,230,235,240,245,250,255,260,262,264,266,268,270,272,274,276,278,280,282,284,285,286,287,288,289,290,291,292]


#             mymap = mcolors.ListedColormap(['peachpuff','navajowhite','mistyrose','steelblue','cornflowerblue','slateblue','royalblue','blue','dodgerblue','deepskyblue','skyblue','mediumturquoise',\
#                                             'mediumaquamarine','lightseagreen','seagreen','greenyellow','indianred','forestgreen','yellow','gold','orange','darkorange',\
#                                             'sandybrown','limegreen','coral','orangered','red','hotpink','darkorchid','blueviolet','purple'])
#             nice_cmap= plt.get_cmap(mymap)
#             colors = nice_cmap([0,1, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
#             colors =nice_cmap([30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0])
#             #cmap, norm = from_levels_and_colors(clevs, colors, extend='both')
#             #norml = mcolors.BoundaryNorm(clevs, ncolors=cmap.N, clip=True)

             colors2 = plt.cm.Blues(np.linspace(0., 1, 128))
             colors3 = plt.cm.Reds(np.linspace(0, 1, 128))


             # combine them and build a new colormap
             colors = np.vstack((colors2,colors3))
             mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)

             cs =plt.contourf(X,Y,vert_prof.iloc[:,4:].T,levels=clevs,cmap=cm.gist_rainbow_r )  #cm.gist_rainbow_r
             cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; cbar.ax.invert_yaxis()

             cs1 =plt.contour(X,Y,vert_prof.iloc[:,4:].T,levels=clevs,colors='K',linewidths=0.3) 
             plt.clabel(cs1, inline=1, fontsize=13)

             ax.set_xticks(x[::5]) ; 
             xTickMarks=vert_prof['Date'][::5]
             xtickNames = ax.set_xticklabels(xTickMarks)            
             plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')
            
             ax.set_yticks(y[::5]) ; 
             yTickMarks=vert_prof.columns[4:][::5]
             ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
             ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
             ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Temperature Profile:'+_date
             plt.title(titl,color='black',fontsize=18,y=1.05)

             plt.xticks(size=18)
    
             plt.tight_layout(h_pad=3) ; 
         
             if not os.path.exists(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]):
                 os.makedirs(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8])
                 
             outFile=outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]+'/'+parm+'_vertical_profile'+_date[0:8]+'.png'
             savefig(outFile);
             plt.close(fig) ; fig.clf(fig)               
##############################################################             
             
             fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
             #ax4 = ax1.twinx()
             x =np.arange(0,vert_prof.iloc[:,4:41].T.shape[1],1) ; 
             y = np.arange(0,vert_prof.iloc[:,4:41].T.shape[0])
             X, Y = np.meshgrid(x, y)

             
             clevs=[260,262,264,266,268,270,272,274,276,278,280,282,284,285,286,287,288,289,290,291,292]

             colors2 = plt.cm.Blues(np.linspace(0., 1, 128))
             colors3 = plt.cm.Reds(np.linspace(0, 1, 128))


             # combine them and build a new colormap
             colors = np.vstack((colors2,colors3))
             mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)

             cs =plt.contourf(X,Y,vert_prof.iloc[:,4:41].T,levels=clevs,cmap=mymap )  #cm.gist_rainbow_r
             cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; cbar.ax.invert_yaxis()

             cs1 =plt.contour(X,Y,vert_prof.iloc[:,4:41].T,levels=clevs,colors='K',linewidths=0.3) 
             plt.clabel(cs1, inline=1, fontsize=13)

             ax.set_xticks(x[::5]) ; 
             xTickMarks=vert_prof['Date'][::5]
             xtickNames = ax.set_xticklabels(xTickMarks)            
             plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')
            
             ax.set_yticks(y[::5]) ; 
             yTickMarks=vert_prof.columns[4:41][::5]
             ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
             ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
             ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Temperature Profile:'+_date
             plt.title(titl,color='black',fontsize=18,y=1.05)

             plt.xticks(size=18)
    
             plt.tight_layout(h_pad=3) ; 
         
             if not os.path.exists(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]):
                 os.makedirs(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8])

             outFile=outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]+'/'+parm+'_vertical_profile'+_date[0:8]+'_1km.png'
             savefig(outFile);
             plt.close(fig) ; fig.clf(fig)                            
#############################################################################################################################################            
     def plot_contour_prefog(parm,vert_prof,_date,catg):
             import matplotlib.pyplot as plt; from pylab import savefig ;  from matplotlib import cm; import matplotlib.colors as mcolors
         
             fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
             #ax4 = ax1.twinx()
             x =np.arange(0,vert_prof.iloc[:,4:].T.shape[1],1) ; 
             y = np.arange(0,vert_prof.iloc[:,4:].T.shape[0])
             X, Y = np.meshgrid(x, y)
            
             clevs=[190,200,210,220,225,230,235,240,245,250,255,260,262,264,266,268,270,272,274,276,278,280,282,284,285,286,287,288,289,290,291,292]

             cs =plt.contourf(X,Y,vert_prof.iloc[:,4:].T,levels=clevs,cmap=cm.gist_rainbow_r )
             cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; cbar.ax.invert_yaxis()

             cs1 =plt.contour(X,Y,vert_prof.iloc[:,4:].T,levels=clevs,colors='K',linewidths=0.3) 
             plt.clabel(cs1, inline=1, fontsize=13)

             ax.set_xticks(x[::5]) ; 
             xTickMarks=vert_prof['Date'][::5]
             xtickNames = ax.set_xticklabels(xTickMarks)            
             plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')
            
             ax.set_yticks(y[::5]) ; 
             yTickMarks=vert_prof.columns[4:][::5]
             ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
             ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
             ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Temperature Profile:'+_date
             plt.title(titl,color='black',fontsize=18,y=1.05)

             plt.xticks(size=18)
    
             plt.tight_layout(h_pad=3) ; 
         
             if not os.path.exists(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]):
                 os.makedirs(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8])

             outFile=outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]+'/'+parm+catg+'_vertical_profile'+_date[0:8]+'.png'
             savefig(outFile);
             plt.close(fig) ; fig.clf(fig)  
##############################################################
             fig, ax= plt.subplots(1, sharex=True, sharey=False,figsize=(12,12),dpi=50)
             #ax4 = ax1.twinx()
             x =np.arange(0,vert_prof.iloc[:,4:41].T.shape[1],1) ; 
             y = np.arange(0,vert_prof.iloc[:,4:41].T.shape[0])
             X, Y = np.meshgrid(x, y)
             clevs=[260,262,264,266,268,270,272,274,276,278,280,282,284,285,286,287,288,289,290,291,292]

             colors2 = plt.cm.Blues(np.linspace(0., 1, 128))
             colors3 = plt.cm.Reds(np.linspace(0, 1, 128))


             # combine them and build a new colormap
             colors = np.vstack((colors2,colors3))
             mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)

             cs =plt.contourf(X,Y,vert_prof.iloc[:,4:41].T,levels=clevs,cmap=mymap )  #cm.gist_rainbow_r
             cbar=plt.colorbar(cs, shrink=0.8, extend='both') ;  cbar.set_ticks([clevs]) ; cbar.ax.invert_yaxis()

             cs1 =plt.contour(X,Y,vert_prof.iloc[:,4:41].T,levels=clevs,colors='K',linewidths=0.3) 
             plt.clabel(cs1, inline=1, fontsize=13)

             ax.set_xticks(x[::5]) ; 
             xTickMarks=vert_prof['Date'][::5]
             xtickNames = ax.set_xticklabels(xTickMarks)            
             plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')
            
             ax.set_yticks(y[::5]) ; 
             yTickMarks=vert_prof.columns[4:41][::5]
             ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
             ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')                             
             ax.set_ylabel('Height Levels',color='blue',fontsize=18) ;  titl='Temperature Profile:'+_date
             plt.title(titl,color='black',fontsize=18,y=1.05)

             plt.xticks(size=18)
    
             plt.tight_layout(h_pad=3) ; 
         
             if not os.path.exists(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]):
                 os.makedirs(outpath+'/FogAnalysis/'+parm+'/'+_date[0:8])

             outFile=outpath+'/FogAnalysis/'+parm+'/'+_date[0:8]+'/'+parm+catg+'_vertical_profile'+_date[0:8]+'_1km.png'
             savefig(outFile);
             plt.close(fig) ; fig.clf(fig)                            
                          
###########################################################################################################################################

     hpc_file=main+'data/Files/hpc_201803.csv'
     rhp_file=main+'data/Files/rhp_201803.csv'
     tpc_file=main+'data/Files/tpc_201803.csv'
     tpb_file=main+'data/Files/tpb_201803.csv'

     met_file=main+'data/Files/met_minute_201803.csv'
     vis_file=main+'data/Files/vis_201803.csv'
     cbh_file=main+'data/Files/cbh_201803.csv'

####################################################################################################################################          
     #tpb_data=pd.read_csv(tpb_file).as_matrix()
     tpb_data=np.genfromtxt(tpb_file,delimiter=',',dtype='S')  ; 
     columns=np.empty((1,94)).astype(str) ; columns[0,0]='Date' ;  columns[0,1:]=tpb_data[0,7:] ;   
     date_cols=tpb_data[1:,0:6].astype(int)
     date_ary=np.vstack([(dt.datetime(*x).replace(year=2000+dt.datetime(*x).year)).strftime('%Y%m%d%H%M%S') for x in date_cols[:]])        
     tpb_data_1=np.concatenate([columns,np.concatenate([date_ary,tpb_data[1:,7:]],axis=1)],axis=0)
     
     tpb_data_1=pd.DataFrame(data=tpb_data_1[1:,:],columns=tpb_data_1[0,:])  
     tpb_data_1['Date']=tpb_data_1['Date'].apply(pd.to_datetime, errors='ignore') ; 
     tpb_data_1.iloc[:,1:]=tpb_data_1.iloc[:,1:].apply(pd.to_numeric,errors='coerce')
     tpb_data_1.index = pd.to_datetime(tpb_data_1.Date) ;          
     tpb_data_1.index =tpb_data_1.index.tz_localize(pytz.utc).tz_convert(pytz.timezone('Asia/Dubai'))
     tpb_data_1['Date']=tpb_data_1.index
     tpb_data_1=tpb_data_1.iloc[:,:].resample('1Min').mean() ; tpb_data_1.insert(0,'Date', tpb_data_1.index)
     #tpb_data_hour=tpb_data_1.iloc[:,:].resample('1H').mean()  ; tpb_data_hour.insert(0,'Date', tpb_data_hour.index) ; 
     idx = pd.date_range('2018-03-01 00:00:00', '2018-03-31 23:59:00',freq='T').tz_localize(pytz.timezone('Asia/Dubai')) #Missing data filled with Nan
     tpb_data_2=tpb_data_1.reindex(idx, fill_value=np.nan)
     tpb_data_2['Date']=tpb_data_2.index

##########################################################################################################################################
     #tpc_data=pd.read_csv(tpc_file).as_matrix()
     tpc_data=np.genfromtxt(tpc_file,delimiter=',',dtype='S')  ; 
     columns=np.empty((1,94)).astype(str) ; columns[0,0]='Date' ;  columns[0,1:]=tpc_data[0,7:] ;   
     date_cols=tpc_data[1:,0:6].astype(int)
     date_ary=np.vstack([(dt.datetime(*x).replace(year=2000+dt.datetime(*x).year)).strftime('%Y%m%d%H%M%S') for x in date_cols[:]])        
     tpc_data_1=np.concatenate([columns,np.concatenate([date_ary,tpc_data[1:,7:]],axis=1)],axis=0)
     
     tpc_data_1=pd.DataFrame(data=tpc_data_1[1:,:],columns=tpc_data_1[0,:])  
     tpc_data_1['Date']=tpc_data_1['Date'].apply(pd.to_datetime, errors='ignore') ; 
     tpc_data_1.iloc[:,1:]=tpc_data_1.iloc[:,1:].apply(pd.to_numeric,errors='coerce')
     tpc_data_1.index = pd.to_datetime(tpc_data_1.Date) ; 
     tpc_data_1.index =tpc_data_1.index.tz_localize(pytz.utc).tz_convert(pytz.timezone('Asia/Dubai'))
     tpc_data_1['Date']=tpc_data_1.index
         
     tpc_data_1=tpc_data_1.iloc[:,:].resample('1Min').mean() ; tpc_data_1.insert(0,'Date', tpc_data_1.index)
     #tpc_data_hour=tpc_data_1.iloc[:,:].resample('1H').mean()  ; tpc_data_hour.insert(0,'Date', tpc_data_hour.index) ; 
     idx = pd.date_range('2018-03-01 00:00:00', '2018-03-31 23:59:00',freq='T').tz_localize(pytz.timezone('Asia/Dubai')) #Missing data filled with Nan
     tpc_data_2=tpc_data_1.reindex(idx, fill_value=np.nan)
     tpc_data_2['Date']=tpc_data_2.index
       
##################################################################################################################################################        
     #hpc_data=pd.read_csv(hpc_file).as_matrix()
     hpc_data=np.genfromtxt(hpc_file,delimiter=',',dtype='S')  ; 
     columns=np.empty((1,94)).astype(str) ; columns[0,0]='Date' ;  columns[0,1:]=hpc_data[0,7:] ;   
     date_cols=hpc_data[1:,0:6].astype(int)
     date_ary=np.vstack([(dt.datetime(*x).replace(year=2000+dt.datetime(*x).year)).strftime('%Y%m%d%H%M%S') for x in date_cols[:]])        
     hpc_data_1=np.concatenate([columns,np.concatenate([date_ary,hpc_data[1:,7:]],axis=1)],axis=0)
     
     hpc_data_1=pd.DataFrame(data=hpc_data_1[1:,:],columns=hpc_data_1[0,:])  
     hpc_data_1['Date']=hpc_data_1['Date'].apply(pd.to_datetime, errors='ignore') ; 
     hpc_data_1.iloc[:,1:]=hpc_data_1.iloc[:,1:].apply(pd.to_numeric,errors='coerce')
     hpc_data_1.index = pd.to_datetime(hpc_data_1.Date) ; 
     hpc_data_1.index =hpc_data_1.index.tz_localize(pytz.utc).tz_convert(pytz.timezone('Asia/Dubai'))
     hpc_data_1['Date']=hpc_data_1.index
         
     hpc_data_1=hpc_data_1.iloc[:,:].resample('1Min').mean() ; hpc_data_1.insert(0,'Date', hpc_data_1.index)
     #hpc_data_hour=hpc_data_1.iloc[:,:].resample('1H').mean()  ; hpc_data_hour.insert(0,'Date', hpc_data_hour.index) ; 
     
     hpc_data_2=hpc_data_1.reindex(idx, fill_value=np.nan)
     hpc_data_2['Date']=hpc_data_2.index     

     #rhp_data=pd.read_csv(rhp_file).as_matrix()
     rhp_data=np.genfromtxt(rhp_file,delimiter=',',dtype='S')  ; 
     columns=np.empty((1,94)).astype(str) ; columns[0,0]='Date' ;  columns[0,1:]=rhp_data[0,7:] ;   
     date_cols=rhp_data[1:,0:6].astype(int)
     date_ary=np.vstack([(dt.datetime(*x).replace(year=2000+dt.datetime(*x).year)).strftime('%Y%m%d%H%M%S') for x in date_cols[:]])        
     rhp_data_1=np.concatenate([columns,np.concatenate([date_ary,rhp_data[1:,7:]],axis=1)],axis=0)
     
     rhp_data_1=pd.DataFrame(data=rhp_data_1[1:,:],columns=rhp_data_1[0,:])  
     rhp_data_1['Date']=rhp_data_1['Date'].apply(pd.to_datetime, errors='ignore') ; 
     rhp_data_1.iloc[:,1:]=rhp_data_1.iloc[:,1:].apply(pd.to_numeric,errors='coerce')
     rhp_data_1.index = pd.to_datetime(rhp_data_1.Date) ; 
     rhp_data_1.index =rhp_data_1.index.tz_localize(pytz.utc).tz_convert(pytz.timezone('Asia/Dubai'))
     rhp_data_1['Date']=rhp_data_1.index
         
     rhp_data_1=rhp_data_1.iloc[:,:].resample('1Min').mean() ; rhp_data_1.insert(0,'Date', rhp_data_1.index)
     #rhp_data_hour=rhp_data_1.iloc[:,:].resample('1H').mean()  ; rhp_data_hour.insert(0,'Date', rhp_data_hour.index) ; 
     
     rhp_data_2=rhp_data_1.reindex(idx, fill_value=np.nan)
     rhp_data_2['Date']=rhp_data_2.index
     
     spc_data_2=calculateSPH(tpc_data_2,hpc_data_2)
################################################################################################################################
#     met_data=pd.read_csv(met_file).as_matrix()   

#     columns=np.empty((1,7)).astype(str) ; columns[0,0]='Date' ; columns[0,1]='pressure' ; columns[0,2]='Temperature' ; 
#     columns[0,3]='RH' ; columns[0,4]='WS' ; columns[0,5]='WD'; columns[0,6]='RainRate'
#     date_cols=met_data[1:,0:6].astype(int)
#     date_ary=np.vstack([(dt.datetime(*x).replace(year=2000+dt.datetime(*x).year)).strftime('%Y%m%d%H%M%S') for x in date_cols[:]])        
#     met_data_1=np.concatenate([columns,np.concatenate([date_ary,met_data[1:,7:]],axis=1)],axis=0)

     met_data=pd.read_csv(met_file)

     met_data_1=met_data.drop(['Date.1'],axis=1)
     
     met_data_1['Date']=met_data_1['Date'].apply(pd.to_datetime, errors='ignore') ; 
     met_data_1[['pressure','Temperature','RH','WS','WD','RainRate']]=met_data_1[['pressure','Temperature','RH','WS','WD','RainRate']].apply(pd.to_numeric,errors='coerce')
     #met_data_1['WS']=met_data_1['WS']*0.2777   #(5/18  km/h to m/sec)
     met_data_1.index = met_data_1.Date ; 
     met_data_1.index =met_data_1.index.tz_localize(pytz.utc).tz_convert(pytz.timezone('Asia/Dubai'))
     met_data_1['Date']=met_data_1.index
        
     #met_data_1=met_data_1.iloc[:,:].resample('1Min').mean() ; met_data_1.insert(0,'Date', met_data_1.index)
     #met_data_hour=met_data_1.iloc[:,:].resample('1H').mean()  ; met_data_hour.insert(0,'Date', met_data_hour.index) ; 
     met_data_2=met_data_1.reindex(idx, fill_value=pd.np.nan) 
     met_data_2['Date']=met_data_2.index
###############################################################################################################################
     vis_data=pd.read_csv(vis_file)
     vis_data['Date']=vis_data['Date'].apply(pd.to_datetime, errors='ignore',format='%Y-%m-%d-%H-%M') ; 
     vis_data[['Ex.Coeff','Visibility(m)','Lux(KM)','DN_Flag','ErrorCode','ctrlrelay']]=\
     vis_data[['Ex.Coeff','Visibility(m)','Lux(KM)','DN_Flag','ErrorCode','ctrlrelay']].apply(pd.to_numeric,errors='coerce')
     vis_data.index = vis_data.Date ;        
     vis_data.index =vis_data.index.tz_localize(pytz.timezone('Asia/Dubai')) #.tz_convert(pytz.utc))
     vis_data['Date']=vis_data.index
     
     vis_data_2=vis_data.reindex(idx, fill_value=np.nan) 
     vis_data_2['Date']=vis_data_2.index

##################################################################################################################################

     cbh_data=pd.read_csv(cbh_file).as_matrix()
     columns=np.empty((1,2)).astype(str) ; columns[0,0]='Date' ; columns[0,-1]='cbh' 
     date_cols=cbh_data[1:,0:6].astype(int)
     date_ary=np.vstack([(dt.datetime(*x).replace(year=2000+dt.datetime(*x).year)).strftime('%Y%m%d%H%M%S') for x in date_cols[:]])        
     cbh_data_1=np.concatenate([columns,np.concatenate([date_ary,cbh_data[1:,7:10]],axis=1)],axis=0)
     
     cbh_data_1=pd.DataFrame(data=cbh_data_1[1:,:],columns=cbh_data_1[0,:])  
     cbh_data_1['Date']=cbh_data_1['Date'].apply(pd.to_datetime, errors='ignore') ; 
     cbh_data_1[['cbh']]=cbh_data_1[['cbh']].apply(pd.to_numeric,errors='coerce')
     cbh_data_1.index = cbh_data_1.Date ;          
     cbh_data_1=cbh_data_1.iloc[:,:].resample('1Min').mean() ; cbh_data_1.insert(0,'Date', cbh_data_1.index)
     cbh_data_1.index =cbh_data_1.index.tz_localize(pytz.utc).tz_convert(pytz.timezone('Asia/Dubai'))
     cbh_data_1['Date']=cbh_data_1.index

     cbh_data_2=cbh_data_1.reindex(idx, fill_value=pd.np.nan) 
     cbh_data_2['Date']=cbh_data_2.index
     
#################################################################################################################
     ## dewpoint calculated from RH
     tpb_hour=tpb_data_2.iloc[:,:].resample('30Min').mean()  ; tpb_hour.insert(0,'Date', tpb_hour.index) ;  
     rhp_hour=rhp_data_2.iloc[:,:].resample('30Min').mean()  ; rhp_hour.insert(0,'Date', rhp_hour.index) ; 
     tpc_hour=tpc_data_2.iloc[:,:].resample('30Min').mean()  ; tpc_hour.insert(0,'Date', tpc_hour.index) ; 
     met_hour=met_data_2.iloc[:,:].resample('30Min').mean()  ; met_hour.insert(0,'Date', met_hour.index) ; 
     vis_hour=vis_data_2.iloc[:,:].resample('30Min').mean()  ; vis_hour.insert(0,'Date', vis_hour.index) ; 
     cbh_hour=cbh_data_2.iloc[:,:].resample('30Min').mean()  ; cbh_hour.insert(0,'Date', cbh_hour.index) ;  

     dpt_data=dewpoint_rh(np.array(tpc_hour.iloc[:,1:])*units('K'),(np.array(rhp_hour.iloc[:,1:])/100.)).to(units('K'))
     dpt_data_1=pd.DataFrame(dpt_data.m,columns=rhp_hour.columns[1:])
     dpt_data_1.index=rhp_hour.Date
     dpt_data_1.insert(0,'Date',rhp_hour.Date)

     dpt_data_tpb=dewpoint_rh(np.array(tpb_hour.iloc[:,1:])*units('K'),(np.array(rhp_hour.iloc[:,1:])/100.)).to(units('K'))
     dpt_data_1_tpb=pd.DataFrame(dpt_data_tpb.m,columns=rhp_hour.columns[1:])
     dpt_data_1_tpb.index=rhp_hour.Date
     dpt_data_1_tpb.insert(0,'Date',rhp_hour.Date)


#########################################################################################################################
     ## Wet bulb Potential Temperature
     import aoslib ; metpy.calc.potential_temperature
     hght=np.array(rhp_hour.columns[1:].astype(int))
     h_to_ps=(list(np.round(height_to_pressure_std(np.array(rhp_hour.columns[1:].astype(int))*units('meter')).m)))
     h_to_pss=pd.concat([pd.DataFrame(h_to_ps).transpose()]*tpb_hour.shape[0])
     tpb_hour_wet=aoslib.calctw(h_to_pss,tpb_hour.iloc[:,1:],rhp_hour.iloc[:,1:])
     tpb_hour_wet_1=pd.DataFrame(tpb_hour_wet,columns=h_to_ps)    #tpb_hour.columns[1:]
     tpb_hour_wet_1.index=tpb_hour.Date    
     tpb_hour_wet_1.insert(0,'Date',tpb_hour.Date)

     mix_ratio_1=aoslib.mixrat(h_to_pss,tpb_hour.iloc[:,1:],rhp_hour.iloc[:,1:])
     mix_ratio_2=pd.DataFrame(mix_ratio_1,columns=h_to_ps)
     mix_ratio_2.index=tpb_hour.Date    
     mix_ratio_2.insert(0,'Date',tpb_hour.Date)

     #tpb_hour_wet_2=aoslib.awips.thetawa(tpb_hour.iloc[0:2,1:],dpt_data_1_tpb.iloc[0:2,1:],h_to_pss.iloc[0:2,:],mix_ratio_1[0:2,:])

     A_w=pd.concat([tpb_hour['Date'],tpb_hour[' 1440'],dpt_data_1_tpb[' 1440'] ,mix_ratio_2[852.0]],axis=1).dropna(axis=0, how='any')
     A_w.columns=['Date','T','Td','Mr']
     tpb_hour_wet_2=pd.DataFrame([aoslib.awips.thetawa(np.round(A_w['T'][ii],1),np.round(A_w['Td'][ii],1) ,850,A_w['Mr'][ii]) for ii in range(0,A_w.shape[0])])
     tpb_hour_wet_2.index=A_w.Date    
     tpb_hour_wet_2.insert(0,'Date',A_w.Date)

     

     #mix_ratio_1=metpy.calc.mixing_ratio_from_relative_humidity(np.array(rhp_hour.iloc[:,1:])/100.,np.array(tpc_hour.iloc[:,1:])*units('K'),h_to_pss.as_matrix()*units.hectopascal)


     ###### Fog Stability Index ##############################
     h_to_ps=(list(np.round(height_to_pressure_std(np.array(rhp_hour.columns[1:].astype(int))*units('meter')).m)))
     h_to_ps.insert(0,'Date')
     dpt_data_2=dpt_data_1 ; dpt_data_2.columns=h_to_ps

     A=pd.concat([dpt_data_2['Date'],met_hour['Temperature'],tpc_hour['0'],dpt_data_2[1013.0],tpc_hour[' 10'],met_hour['WS']],axis=1)
     A.columns=['Date','met_tmp','TPC_0','Dew_0','tpc_10','met_ws']
     
     fsi_index=(4*(A['Temperature']))-2*((A['Temperature']) + (A[1013.0]))+ (A['WS']*1.94384)

     fsi_index_1=pd.concat([dpt_data_2['Date'],vis_hour['Visibility(m)'],fsi_index],axis=1)

     fsi_hig=(fsi_index_1.iloc[np.where(fsi_index_1['Visibility(m)'] >5000)])                              #.between_time('22:00','06:00') ; 
     fsi_mod=(fsi_index_1.iloc[np.where((fsi_index_1['Visibility(m)'] >1000)&(fsi_index_1['Visibility(m)'] <5000) )]) #.between_time('22:00','06:00') ;  
     fsi_fog=fsi_index_1.iloc[np.where(fsi_index_1['Visibility(m)'] <=1000)]

     [[fsi_fog[0].min(), fsi_fog[0].max()],[fsi_mod[0].min(), fsi_mod[0].max()],[fsi_hig[0].min(), fsi_hig[0].max()]]

     fog_point = (0.044 * A['met_tmp']) + (0.844 * A['Dew_0']) - 0.55 
     fog_threat= tpb_hour_wet_1[852.0]-fog_point


###########################################################################################################################
     h_to_ps=(list(np.round(height_to_pressure_std(np.array(rhp_hour.columns[1:].astype(int))*units('meter')).m)))
     h_to_ps.insert(0,'Date')
     
     dpt_data_2_tpb=dpt_data_1_tpb ; dpt_data_2_tpb.columns=h_to_ps
     



##############################  TPB
     A=pd.concat([dpt_data_2_tpb['Date'],met_hour['Temperature'],tpb_hour['0'],tpb_hour[' 1000'],dpt_data_2_tpb[1013.0],dpt_data_2_tpb[852.0],met_hour['WS'],\
                   met_hour['RH'],vis_hour['Ex.Coeff'],cbh_hour['cbh']],axis=1)

     fsi_index_tpb_1=np.round((4*(A['Temperature']))-2*((A[' 1000']) + (A[1013.0]))+ (A['WS']*1.94384)+4*(A['cbh']/1000))
     #######################

#     A=pd.concat([dpt_data_2_tpb['Date'],met_hour['Temperature'],tpb_hour['0'],tpb_hour[' 460'],dpt_data_2_tpb[1013.0],dpt_data_2_tpb[959.0],met_hour['WS'],met_hour['RH']],axis=1)
#
#     fsi_index_tpb_2=(A['0']-A[' 460']) + (A[1013.0]-A[959.0]) + (A['WS']*1.94384) #+A['RH']
#
#
#     fsi_index_tpb_3=(A['0']-A[1013.0]) + (A[' 460']-A[959.0]) + (A['WS']*1.94384) #+A['RH']
#
#     #fsi_index_tpb=(A['0']-A[1013.0]) + (A['0']-A[' 1440']) + (A['WS']*1.94384) #+A['RH']


     fsi_index_1=pd.concat([dpt_data_2_tpb['Date'],vis_hour['Visibility(m)'],fsi_index_tpb_1,met_hour['RH'],met_hour['WS']],axis=1)
     fsi_index_1.columns=['Date','Visibility(m)','fsi','RH','WS']
     fsi_index_1=fsi_index_1 #.between_time('23:00','06:00') 
     fsi_hig=(fsi_index_1.iloc[np.where(fsi_index_1['Visibility(m)'] >3000)])                              #.between_time('22:00','06:00') ; 
     fsi_mod=(fsi_index_1.iloc[np.where((fsi_index_1['Visibility(m)'] >1000)&(fsi_index_1['Visibility(m)'] <=3000) )]) #.between_time('22:00','06:00') ;  
     fsi_fog=fsi_index_1.iloc[np.where(fsi_index_1['Visibility(m)'] <=1000)]

     [[fsi_fog['fsi'].min(), fsi_fog['fsi'].max()],[fsi_mod['fsi'].min(), fsi_mod['fsi'].max()],[fsi_hig['fsi'].min(), fsi_hig['fsi'].max()]]


#################### TPC 

     A=pd.concat([dpt_data_1['Date'],met_hour['Temperature'],tpc_hour['0'],tpc_hour[' 1000'],dpt_data_1[1013.0],dpt_data_1[852.0],met_hour['WS'],\
                                       met_hour['RH'],vis_hour['Ex.Coeff'],cbh_hour['cbh']],axis=1)

     fsi_index_tpb_1=np.round((4*(A['Temperature']))-2*((A[' 1000']) + (A[1013.0]))+ (A['WS']*1.94384)+(A['cbh']/1000))
     #######################

#     A=pd.concat([dpt_data_2_tpb['Date'],met_hour['Temperature'],tpb_hour['0'],tpb_hour[' 460'],dpt_data_2_tpb[1013.0],dpt_data_2_tpb[959.0],met_hour['WS'],met_hour['RH']],axis=1)
#
#     fsi_index_tpb_2=(A['0']-A[' 460']) + (A[1013.0]-A[959.0]) + (A['WS']*1.94384) #+A['RH']
#
#
#     fsi_index_tpb_3=(A['0']-A[1013.0]) + (A[' 460']-A[959.0]) + (A['WS']*1.94384) #+A['RH']
#
#     #fsi_index_tpb=(A['0']-A[1013.0]) + (A['0']-A[' 1440']) + (A['WS']*1.94384) #+A['RH']


     fsi_index_1=pd.concat([dpt_data_2['Date'],vis_hour['Visibility(m)'],fsi_index_tpb_1,met_hour['RH'],met_hour['WS']],axis=1)
     fsi_index_1.columns=['Date','Visibility(m)','fsi','RH','WS']
     fsi_index_1=fsi_index_1 #.between_time('23:00','06:00') 
     fsi_hig=(fsi_index_1.iloc[np.where(fsi_index_1['Visibility(m)'] >3000)])                              #.between_time('22:00','06:00') ; 
     fsi_mod=(fsi_index_1.iloc[np.where((fsi_index_1['Visibility(m)'] >1000)&(fsi_index_1['Visibility(m)'] <=3000) )]) #.between_time('22:00','06:00') ;  
     fsi_fog=fsi_index_1.iloc[np.where(fsi_index_1['Visibility(m)'] <=1000)]

     [[fsi_fog['fsi'].min(), fsi_fog['fsi'].max()],[fsi_mod['fsi'].min(), fsi_mod['fsi'].max()],[fsi_hig['fsi'].min(), fsi_hig['fsi'].max()]]

     
#############################################################################################################################################################
     parm='DPT' ; _date='201803'

     A1=pd.concat([vis_data_2['Date'],vis_data_2['Visibility(m)'], met_data_2['RH'],met_data_2['WS']], axis=1)
     A_hour=A1.iloc[:,:].resample('30Min').mean()  ; A_hour.insert(0,'Date', A_hour.index) ; 
     B_hour=pd.concat([A_hour,dpt_data_1_tpb.iloc[:,1:]],axis=1)

     for indx in np.unique([x.strftime('%Y%m%d') for x in B_hour.index.date]) : 
         B1_hour=B_hour.loc[indx]     

#################         contour plots
         plot_contour_dailydata(parm,B1_hour,indx)    

         fog_st_time=(B1_hour.iloc[np.where((B1_hour['Visibility(m)'] <=1300) & (B1_hour['RH'] >=88) & (B1_hour['WS'] <=3.0))]).between_time('00:00','10:00') 
         
         if not fog_st_time.empty :
             pre_fg_st_time=(dt.datetime.strptime(fog_st_time.index.to_datetime()[0].strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')-dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
             pre_fg_ed_time=fog_st_time.index.to_datetime()[0].strftime('%Y-%m-%d %H:%M:%S')    
             pre_fg_data=(B_hour.loc[pre_fg_st_time:pre_fg_ed_time]).dropna(axis=0, how='any')
             if not pre_fg_data.shape[0] <=1 : 
                 plot_contour_prefog(parm,pre_fg_data,indx,'pre_fog')

             fg_stt_time=fog_st_time.index.to_datetime()[0].strftime('%Y-%m-%d %H:%M:%S')
             fg_ed_time=fog_st_time.index.to_datetime()[-1].strftime('%Y-%m-%d %H:%M:%S')    
             fg_data=(B1_hour.loc[fg_stt_time:fg_ed_time]).dropna(axis=0, how='any')
             if not fg_data.shape[0] <=1 :            
                 plot_contour_prefog(parm,fg_data,indx,'fog')
             
             
             post_fg_stt_time=(dt.datetime.strptime(fog_st_time.index.to_datetime()[-1].strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')+dt.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')            
             post_fg_ed_time=(dt.datetime.strptime(fog_st_time.index.to_datetime()[-1].strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')+dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
             post_fog_data=(B1_hour.loc[post_fg_stt_time:post_fg_ed_time]).dropna(axis=0, how='any')
             if not post_fog_data.empty :            
                 plot_contour_prefog(parm,post_fog_data,indx,'post_fog')             

#############################################################################################



     B_data_hig=(B_hour.iloc[np.where(B_hour['Visibility(m)'] >1000)])                              #.between_time('22:00','06:00') ; 
     #B_data_low=(A.iloc[np.where((A['Visibility(m)'] >1000)&(A['Visibility(m)'] <5000) )]) #.between_time('22:00','06:00') ;  
     B_data_fog=B_hour.iloc[np.where(B_hour['Visibility(m)'] <=1000)]

     B_data_fog_1=(B_data_fog.iloc[np.where((B_data_fog['RH'] >88) & (B_data_fog['WS'] <3.0))]) #.between_time('22:00','06:00')
     B_hour_fog=B_data_fog_1.iloc[:,:].resample('30Min').mean()  ; B_hour_fog.insert(0,'Date', B_hour_fog.index) ; 
     B1_hour_fog=B_hour_fog.dropna(axis=0, how='any')
    
     plot_contour_data(parm,B1_hour_fog,'fog',5)

     B_hour_hig=B_data_hig.iloc[:,:].resample('30Min').mean() ; B_hour_hig.insert(0,'Date', B_hour_hig.index) ;
     B1_hour_hig=B_hour_hig.dropna(axis=0, how='any')  
     
     plot_contour_data(parm,B_hour_hig,'high',30)

#     B_hour_low=B_data_low.iloc[:,:].resample('30Min').mean() ; B_hour_low.insert(0,'Date', B_hour_low.index) ;
#     B1_hour_low=B_hour_low.dropna(axis=0, how='any')  
#     
#     plot_contour_data(parm,B1_hour_low,'low')
#     plot_contour_data_1km(parm,B1_hour_low,'low')

###########################################################################
     parm='DPT' ; _date='201803'
     fsi_index_1=fsi_index_1.dropna(axis=0,how='any') 
     for indx in np.unique([x.strftime('%Y%m%d') for x in fsi_index_1.index.date]) : 
         B1_hour=fsi_index_1.loc[indx]  
         if not B1_hour.empty :
             plot_fsi(parm,B1_hour,indx)

         fog_st_time=(B1_hour.iloc[np.where((B1_hour['Visibility(m)'] <=1000) & (B1_hour['RH'] >=88) & (B1_hour['WS'] <=3.0))]).between_time('00:00','10:00') 

         if not fog_st_time.empty :
             pre_fg_st_time=(dt.datetime.strptime(fog_st_time.index.to_datetime()[0].strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')-dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
             pre_fg_ed_time=fog_st_time.index.to_datetime()[0].strftime('%Y-%m-%d %H:%M:%S')    
             pre_fg_data=(fsi_index_1.loc[pre_fg_st_time:pre_fg_ed_time]).dropna(axis=0, how='any')

             if not pre_fg_data.shape[0] <=1 : 
                 plot_fsi_catg(parm,pre_fg_data,indx,'pre_fog')

             fg_stt_time=fog_st_time.index.to_datetime()[0].strftime('%Y-%m-%d %H:%M:%S')
             fg_ed_time=fog_st_time.index.to_datetime()[-1].strftime('%Y-%m-%d %H:%M:%S')    
             fg_data=(fsi_index_1.loc[fg_stt_time:fg_ed_time]).dropna(axis=0, how='any')
             if not fg_data.shape[0] <=1 :            
                 plot_fsi_catg(parm,fg_data,indx,'fog')
             
             
             post_fg_stt_time=(dt.datetime.strptime(fog_st_time.index.to_datetime()[-1].strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')+dt.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')            
             post_fg_ed_time=(dt.datetime.strptime(fog_st_time.index.to_datetime()[-1].strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')+dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
             post_fog_data=(fsi_index_1.loc[post_fg_stt_time:post_fg_ed_time]).dropna(axis=0, how='any')
             if not post_fog_data.empty :            
                 plot_fsi_catg(parm,post_fog_data,indx,'post_fog')             










##################################################################################################################################

main='/home/vkvalappil/Data/radiometerAnalysis/'  ; scripts=main+'/scripts/' ; outpath=main+'/output/'
    readRadiometerData(filename) ; 













