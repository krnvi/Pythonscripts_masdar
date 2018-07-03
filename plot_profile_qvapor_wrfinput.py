#!/usr/bin/python

import numpy as np ; import datetime as dt
import matplotlib.pyplot as plt; from pylab import * ;
from matplotlib import * ; import dateutil as du ;import seaborn as sns
from dateutil import rrule ; 

main='/home/vkvalappil/Data/modelWRF/' ; scripts=main+'/scripts/' ;  
date='2017031500' ; rs_date='2017011500' ; fcs_st_date=dt.datetime.strptime(date,'%Y%m%d%H') ; 

file_gsi=main+'/GSI/gsiout/gsi/'+date[8:10]+'/gsianalysis_MR_'+date+'.csv' ; 

file_ngsi=main+'/input/no_gsi/'+date[8:10]+'/no_gsianalysis_MR_'+date+'.csv' ;

file_rs='/home/vkvalappil/Data/masdar_station_data/wyoming/'+date[0:6]+'/AbuDhabi_upperair_'+date+'.csv'
outFile=main+'/GSI/gsiout/gsi/'+date[8:10]+'/qvapor_'+date +'.png'


data_g=np.genfromtxt(file_gsi,dtype='S',delimiter=',')[1:44,:]
data_ng=np.genfromtxt(file_ngsi,dtype='S',delimiter=',')[1:44,:]
data_rs=np.genfromtxt(file_rs,dtype='S',delimiter=',')[2:,:]


#data_g=np.genfromtxt(file_gsi,dtype='S',delimiter=',')[1:10,:]
#data_ng=np.genfromtxt(file_ngsi,dtype='S',delimiter=',')[1:10,:]
#data_rs=np.genfromtxt(file_rs,dtype='S',delimiter=',') [2:11,:]

def find_closest(A, target):
    #A must be sorted
    idx = A.searchsorted(target)
    idx = np.clip(idx, 1, len(A)-1)
    left = A[idx-1]
    right = A[idx]
    idx -= target - left < right - target
    return idx


pres_g=data_g[:,4].astype(float) ; pres_ng=data_ng[:,4].astype(float) ; pres_rs=data_rs[:,0].astype(float) ;

indx=find_closest(pres_g,pres_rs) ;  

mr_g=data_g[:,2].astype(np.float) ; 
mr_ng=data_ng[:,2].astype(np.float) ; 
mr_rs=data_rs[indx,5].astype(np.float)/1000 ; 

pos  = np.arange(0,len(mr_g),1) ;  pos_rs  = np.arange(0,len(mr_rs),1) ; 

fig=plt.figure(figsize=(12,5),dpi=100); ax = fig.add_subplot(111,axisbg='darkslategray')
sns.set(style='ticks')

ax.plot(mr_g,pos,'blue',linestyle='-',linewidth=2.0,marker='o',markersize=5.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='Gsi')


ax.plot(mr_ng,pos,'red',linestyle='-',linewidth=2.0,marker='o',markersize=5.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='No_gsi')
          
ax.plot(mr_rs,pos_rs,'black',linestyle='-',linewidth=2.0,marker='o',markersize=5.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='Sondae')
           
           
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.set_xticks(np.arange(min(mr_ng),max(mr_ng),0.002))

#ax.set_yticks(pos) ; yTickMarks=data_rs[:,0]

#ytickNames = ax.set_yticklabels(yTickMarks)

#plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')

ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='blue')
ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)

#leg=ax.legend(["2m,10m"],loc=1,bbox_to_anchor=(-0.3, 0.9, 1., .102),frameon=1)
#frame = leg.get_frame() ; frame.set_facecolor('white')

leg=ax.legend(loc='upper right')

ax.set_ylabel('Model Levels',color='blue',fontsize=16)
plt.title('Model levels Mixing Ratio (Kg/Kg)',color='black',fontsize=16,y=1.15)

plt.tight_layout(h_pad=3)
savefig(outFile, dpi=100);
plt.close(fig)
fig.clf(fig)










           
           
           
           
           
           
           