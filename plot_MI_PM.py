import numpy as np ;  import datetime as dt
from dateutil import rrule
import matplotlib.pyplot as plt; from pylab import * ;
from matplotlib import * ; import dateutil as du ;import seaborn as sns



A=np.genfromtxt('/home/Data/workspace/20160224.csv',delimiter=',',dtype='S')
B=A[1::12,:]

TSP=np.round(B[:,4].astype(float)).astype(int) ;PM1=np.round(B[:,5].astype(float)).astype(int) ;
PM2=np.round(B[:,6].astype(float)).astype(int); PM10=np.round(B[:,7].astype(float)).astype(int) ; Time=B[:,3]


pos  = np.arange(1,len(TSP)+1,1) ; dt=Time 

fig=plt.figure(figsize=(12,5),dpi=100); ax = fig.add_subplot(111,axisbg='darkslategray')
sns.set(style='ticks')

ax.plot(pos,PM1,'blue',linestyle='-',linewidth=2.0,marker='o',markersize=5.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='PM 1')

ax.plot(pos,PM2,'green',linestyle='-',linewidth=2.0,marker='<',markersize=5.0,\
           markeredgewidth=2.0,markerfacecolor='green',markeredgecolor='green',label='PM 2.5')
           
#ax.plot(pos,PM10,'red',linestyle='-',linewidth=2.0,marker='<',markersize=5.0,\
#           markeredgewidth=2.0,markerfacecolor='red',markeredgecolor='red',label='PM 10')           

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_yticks(np.arange(min(PM2)-3,max(PM2)+3,10.0))

ax.set_xticks(pos) ; xTickMarks=dt
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')

ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='blue')
ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)

#leg=ax.legend(["2m,10m"],loc=1,bbox_to_anchor=(-0.3, 0.9, 1., .102),frameon=1)
#frame = leg.get_frame() ; frame.set_facecolor('white')

leg=ax.legend(loc='upper right')

ax.set_ylabel('PM (ug/m3)',color='blue',fontsize=16)
plt.title('PM 1 & PM 2.5 (MI Field Station)',color='black',fontsize=16,y=1.15)

plt.tight_layout(h_pad=3)
savefig('/home/Data/workspace/MI_PM.png', dpi=100);
plt.close(fig)
fig.clf(fig)
