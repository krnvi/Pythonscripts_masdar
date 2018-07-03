import sys ;import os ; import numpy as np ; import pandas as pd ; import datetime as dt ; from dateutil import tz, rrule ; import pytz

def plot_bars(C,parm,ds ):
    import matplotlib.pyplot as plt; from pylab import savefig 

    fig=plt.figure(figsize=(20,12),dpi=50,frameon=True); ax = fig.add_subplot(111,facecolor='white')

    pos_1  = np.arange(0,14*C.shape[0],14) ; wdh=3.5 ; opacity = 1.0 ; #ax.hold(True);

    ax.bar(pos_1+wdh ,C['TMP'],width=wdh, color='g',alpha=opacity,label='temperature')


    ax.axhline(0, color="k")

    plt.tick_params(axis='y',which='both', left='on',  right='off', labelright='off')
    ax.tick_params(axis='y', colors='black',labelsize=16) ; ax.yaxis.set_ticks_position('left') ;

    #ax.set_yticks(np.arange(-10,45,10)) ; 
    ax.set_ylabel(parm,color='black',fontsize=16,fontweight='bold') ;
    ax.set_xlabel('TIME: UTC ',color='black',fontsize=16,fontweight='bold') ;

    ax.set_xticks(np.arange(0,14*C.shape[0],14)+wdh) ; 
    xTickMarks=C.index #pd.TimedeltaIndex.to_series(C.index).dt.components.hours 
    xtickNames =ax.set_xticklabels(xTickMarks,rotation=90,fontsize=14,fontweight='bold')

    #plt.tick_params(axis='x',which='both', bottom='off',  top='off', labelbottom='off')
#    for n, row in enumerate(C.iloc[:]):
#        plt.text(4*n, row, np.round(row,3), ha='center', rotation=0, va='bottom',fontsize=16,fontweight='bold')

    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2,3,4)

    leg=ax.legend(loc='lower right',fontsize=18)

    plt.tight_layout(pad=3) ;

    plt.title( '2M '+parm,fontsize=16)
    #outFile=output+'stat/corrected/dom2_'+parm1+'_'+metric+'_'+ds+'.png' 
    outFile=output+'/wyoming/'+parm+'_'+ds+'.png' 
    savefig(outFile);
    plt.close(fig) ; fig.clf(fig)
    
###########################################################################################################  

main='/home/vkvalappil/Data/oppModel' ; output=main+'/output/output/stat/' ; inp=main+'/output/output/'
date='2016050106'

date_1=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=0)
date_2=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=610)
date_list=[x.strftime('%Y%m%d%H') for x in rrule.rrule(rrule.DAILY,dtstart=date_1,until=date_2)]

obs_h=[] ;
for dte in date_list[:]:
     
    obs_file_1='/home/vkvalappil/Data/masdar_station_data/wyoming/'+dte[0:6]+'/AbuDhabi_surf_mr'+dte[0:8]+'.csv'
    obs=pd.read_csv(obs_file_1) ;
    obs['TIME']=obs['TIME'].apply(pd.to_datetime,errors='ignore')
    obs.iloc[:,3:]=obs.iloc[:,3:].apply(pd.to_numeric,errors='coerce')
    obs_1=obs.iloc[:,2:]
    obs_1.index=obs_1.TIME
    obs_1.index=obs_1.index.tz_localize(pytz.utc)
    obs_3=pd.concat([obs_1['TIME'],obs_1['TMP'],obs_1['DEW'],obs_1['RH'],obs_1['mrio'],obs_1['SPD']],axis=1)
    obs_h.append(obs_3)
    plot_bars(obs_3,'temperature',obs_3.index.strftime('%Y%m%d')[0] )    
    
    
Obs=pd.concat(obs_h,axis=0)


   
obs_mon =[g for n, g in Obs.groupby(pd.TimeGrouper('M'))]

obs_mon_hour_avg=[d.groupby(pd.to_timedelta(d.index.hour,  unit='H')).mean() for d in obs_mon]    
    
plot_bars(obs_mon_hour_avg[0],'temperature','201605' )    
plot_bars(obs_mon_hour_avg[1],'temperature','201606' )    
plot_bars(obs_mon_hour_avg[2],'temperature','201607' )    
plot_bars(obs_mon_hour_avg[3],'temperature','201608' )    
plot_bars(obs_mon_hour_avg[4],'temperature','201609' )    
plot_bars(obs_mon_hour_avg[5],'temperature','201610' )    
plot_bars(obs_mon_hour_avg[6],'temperature','201611' )    
plot_bars(obs_mon_hour_avg[7],'temperature','201612' )    
plot_bars(obs_mon_hour_avg[8],'temperature','201701' )    
plot_bars(obs_mon_hour_avg[9],'temperature','201702' )    
plot_bars(obs_mon_hour_avg[10],'temperature','201703' )    
plot_bars(obs_mon_hour_avg[11],'temperature','201704' )    
plot_bars(obs_mon_hour_avg[12],'temperature','201705' )    
plot_bars(obs_mon_hour_avg[13],'temperature','201706' )    
plot_bars(obs_mon_hour_avg[14],'temperature','201707' )    
plot_bars(obs_mon_hour_avg[15],'temperature','201708' )    
plot_bars(obs_mon_hour_avg[16],'temperature','201709' )    
plot_bars(obs_mon_hour_avg[17],'temperature','201710' )    
plot_bars(obs_mon_hour_avg[18],'temperature','201711' )    
plot_bars(obs_mon_hour_avg[19],'temperature','201712' )    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    