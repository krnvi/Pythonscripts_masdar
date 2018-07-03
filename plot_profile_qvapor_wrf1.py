#!/usr/bin/python

import numpy as np ; import datetime as dt ; import os ;
import matplotlib.pyplot as plt; from pylab import * ;  
from matplotlib import * ; import seaborn as sns ; 
from dateutil import rrule 

main='/home/vkvalappil/Data/modelWRF/' ; scripts=main+'/scripts/' ; output=main+'ARW/output/'
date='2017011106' ; fcs_leaddays=3 ; #provide date as argument, forecast start and end date defined
fcs_st_date=dt.datetime.strptime(date,'%Y%m%d%H') ; fcs_ed_date=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=fcs_leaddays));  

file_date_list=[x.strftime('%Y-%m-%d_%H:%S:%S') for x in rrule.rrule(rrule.HOURLY,dtstart=fcs_st_date,until=fcs_ed_date)] ; #forecast start and end datelist 

for ii in range(0,len(file_date_list)):
    out_path=output+'GFS_ENKF/plots/'+date
    if not os.path.exists(out_path):    
       os.makedirs(out_path)
    outFile=out_path+'/modelLevel_gsi_nogsi_'+file_date_list[ii]+'.png'
    file_gsi=output+'GFS_ENKF/'+date+'/modelLevel_MR'+file_date_list[ii]+'.csv' ; 
    file_ngsi=output+'/no_gsi_0.25/'+date+'/modelLevel_MR'+file_date_list[ii]+'.csv' ;
    #file_rs='/home/Data/workspace/wyming/upperair/AbuBhabi_upperair_2016122012.csv'

#    data_g=np.genfromtxt(file_gsi,dtype='S',delimiter=',')[1:44,:]
#    data_ng=np.genfromtxt(file_ngsi,dtype='S',delimiter=',')[1:44,:]
#    #data_rs=np.genfromtxt(file_rs,dtype='S',delimiter=',')[2:,:]

    data_g=np.genfromtxt(file_gsi,dtype='S',delimiter=',')[1:10,:]
    data_ng=np.genfromtxt(file_ngsi,dtype='S',delimiter=',')[1:10,:]


    mr_g=data_g[:,4].astype(np.float) ; 
    mr_ng=data_ng[:,4].astype(np.float) ; 
    #mr_rs=data_rs[:,5].astype(np.float)/1000 ; 

    pos  = np.arange(0,len(mr_g),1) ; # pos_rs  = np.arange(0,len(mr_rs),1) ; 

    fig=plt.figure(figsize=(12,5),dpi=100); ax = fig.add_subplot(111,axisbg='darkslategray')
    sns.set(style='ticks')

    ax.plot(mr_g,pos,'blue',linestyle='-',linewidth=2.0,marker='o',markersize=5.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='Gsi')


    ax.plot(mr_ng,pos,'red',linestyle='-',linewidth=2.0,marker='o',markersize=5.0,\
           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='No_gsi')
          
#    ax.plot(mr_rs,pos_rs,'black',linestyle='-',linewidth=2.0,marker='o',markersize=5.0,\
#           markeredgewidth=2.0,markerfacecolor='blue',markeredgecolor='blue',label='Sondae')
#           
           
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
    titl='Model levels Mixing Ratio (Kg/Kg)'+file_date_list[ii]
    plt.title(titl,color='black',fontsize=16,y=1.15)

    plt.tight_layout(h_pad=3)
    savefig(outFile, dpi=100);
    plt.close(fig)
    fig.clf(fig)










           
           
           
           
           
           
           