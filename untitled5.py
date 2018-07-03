import sys ; import numpy as np ; import datetime as dt ; import matplotlib.pyplot as plt; from pylab import * ;
from matplotlib import * ; import dateutil as du ;import seaborn as sns ; from dateutil import rrule ; from scipy.interpolate import interp1d

main='/home/vkvalappil/Data/'  ; scripts=main+'workspace/pythonscripts/' ; 
date=str(sys.argv[1]) ; 
rad_file=main+'/radiometerAnalysis/NormalDayAnalysis_Feb_28/17022800_17022805.MET.ASC' ;  
outFile=main+'/radiometerAnalysis/NormalDayAnalysis_Feb_28/17022800_17022805.MET.png'
###############################################################################################################################################################

rad_data=np.genfromtxt(rad_file,delimiter=',',dtype='S') ;   

date_1='2017022800:00:00' ; date_2='2017022805:59:59'
st_date=dt.datetime.strptime(date_1,'%Y%m%d%H:%M:%S') ; ed_date=dt.datetime.strptime(date_2,'%Y%m%d%H:%M:%S')
date_list=np.array(rad_data[:,0:6])
date_list1=([dt.datetime.strptime(x[0]+'-'+x[1]+'-'+x[2]+'-'+x[3]+'-'+x[4]+'-'+x[5],'%y - %m - %d - %H - %M - %S ') for x in date_list[:]])
date_list2=[x.strftime('%y-%m-%d-%H:%M:%S') for x in date_list1]

new_data=np.concatenate([np.vstack(date_list2),np.vstack(rad_data[:,7:])],axis=1)

indx=np.unique(new_data[:,0],return_index=True)[1] ;
new_data=new_data[indx,:] ; 

new_date_list=np.vstack([x.strftime('%y-%m-%d-%H:%M:%S') for x in rrule.rrule(rrule.SECONDLY,dtstart=st_date,until=ed_date)])

#missIndx_1=np.squeeze(np.array(np.where(~np.in1d(new_date_list[:,0],new_data[:,0]))).T)
#missIndx_2=np.squeeze(np.array(np.where(np.in1d(new_date_list[:,0],new_data[:,0]))).T)
#missTime=new_date_list[missIndx_1]
#new_data_1=np.zeros((new_date_list.shape[0],new_data.shape[1])).astype(str)
#fill_data=np.zeros((missIndx_1.shape[0],new_data.shape[1])).astype(str)
#fill_data[:,0]=np.squeeze(missTime) ; fill_data[:,1]=np.nan
#new_data_1[missIndx_1,:]=fill_data
#new_data_1[missIndx_2,:]=new_data[0:-1]

rad_ps=new_data[:,1].astype(float) ;        #new_data_1[:,1].astype(float) ; #rad_irt=rad_irt.reshape(6,60,60,1) ; m_mean=np.nanmean(rad_irt,axis=3)
#rad_date=new_data_1[:,0] ; rad_date=rad_date.reshape(24,60,1)

outFile=main+'/radiometerAnalysis/NormalDayAnalysis_Feb_28/17022800_17022805.PS.png'

fig=plt.figure(figsize=(12,10),dpi=50); ax = fig.add_subplot(111,axisbg='white')
sns.set(style='ticks') ; pos  = np.arange(1,len(rad_ps)+1,1) ;  
#ax.hold(True)
ax.plot(pos,rad_ps,'blue',linestyle='-',linewidth=2.0,marker='o',markersize=1.0,\
           markeredgewidth=1.0,markerfacecolor='blue',markeredgecolor='blue',label='Surface pressure')

ax.xaxis.set_ticks_position('bottom') ; ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_color('black') ;ax.spines['right'].set_color('black') ;
ax.spines['top'].set_color('black') ;ax.spines['left'].set_color('black') ;
   
ax.set_yticks(np.arange(min(np.round(rad_ps).astype(int))-4,max(np.round(rad_ps).astype(int))+4,2.0))
#ax.set_yticks(np.arange(5000,12000,1000.0))
#pos=np.arange(1,len(h_mean),1) ; 
x_lim=pos[::3600] ; ax.set_xticks(x_lim) ;  xTickMarks=new_date_list[::3600,0]
xtickNames = ax.set_xticklabels(xTickMarks) ; plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')

ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')
ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)

#leg=ax.legend(loc='upper right',fontsize=20)

#ax.set_ylabel('Height Levels',color='blue',fontsize=20) ;  
titl=' Surface pressure' ; plt.title(titl,color='black',fontsize=22,y=1.05)

