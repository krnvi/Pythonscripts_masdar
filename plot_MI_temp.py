#!/usr/bin/python

import numpy as np ;  import datetime as dt
from dateutil import rrule
import matplotlib.pyplot as plt; from pylab import * ;
from matplotlib import * ; import dateutil as du ;import seaborn as sns



A=np.genfromtxt('/home/Data/workspace/wyming/MIFS_sep_hourly.csv',delimiter=',',dtype='S')

T2=np.round(A[1:49,3].astype(np.float)).astype(int) ; T10=np.round(A[1:49,4].astype(np.float)).astype(int) ; Time=A[1:49,0]

pos  = np.arange(1,len(T2)+1,1) ; dt=Time 

fig=plt.figure(figsize=(12,5),dpi=100); ax = fig.add_subplot(111,axisbg='darkslategray')
sns.set(style='ticks')

ax.plot(pos,T2,'blue',linestyle='-',linewidth=2.0,marker='o',markersize=5.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='2m')

ax.plot(pos,T10,'green',linestyle='-',linewidth=2.0,marker='<',markersize=5.0,\
           markeredgewidth=2.0,markerfacecolor='green',markeredgecolor='green',label='10m')

ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_yticks(np.arange(min(T2)-3,max(T2)+3,3.0))

ax.set_xticks(pos) ; xTickMarks=dt
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')

ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='blue')
ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)

#leg=ax.legend(["2m,10m"],loc=1,bbox_to_anchor=(-0.3, 0.9, 1., .102),frameon=1)
#frame = leg.get_frame() ; frame.set_facecolor('white')

leg=ax.legend(loc='upper right')

ax.set_ylabel('Temperature (Deg)',color='blue',fontsize=16)
plt.title('2M & 10M Temperature (MI Field Station)',color='black',fontsize=16,y=1.15)

plt.tight_layout(h_pad=3)
savefig('/home/Data/workspace/MI_temp.png', dpi=100);
plt.close(fig)
fig.clf(fig)













