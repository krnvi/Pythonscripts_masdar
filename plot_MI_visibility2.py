
import sys ; import numpy as np ; import datetime as dt ; import matplotlib.pyplot as plt; from pylab import * ;
from matplotlib import * ; import dateutil as du ;import seaborn as sns ; from dateutil import rrule ; from scipy.interpolate import interp1d

main='/home/vkvalappil/Data/'  ; scripts=main+'workspace/pythonscripts/' ; 
date=str(sys.argv[1]) ; 
vis_file=main+'/visiometerAnalysis/_data/'+date[0:4]+'/'+date[4:6]+'/'+date[0:8]+'/'+date[0:8]+'_2.csv' ;  
met_file='/home/vkvalappil/Data/masdar_station_data/wyoming/201704/AbuDhabi_surf_20170423_1.csv'
outFile=main+'/visiometerAnalysis/_data/'+date[0:4]+'/'+date[4:6]+'/'+date[0:8]+'/'+date[0:8]+'.png'
###############################################################################################################################################################

vis_data=np.genfromtxt(vis_file,delimiter=',',dtype='S')[1:,:] ;   
vis_data=vis_data.reshape(24,60,7)

met_data=np.genfromtxt(met_file,delimiter=',',dtype='S')[1:,:] ;   
met_vis=met_data[1:,8].astype(float)

h_data=vis_data[:,:,1:4].astype(float).mean(axis=1)

vis=h_data[:,1]/1000 ; ecf=h_data[:,0]   ; time=vis_data[:,0,0] ; 

fig=plt.figure(figsize=(12,10),dpi=50); ax = fig.add_subplot(111,axisbg='white')
sns.set(style='ticks') ; pos  = np.arange(1,len(vis)+1,1) ;  

#ax1=ax.twinx()   

#ax.hold(True)
ax.plot(pos,vis,'blue',linestyle='-',linewidth=3.0,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='green',markeredgecolor='black',label='Masdar')

#leg=ax.legend(["MI Visibility"],loc=1,bbox_to_anchor=(-0.3, 0.9, 1., .102),frameon=1)
#frame = leg.get_frame() ; frame.set_facecolor('white')

ax.plot(pos,met_vis,'red',linestyle='-',linewidth=3.0,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='green',markeredgecolor='black',label='Metar')

 

ax.spines['bottom'].set_color('black') ;ax.spines['right'].set_color('black') ;
ax.spines['top'].set_color('black') ;ax.spines['left'].set_color('black') ;

ax.xaxis.set_ticks_position('bottom') ; ax.yaxis.set_ticks_position('left')
ax.set_yticks(np.arange(0,max(np.round(met_vis).astype(int))+4,2))
ax.tick_params(axis='y', colors='blue',labelsize=14) ; ax.set_ylabel('visibility (KM)',color='blue',fontsize=18) ;

#ax1.yaxis.set_ticks_position('right') ; ax1.set_yticks(np.arange(0,max(ecf)+0.1,0.1))
#ax1.tick_params(axis='y', colors='red',labelsize=14) ; ax1.set_ylabel('Ext.Coefficient',color='red',fontsize=18) ; 

x_lim=pos ; ax.set_xticks(x_lim) ;  xTickMarks=time 
xtickNames = ax.set_xticklabels(xTickMarks) ; plt.setp(xtickNames, rotation=90, fontsize=15,family='sans-serif',color='black')
#ax.tick_params(axis='x', colors='black') ; 

ax.grid(True,which="major", linestyle='--',color='black',alpha=.6)



#leg=ax.legend(["Metar Visibility"],loc=1,bbox_to_anchor=(0, 0.9, 1., .102),frameon=1)
#frame = leg.get_frame() ; frame.set_facecolor('white')

titl=' Visibility - MI Field Station(Blue) & Airport Metar(Red)' ; plt.title(titl,color='black',fontsize=22,y=1.00)

plt.tight_layout(h_pad=3) ; 
savefig(outFile);
plt.close(fig) ; fig.clf(fig)


