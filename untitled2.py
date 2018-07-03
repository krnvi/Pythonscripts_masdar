#!/usr/bin/env python

import sys ; import numpy as np ; import datetime as dt ; import matplotlib.pyplot as plt; from pylab import * ;
from matplotlib import * ; import dateutil as du ;import seaborn as sns ; from dateutil import rrule ; from scipy.interpolate import interp1d


main='/home/vkvalappil/Data/'  ; scripts=main+'workspace/pythonscripts/' ; 
date=str(sys.argv[1]) ; 
rad_file=main+'/radiometerAnalysis/'+date[0:8]+'/'+date+'_HPC.csv' ; rso_file=main+'/masdar_station_data/wyoming/'+date[0:6]+'/AbuDhabi_upperair_'+date+'.csv'
outFile=main+'/radiometerAnalysis/'+date[0:8]+'/'+date+'_HPC.png'
###############################################################################################################################################################

rad_data=np.genfromtxt(rad_file,delimiter=',',dtype='S') ; rad_data=rad_data[:,8:].T ; rso_data=np.genfromtxt(rso_file,delimiter=',',dtype='S') ; 

rad_hum=rad_data[:,1].astype(float) ; rad_hgts=rad_data[:,0].astype(int)

rso_hum=rso_data[2:,4].astype(float) ; rso_hgts=rso_data[2:,1].astype(int) ; 
#rso_hum=rso_hum[rso_hgts<10000] ; rso_hgts=rso_hgts[rso_hgts<10000] ;

f = interp1d(rso_hgts, rso_hum) ; rso_hum_new=f(rad_hgts[2:])

def find_closest(A, target):
    #A must be sorted
    idx = A.searchsorted(target)
    idx = np.clip(idx, 1, len(A)-1)
    left = A[idx-1]
    right = A[idx]
    idx -= target - left < right - target
    return idx

indx=find_closest(rad_hgts,rso_hgts) ; rad_hum=rad_hum[2:] ;  rad_hgts=rad_hgts[2:] ; rso_hum=rso_hum_new

#################################################################################################################################################################

#loc_list=[1,12,15,16,24,25,32,36,37,39,40,43,48,54,55,58,58,59,66,67,70,73,74,75,75,76,76,78,79,79,80,82,83,84,84,85,87,89,90,91,91]

#rad_temp_1=rad_data[loc_list,1].astype(float)-273.15
#rad_temp_2=rad_data[loc_list,2].astype(float)-273.15
#rad_hgts=rad_data[loc_list,0]
###################################################################################################################################
fig=plt.figure(figsize=(12,10),dpi=50); ax = fig.add_subplot(111,axisbg='white')
sns.set(style='ticks') ; pos  = np.arange(0,len(rad_hum),1) ; #pos1  = np.arange(0,len(rso_hum),1) ;
ax.hold(True)
ax.plot(rad_hum,pos,'blue',linestyle='-',linewidth=2.0,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='RH Rad')

ax.plot(rso_hum,pos,'black',linestyle='-',linewidth=2.0,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='black',markeredgecolor='black',label='RH sondae') 

ax.xaxis.set_ticks_position('bottom') ; ax.yaxis.set_ticks_position('left')
   
ax.set_xticks(np.arange(min(np.round(rso_hum.astype(int))),max(np.round(rso_hum.astype(int)))+10,5.0))

#ax.set_yticks(pos) ; 
yTickMarks=rad_hgts ; #yTickMarks=rad_hgts
ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
#plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')

ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')
ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)

#leg=ax.legend(["2m,10m"],loc=1,bbox_to_anchor=(-0.3, 0.9, 1., .102),frameon=1)
#frame = leg.get_frame() ; frame.set_facecolor('white')

leg=ax.legend(loc='upper right',fontsize=20)

ax.set_ylabel('Height Levels',color='blue',fontsize=16) ;  titl='Relative Humidity (Radiometer & RadioSondae) '+date
plt.title(titl,color='black',fontsize=25,y=1.05)

plt.tight_layout(h_pad=3) ; savefig(outFile);
plt.close(fig) ; fig.clf(fig)

#quit()