plt.tight_layout(h_pad=3) ; 
savefig(outFile);
plt.close(fig) ; fig.clf(fig)

##################################################################################################################################

rad_ps=new_data[:,2].astype(float) ;        #new_data_1[:,1].astype(float) ; #rad_irt=rad_irt.reshape(6,60,60,1) ; m_mean=np.nanmean(rad_irt,axis=3)
#rad_date=new_data_1[:,0] ; rad_date=rad_date.reshape(24,60,1)

outFile=main+'/radiometerAnalysis/NormalDayAnalysis_Feb_28/17022800_17022805.TMP.png'

fig=plt.figure(figsize=(12,10),dpi=50); ax = fig.add_subplot(111,axisbg='white')
sns.set(style='ticks') ; pos  = np.arange(1,len(rad_ps)+1,1) ;  
#ax.hold(True)
ax.plot(pos,rad_ps,'blue',linestyle='-',linewidth=2.0,marker='o',markersize=1.0,\
           markeredgewidth=1.0,markerfacecolor='blue',markeredgecolor='blue',label='Surface Temperature')

ax.xaxis.set_ticks_position('bottom') ; ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_color('black') ;ax.spines['right'].set_color('black') ;
ax.spines['top'].set_color('black') ;ax.spines['left'].set_color('black') ;
   
ax.set_yticks(np.arange(min(np.round(rad_ps).astype(int))-4,max(np.round(rad_ps).astype(int))+4,2.0))
#ax.set_yticks(np.arange(5000,12000,1000.0))
#pos=np.arange(1,len(h_mean),1) ; 
x_lim=pos[::3600] ; ax.set_xticks(x_lim) ;  xTickMarks=new_date_list[::3600,0]
xtickNames = ax.set_xticklabels(xTickMarks) ; plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')

ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')
ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)

#leg=ax.legend(loc='upper right',fontsize=20)

#ax.set_ylabel('Height Levels',color='blue',fontsize=20) ;  
titl=' 2m Temperature' ; plt.title(titl,color='black',fontsize=22,y=1.05)

plt.tight_layout(h_pad=3) ; 
savefig(outFile);
plt.close(fig) ; fig.clf(fig)

##########################################################################################################################################

rad_ps=new_data[:,3].astype(float) ;        #new_data_1[:,1].astype(float) ; #rad_irt=rad_irt.reshape(6,60,60,1) ; m_mean=np.nanmean(rad_irt,axis=3)
#rad_date=new_data_1[:,0] ; rad_date=rad_date.reshape(24,60,1)

outFile=main+'/radiometerAnalysis/NormalDayAnalysis_Feb_28/17022800_17022805.RH.png'

fig=plt.figure(figsize=(12,10),dpi=50); ax = fig.add_subplot(111,axisbg='white')
sns.set(style='ticks') ; pos  = np.arange(1,len(rad_ps)+1,1) ;  
#ax.hold(True)
ax.plot(pos,rad_ps,'blue',linestyle='-',linewidth=2.0,marker='o',markersize=1.0,\
           markeredgewidth=1.0,markerfacecolor='blue',markeredgecolor='blue',label='Surface Relative Humidity')

ax.xaxis.set_ticks_position('bottom') ; ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_color('black') ;ax.spines['right'].set_color('black') ;
ax.spines['top'].set_color('black') ;ax.spines['left'].set_color('black') ;
   
ax.set_yticks(np.arange(min(np.round(rad_ps).astype(int))-4,max(np.round(rad_ps).astype(int))+4,2.0))
#ax.set_yticks(np.arange(5000,12000,1000.0))
#pos=np.arange(1,len(h_mean),1) ; 
x_lim=pos[::3600] ; ax.set_xticks(x_lim) ;  xTickMarks=new_date_list[::3600,0]
xtickNames = ax.set_xticklabels(xTickMarks) ; plt.setp(xtickNames, rotation=90, fontsize=10,family='sans-serif')

ax.tick_params(axis='x', colors='blue') ; ax.tick_params(axis='y', colors='blue')
ax.grid(True,which="major", linestyle='--',color='k',alpha=.3)

#leg=ax.legend(loc='upper right',fontsize=20)

#ax.set_ylabel('Height Levels',color='blue',fontsize=20) ;  
titl=' 2m Relative Humidity ' ; plt.title(titl,color='black',fontsize=22,y=1.05)

plt.tight_layout(h_pad=3) ; 
savefig(outFile);
plt.close(fig) ; fig.clf(fig)







































