#!/usr/bin/env python

import sys ; import numpy as np ; import datetime as dt ; import matplotlib.pyplot as plt; from pylab import * ;
from matplotlib import * ; import dateutil as du ;import seaborn as sns ; from dateutil import rrule ; from scipy.interpolate import interp1d

main='/home/vkvalappil/Data/'  ; scripts=main+'workspace/pythonscripts/' ; 
date=str(sys.argv[1]) ; 
rad_file=main+'/radiometerAnalysis/'+date[0:8]+'/'+date+'_TPB.csv' ;  outFile=main+'/radiometerAnalysis/'+date[0:8]+'/'+date+'_TPB.png'
###############################################################################################################################################################



rad_data=np.genfromtxt(rad_file,delimiter=',',dtype='S') ; rad_data=rad_data[:,8:].T ;  

rad_temp_1=rad_data[:,1::2].astype(float)-273.15 ; rad_temp_2=rad_data[:,2::2].astype(float)-273.15 ; rad_hgts=rad_data[:,0].astype(int)


###################################################################################################################################
fig=plt.figure(figsize=(12,10),dpi=50); ax = fig.add_subplot(111,axisbg='white')
sns.set(style='ticks') ; pos  = np.arange(0,len(rad_temp_1),1) ;  
ax.hold(True)
ax.plot(rad_temp_1,pos),'blue',linestyle='-',linewidth=2.0,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='rad_temp_1stQuad')

ax.plot(rad_temp_2,pos,'red',linestyle='-',linewidth=2.0,marker='o',markersize=2.0,\
           markeredgewidth=2.0,markerfacecolor='red',markeredgecolor='red',label='rad_temp_2ndQuad')


ax.xaxis.set_ticks_position('bottom') ; ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_color('black') ;ax.spines['right'].set_color('black') ;
ax.spines['top'].set_color('black') ;ax.spines['left'].set_color('black') ;
   
ax.set_xticks(np.arange(min(np.round(rad_temp_1.astype(int))),max(np.round(rad_temp_1.astype(int)))+10,5.0))


ax.set_yticks(pos[::4]) ; 
yTickMarks=rad_hgts[::4] ; #yTickMarks=rad_hgts
ytickNames = ax.set_yticklabels(yTickMarks,fontsize=18)
    
#plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')

ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')
ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)

#leg=ax.legend(["2m,10m"],loc=1,bbox_to_anchor=(-0.3, 0.9, 1., .102),frameon=1)
#frame = leg.get_frame() ; frame.set_facecolor('white')

leg=ax.legend(loc='upper right',fontsize=20)

ax.set_ylabel('Height Levels',color='blue',fontsize=20) ;  titl='Boundary Layer temperature (Radiometer & RadioSondae) '+date
plt.title(titl,color='black',fontsize=25,y=1.05)

#plt.tight_layout(h_pad=3) ; 
savefig(outFile);
plt.close(fig) ; fig.clf(fig)

#quit()