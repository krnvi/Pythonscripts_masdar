#!/usr/bin/python

import sys ;import os ; import numpy as np ; import pandas as pd ; import datetime as dt ; from dateutil import tz, rrule ; import pytz
import matplotlib.pyplot as plt; from pylab import savefig 

import tensorflow as tf  
from sklearn.metrics import explained_variance_score, mean_absolute_error,  median_absolute_error ,mean_squared_error
from sklearn.model_selection import train_test_split  
####################################################################################################################################

def plot_line(C,parm,parm1,ds ):
    
    fig=plt.figure(figsize=(20,12),dpi=50,frameon=True); ax1 = fig.add_subplot(111,facecolor='white')

    pos=np.arange(0,C.shape[0],1) ; opacity = 1.0 ; #ax.hold(True);

    ax1.plot(pos,C['mod'],color='b',alpha=opacity,lw=4,linestyle='-',label='Dom 2 model')
    ax1.plot(pos,C['mod_cor'],color='r',alpha=opacity,lw=4,linestyle='-',label='Dom 2 model cor')
    ax1.plot(pos,C['obs'],color='k',alpha=opacity,lw=4,linestyle='-',label='obs')

    plt.tick_params(axis='y',which='both', left='on',  right='off', labelright='off')
    ax1.tick_params(axis='y', colors='black',labelsize=16) ; ax1.yaxis.set_ticks_position('left') ;

    #ax.set_yticks(np.arange(-10,45,10)) ; 
    ax1.set_ylabel(parm,color='black',fontsize=16,fontweight='bold') ;
    ax1.set_xlabel('TIME: UTC ',color='black',fontsize=16,fontweight='bold') ;

    ax1.set_xticks(np.arange(0,C.shape[0],1)) ; 
    xTickMarks=C.index #pd.TimedeltaIndex.to_series(C.index).dt.components.hours 
    xtickNames =ax1.set_xticklabels(xTickMarks,rotation=90,fontsize=14,fontweight='bold')

    #plt.tick_params(axis='x',which='both', bottom='off',  top='off', labelbottom='off')
#    for n, row in enumerate(C.iloc[:]):
#        plt.text(4*n, row, np.round(row,3), ha='center', rotation=0, va='bottom',fontsize=16,fontweight='bold')

    handles, labels = ax1.get_legend_handles_labels()
    display = (0,1,2,3,4)

    leg=ax1.legend(loc='lower right',fontsize=18)

    plt.tight_layout(pad=3) ;

    plt.title( parm1+' : 2M '+parm,fontsize=16)
    #outFile=output+'stat/corrected/dom2_'+parm1+'_'+metric+'_'+ds+'.png' 
    outFile=output+'/corrected/corrected_rq/dom2_'+parm1+'_'+ds+'.png' 
    savefig(outFile);
    plt.close(fig) ; fig.clf(fig)

##############################################################################################################################
def plot_bars_bias(C,parm,parm1,metric,ds ):
    
    fig=plt.figure(figsize=(20,12),dpi=50,frameon=True); ax = fig.add_subplot(111,facecolor='white')

    pos_1  = np.arange(0,10*C.shape[0],10) ;   wdh=2.5 ; opacity = 1.0 ; #ax.hold(True);

    ax.bar(pos_1+wdh,C['bias_mod'],width=wdh, color='b',alpha=opacity,label='Dom 2 bias')
    ax.bar(pos_1+2*wdh ,C['bias_cor'],width=wdh, color='r',alpha=opacity,label='Dom 2 bias cor')
    ax.bar(pos_1+3*wdh ,C['bias_ba'],width=wdh, color='g',alpha=opacity,label='Dom 2 bias cor ba')


    ax.axhline(0, color="k")

    plt.tick_params(axis='y',which='both', left='on',  right='off', labelright='off')
    ax.tick_params(axis='y', colors='black',labelsize=16) ; ax.yaxis.set_ticks_position('left') ;

    #ax.set_yticks(np.arange(-10,45,10)) ; 
    ax.set_ylabel(metric,color='black',fontsize=16,fontweight='bold') ;
    ax.set_xlabel('TIME: UTC ',color='black',fontsize=16,fontweight='bold') ;

    ax.set_xticks(np.arange(0,10*C.shape[0],10)+2*wdh) ; 
    xTickMarks=C.index #pd.TimedeltaIndex.to_series(C.index).dt.components.hours 
    xtickNames =ax.set_xticklabels(xTickMarks,rotation=90,fontsize=14,fontweight='bold')

    #plt.tick_params(axis='x',which='both', bottom='off',  top='off', labelbottom='off')
#    for n, row in enumerate(C.iloc[:]):
#        plt.text(4*n, row, np.round(row,3), ha='center', rotation=0, va='bottom',fontsize=16,fontweight='bold')

    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2,3,4)

    leg=ax.legend(loc='lower right',fontsize=18)

    plt.tight_layout(pad=3) ;

    plt.title( parm1+' : 2M '+parm,fontsize=16)
    #outFile=output+'stat/corrected/dom2_'+parm1+'_'+metric+'_'+ds+'.png' 
    outFile=output+'/corrected/dom2_'+parm+'_'+parm1+'_'+metric+'_'+ds+'.png' 
    savefig(outFile);
    plt.close(fig) ; fig.clf(fig)
 ################################################################################################################
def plot_bars_rmse_hw(C,parm,parm1,metric,ds ):
    
    fig=plt.figure(figsize=(20,12),dpi=50,frameon=True); ax = fig.add_subplot(111,facecolor='white')

    pos_1  = np.arange(0,10*C.shape[0],10) ; wdh=2.5 ; opacity = 1.0 ; #ax.hold(True);

    ax.bar(pos_1+wdh,C['uc_rmse'],width=wdh, color='b',alpha=opacity,label='Dom 2 rmse')
    ax.bar(pos_1+2*wdh ,C['cor_rmse'],width=wdh, color='r',alpha=opacity,label='Dom 2 rmse cor')
    #ax.bar(pos_1+3*wdh ,C['rmse_cor_ba'],width=wdh, color='g',alpha=opacity,label='Dom 2 rmse cor ba')


    #ax.axhline(1, color="k")

    plt.tick_params(axis='y',which='both', left='on',  right='off', labelright='off')
    ax.tick_params(axis='y', colors='black',labelsize=16) ; ax.yaxis.set_ticks_position('left') ;

    #ax.set_yticks(np.arange(-10,45,10)) ; 
    ax.set_ylabel(metric,color='black',fontsize=16,fontweight='bold') ;
    ax.set_xlabel('TIME: UTC ',color='black',fontsize=16,fontweight='bold') ;

    ax.set_xticks(np.arange(0,10*C.shape[0],10)+2*wdh) ; 
    xTickMarks=C.index.strftime('%H:%S') #pd.TimedeltaIndex.to_series(C.index).dt.components.hours 
    xtickNames =ax.set_xticklabels(xTickMarks,rotation=90,fontsize=14,fontweight='bold')

    #plt.tick_params(axis='x',which='both', bottom='off',  top='off', labelbottom='off')
#    for n, row in enumerate(C.iloc[:]):
#        plt.text(4*n, row, np.round(row,3), ha='center', rotation=0, va='bottom',fontsize=16,fontweight='bold')

    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2,3,4)

    leg=ax.legend(loc='lower right',fontsize=18)

    plt.tight_layout(pad=3) ;

    plt.title( parm1+' : 2M '+parm,fontsize=16)
    outFile=output+'/corrected/corrected_rq/dom2_'+parm+'_'+parm1+'_'+metric+'_'+ds+'.png' 
    savefig(outFile);
    plt.close(fig) ; fig.clf(fig)    
##########################################################################################################################################
def plot_bars_rmse_dy(C,parm,parm1,metric,ds ):
    
    fig=plt.figure(figsize=(20,12),dpi=50,frameon=True); ax = fig.add_subplot(111,facecolor='white')

    pos_1  = np.arange(0,10*C.shape[0],10) ; wdh=2.5 ; opacity = 1.0 ; #ax.hold(True);

    ax.bar(pos_1+wdh,C['uc_rmse'],width=wdh, color='b',alpha=opacity,label='Dom 2 rmse')
    ax.bar(pos_1+2*wdh ,C['cor_rmse'],width=wdh, color='r',alpha=opacity,label='Dom 2 rmse cor')
    #ax.bar(pos_1+3*wdh ,C['rmse_cor_ba'],width=wdh, color='g',alpha=opacity,label='Dom 2 rmse cor ba')

    #ax.axhline(1, color="k")

    plt.tick_params(axis='y',which='both', left='on',  right='off', labelright='off')
    ax.tick_params(axis='y', colors='black',labelsize=16) ; ax.yaxis.set_ticks_position('left') ;

    #ax.set_yticks(np.arange(-10,45,10)) ; 
    ax.set_ylabel(metric,color='black',fontsize=16,fontweight='bold') ;
    ax.set_xlabel('TIME: UTC ',color='black',fontsize=16,fontweight='bold') ;

    ax.set_xticks(np.arange(0,10*C.shape[0],10)+2*wdh) ; 
    xTickMarks=C.index.strftime('%Y%m%d') #pd.TimedeltaIndex.to_series(C.index).dt.components.hours 
    xtickNames =ax.set_xticklabels(xTickMarks,rotation=90,fontsize=14,fontweight='bold')

    #plt.tick_params(axis='x',which='both', bottom='off',  top='off', labelbottom='off')
#    for n, row in enumerate(C.iloc[:]):
#        plt.text(4*n, row, np.round(row,3), ha='center', rotation=0, va='bottom',fontsize=16,fontweight='bold')

    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2,3,4)

    leg=ax.legend(loc='lower right',fontsize=18)

    plt.tight_layout(pad=3) ;

    plt.title( parm1+' : 2M '+parm,fontsize=16)
    outFile=output+'/corrected/corrected_rq/dom2_'+parm+'_'+parm1+'_'+metric+'_'+ds+'.png' 
    savefig(outFile);
    plt.close(fig) ; fig.clf(fig)   
    
##########################################################################################################################################
main='/home/vkvalappil/Data/oppModel' ; output=main+'/output/output/stat/' ; inp=main+'/output/output/'
date='2017051506'

date_1=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=0)
date_2=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=389)
date_list=[x.strftime('%Y%m%d%H') for x in rrule.rrule(rrule.DAILY,dtstart=date_1,until=date_2)]

bias_day1 = [] ; bias_day1_cor = [] 
rmse_day1 = [] ; rmse_day1_cor = [] ;
bias_day2 = [] ; bias_day2_cor = [] ;
rmse_day2 = [] ; rmse_day2_cor = [] ;
bias_hour_day1=[] ; bias_hour_day1_cor=[] ;
bias_hour_day2=[] ; bias_hour_day2_cor=[] ;

mod_hour_day1=[] ; mod_hour_day1_cor=[]
obs_hour_day1=[] ; 
mod_hour_day2=[] ; mod_hour_day2_cor=[]
obs_hour_day2=[] ;

for dte in date_list[:]:
    
    file_2=inp+'domain_2/surfaceLevel/hourly'+dte+'.csv'
    if (os.path.isfile(file_2)):
        
        mod_dom_2_fcst=pd.read_csv(file_2) ; #mod_dom_2_fcst=mod_dom_2_fcst.iloc[72:144,:] ;         
        mod_dom_2_fcst['localTime']=mod_dom_2_fcst['localTime'].apply(pd.to_datetime, errors='ignore')    
        mod_dom_2_fcst.iloc[:,4:]=mod_dom_2_fcst.iloc[:,4:].apply(pd.to_numeric,errors='coerce')
        mod_dom_2_1_fcst=mod_dom_2_fcst.iloc[:,3:] 
        mod_dom_2_1_fcst.index=mod_dom_2_1_fcst.localTime
        
        mod_dom_2_1_fcst.index=mod_dom_2_1_fcst.index.tz_localize(pytz.timezone('Asia/Dubai')).tz_convert(pytz.utc)
        mod_dom_2_1_fcst['localTime']=mod_dom_2_1_fcst.index
          
################################################################################################
        no_lag_days=10
        
        dte_1=dt.datetime.strptime(dte,'%Y%m%d%H')+dt.timedelta(days=-no_lag_days)
        dte_2=dt.datetime.strptime(dte,'%Y%m%d%H')+dt.timedelta(days=-1)      
        date_req_list=[x.strftime('%Y%m%d%H') for x in rrule.rrule(rrule.DAILY,dtstart=dte_1,until=dte_2)]
        obs_mod=[]
        for dte1 in date_req_list[:]:
            file_2=inp+'domain_2/surfaceLevel/hourly'+dte1+'.csv'
            if (os.path.isfile(file_2)):
                
                mod_dom_2=pd.read_csv(file_2) ; #mod_dom_2=mod_dom_2.iloc[72:144,:] ; 
                o_date_1=dte1 ;          
                o_date_2=(dt.datetime.strptime(dte1,'%Y%m%d%H')+dt.timedelta(days=1)).strftime('%Y%m%d%H')
                o_date_3=(dt.datetime.strptime(dte1,'%Y%m%d%H')+dt.timedelta(days=2)).strftime('%Y%m%d%H')
                o_date_4=(dt.datetime.strptime(dte1,'%Y%m%d%H')+dt.timedelta(days=3)).strftime('%Y%m%d%H')        
          
                obs_file_1='/home/vkvalappil/Data/masdar_station_data/wyoming/'+o_date_1[0:6]+'/AbuDhabi_surf_mr'+o_date_1[0:8]+'.csv'
                obs_file_2='/home/vkvalappil/Data/masdar_station_data/wyoming/'+o_date_2[0:6]+'/AbuDhabi_surf_mr'+o_date_2[0:8]+'.csv'
                obs_file_3='/home/vkvalappil/Data/masdar_station_data/wyoming/'+o_date_3[0:6]+'/AbuDhabi_surf_mr'+o_date_3[0:8]+'.csv'
                obs_file_4='/home/vkvalappil/Data/masdar_station_data/wyoming/'+o_date_4[0:6]+'/AbuDhabi_surf_mr'+o_date_4[0:8]+'.csv'
        
                mod_dom_2['localTime']=mod_dom_2['localTime'].apply(pd.to_datetime, errors='ignore')    
                mod_dom_2.iloc[:,4:]=mod_dom_2.iloc[:,4:].apply(pd.to_numeric,errors='coerce')
                mod_dom_2_1=mod_dom_2.iloc[:,3:]
                mod_dom_2_1.index=mod_dom_2_1.localTime
                mod_dom_2_1.index=mod_dom_2_1.index.tz_localize(pytz.timezone('Asia/Dubai')).tz_convert(pytz.utc)
                mod_dom_2_1['localTime']=mod_dom_2_1.index
        
                obs_1=pd.read_csv(obs_file_1) ; obs_2=pd.read_csv(obs_file_2) ; obs_3=pd.read_csv(obs_file_3) ; obs_4=pd.read_csv(obs_file_4)
                obs=pd.concat([obs_1,obs_2,obs_3,obs_4],axis=0)
    
                obs['TIME']=obs['TIME'].apply(pd.to_datetime,errors='ignore')
                obs.iloc[:,3:]=obs.iloc[:,3:].apply(pd.to_numeric,errors='coerce')
                obs_1=obs.iloc[:,2:]
                obs_1.index=obs_1.TIME
                obs_1.index=obs_1.index.tz_localize(pytz.utc)
  
                idx = obs_1.index.intersection(mod_dom_2_1.index)
                obs_2=obs_1.loc[idx]
                obs_3=pd.concat([obs_2['TIME'],obs_2['TMP'],obs_2['DEW'],obs_2['RH'],obs_2['mrio'],obs_2['SPD']],axis=1)
                obs_3.columns=['TIME','OTMP','ODEW','ORH','OMRIO','OSPD']
                
                mod_dom_2_2=pd.concat([mod_dom_2_1['localTime'],mod_dom_2_1['TEMP'],mod_dom_2_1['DTEMP'],mod_dom_2_1['RH'],mod_dom_2_1['MXRATIO'],mod_dom_2_1['WDIR']*0.277],axis=1)    
                mod_dom_2_2.columns=['localTime','MTMP','MDEW','MRH','MMRIO','MSPD']
                
                mod_obs_1=pd.concat([mod_dom_2_2,obs_3],axis=1).iloc[0:31,:]                 
                obs_mod.append(mod_obs_1)
            else :   
               print(dte)
               print("No Data Exist")
               
        obs_mod=pd.concat(obs_mod,axis=0) 
################################################################################################################################        
        d_t_1=(dt.datetime.strptime(date_req_list[0],'%Y%m%d%H')).strftime('%Y-%m-%d %H') ; 
        d_t_2=(dt.datetime.strptime(date_req_list[-1],'%Y%m%d%H')).strftime('%Y-%m-%d') ; 
        
        d_t_3=(dt.datetime.strptime(dte,'%Y%m%d%H')).strftime('%Y-%m-%d %H') ; 
        
        obs_mod_train=obs_mod[d_t_1:d_t_3] ; obs_mod_test=mod_dom_2_1_fcst[0:31] 
        
        hourt = pd.to_timedelta(obs_mod_train.index.hour,  unit='H')
        obs_mod_train_hour_sum_day1=obs_mod_train.groupby(hourt).sum() 

        a = obs_mod_train_hour_sum_day1.values ; 
        obs_mod_q = a[:,5:]/a[:,0:5].astype(str).astype(float)
        obs_mod_q=pd.DataFrame(obs_mod_q)
        obs_mod_q.columns=obs_mod_train_hour_sum_day1.columns[0:5]
        obs_mod_q.index=obs_mod_train_hour_sum_day1.index        

        #a = obs_mod_train.values ; 
        #obs_mod_q = a[:,7:]/a[:,1:6].astype(str).astype(float)
        #obs_mod_q=pd.DataFrame(obs_mod_q)
        #obs_mod_q.columns=obs_mod_train.columns[1:6]
        #obs_mod_q.index=obs_mod_train.index
        
        obs_mod_q_1=pd.concat([obs_mod_q.iloc[6:],obs_mod_q[0:6]],axis=0)  # ratio matrix for obs and model
        obs_mod_q_2=pd.concat([obs_mod_q_1]*3)          


        mod_dom_2_1_fcst_1=pd.concat([mod_dom_2_1_fcst.iloc[0:,2:5],mod_dom_2_1_fcst.iloc[0:,7],mod_dom_2_1_fcst.iloc[0:,10]],axis=1)

        mod_dom_2_1_fcst_2=pd.DataFrame(obs_mod_q_2.values*mod_dom_2_1_fcst_1.values, columns=mod_dom_2_1_fcst_1.columns, index=mod_dom_2_1_fcst_1.index)

        mod_dom_2_1_fcst_2.insert(0,'Date',mod_dom_2_1_fcst_1.index)           #corrected forecast
             
####################################################################################################################################
        o_date_1=dte ; 
        o_date_2=(dt.datetime.strptime(dte,'%Y%m%d%H')+dt.timedelta(days=1)).strftime('%Y%m%d%H')
        o_date_3=(dt.datetime.strptime(dte,'%Y%m%d%H')+dt.timedelta(days=2)).strftime('%Y%m%d%H')
        o_date_4=(dt.datetime.strptime(dte,'%Y%m%d%H')+dt.timedelta(days=3)).strftime('%Y%m%d%H')
    
        obs_file_1='/home/vkvalappil/Data/masdar_station_data/wyoming/'+o_date_1[0:6]+'/AbuDhabi_surf_mr'+o_date_1[0:8]+'.csv'
        obs_file_2='/home/vkvalappil/Data/masdar_station_data/wyoming/'+o_date_2[0:6]+'/AbuDhabi_surf_mr'+o_date_2[0:8]+'.csv'
        obs_file_3='/home/vkvalappil/Data/masdar_station_data/wyoming/'+o_date_3[0:6]+'/AbuDhabi_surf_mr'+o_date_3[0:8]+'.csv'
        obs_file_4='/home/vkvalappil/Data/masdar_station_data/wyoming/'+o_date_4[0:6]+'/AbuDhabi_surf_mr'+o_date_4[0:8]+'.csv'
        
        obs_1=pd.read_csv(obs_file_1) ; obs_2=pd.read_csv(obs_file_2) ; obs_3=pd.read_csv(obs_file_3) ; obs_4=pd.read_csv(obs_file_4)
        obs=pd.concat([obs_1,obs_2,obs_3,obs_4],axis=0)
    
        obs['TIME']=obs['TIME'].apply(pd.to_datetime,errors='ignore')
        obs.iloc[:,3:]=obs.iloc[:,3:].apply(pd.to_numeric,errors='coerce')
        obs_1=obs.iloc[:,2:]
        obs_1.index=obs_1.TIME
        obs_1.index=obs_1.index.tz_localize(pytz.utc)
  
        idx = obs_1.index.intersection(mod_dom_2_1_fcst.index)
        obs_2=obs_1.loc[idx]
        obs_3=pd.concat([obs_2['TIME'],obs_2['TMP'],obs_2['DEW'],obs_2['RH'],obs_2['mrio'],obs_2['SPD']],axis=1)
#####################################################################################################################################################

#        mod_dom_2_2=pd.concat([mod_dom_2_1_fcst['localTime'],mod_dom_2_1_fcst['TEMP'],mod_dom_2_1_fcst['DTEMP'],\
#                                mod_dom_2_1_fcst['RH'],mod_dom_2_1_fcst['MXRATIO'],mod_dom_2_1_fcst['WDIR']*0.277],axis=1)  # Raw model forecast  

        mod_dom_2_2=pd.concat([mod_dom_2_1_fcst['localTime'],mod_dom_2_1_fcst_1],axis=1)
        mod_dom_2_2.columns=obs_3.columns  
        mod_dom_2_1_fcst_2.columns=obs_3.columns
        
################################### Calculating Daily bias and daily rmse ############################################################################
        p_data=pd.concat([mod_dom_2_1_fcst_2['TIME'],np.round(mod_dom_2_1_fcst_2['TMP']),mod_dom_2_2['TMP'],obs_3['TMP']],axis=1)
        p_data.columns=['Date','mod_cor','mod','obs']
        #plot_line(p_data.iloc[7:31,:],'Temperature','Temperature',dte[0:8])

        ##### Day 1
        mod_dom_2_bias_1=mod_dom_2_2.iloc[7:31,1:].sub(obs_3.iloc[7:31,1:],axis=0)                     #### Raw Model
        
        mod_dom_2_bias_1_cor=mod_dom_2_1_fcst_2.iloc[7:31,1:].sub(obs_3.iloc[7:31,1:],axis=0)          #### corrected 
         
        mod_dom_2_rmse_1=((mod_dom_2_bias_1**2).mean(axis=0))**0.5                                     #### raw model 
        
        mod_dom_2_rmse_1_cor=((mod_dom_2_bias_1_cor**2).mean(axis=0))**0.5                             #### corrected

        ##### Day2
        
        mod_dom_2_bias_2=mod_dom_2_2.iloc[31:55,1:].sub(obs_3.iloc[31:55,1:],axis=0)      
        mod_dom_2_bias_2_cor= mod_dom_2_1_fcst_2.iloc[31:55,1:].sub(obs_3.iloc[31:55,1:],axis=0)      

        mod_dom_2_rmse_2=((mod_dom_2_bias_2**2).mean(axis=0))**0.5
        mod_dom_2_rmse_2_cor=((mod_dom_2_bias_2_cor**2).mean(axis=0))**0.5

##################################################################################################        

        bias_day_1=np.vstack(mod_dom_2_bias_1.mean(axis=0).values).T
        bias_day_1=pd.DataFrame(bias_day_1,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])
        bias_day_1.insert(0,'Date',dte)

        rmse_day_1=np.vstack(mod_dom_2_rmse_1.values).T
        rmse_day_1=pd.DataFrame(rmse_day_1,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])
        rmse_day_1.insert(0,'Date',dte)  

        bias_day1.append(bias_day_1) ;     rmse_day1.append(rmse_day_1) ####### daily bias day wise appended day1

############## correction 
        bias_day_1_cor=np.vstack(mod_dom_2_bias_1_cor.mean(axis=0).values).T
        bias_day_1_cor=pd.DataFrame(bias_day_1_cor,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])
        bias_day_1_cor.insert(0,'Date',dte)

        rmse_day_1_cor=np.vstack(mod_dom_2_rmse_1_cor.values).T
        rmse_day_1_cor=pd.DataFrame(rmse_day_1_cor,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])
        rmse_day_1_cor.insert(0,'Date',dte)  

        bias_day1_cor.append(bias_day_1_cor) ;     rmse_day1_cor.append(rmse_day_1_cor) ####### daily bias day wise appended day1
       
##############                
        bias_hour_day1.append(mod_dom_2_bias_1)  ####### hourly bias appended for each day day1
        mod_hour_day1.append(mod_dom_2_2.iloc[7:31,1:]) ;  obs_hour_day1.append(obs_3.iloc[7:31,1:])

        bias_hour_day1_cor.append(mod_dom_2_bias_1_cor)  ####### hourly bias appended for each day day1
        mod_hour_day1_cor.append( mod_dom_2_1_fcst_2.iloc[7:31,1:]) ;   

####################################     
        bias_day_2=np.vstack(mod_dom_2_bias_2.mean(axis=0).values).T

        bias_day_2=pd.DataFrame(bias_day_2,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])

        bias_day_2.insert(0,'Date',dte)

        rmse_day_2=np.vstack(mod_dom_2_rmse_2.values).T 
        
        rmse_day_2=pd.DataFrame(rmse_day_2,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])

        rmse_day_2.insert(0,'Date',dte)

        bias_day2.append(bias_day_2) ; rmse_day2.append(rmse_day_2) ## daily bias day wise appended day2
##########################
        bias_day_2_cor=np.vstack(mod_dom_2_bias_2_cor.mean(axis=0).values).T

        bias_day_2_cor=pd.DataFrame(bias_day_2_cor,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])

        bias_day_2_cor.insert(0,'Date',dte)

        rmse_day_2_cor=np.vstack(mod_dom_2_rmse_2_cor.values).T 
        
        rmse_day_2_cor=pd.DataFrame(rmse_day_2_cor,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])

        rmse_day_2_cor.insert(0,'Date',dte)

        bias_day2_cor.append(bias_day_2_cor) ; rmse_day2_cor.append(rmse_day_2_cor) ## daily bias day wise appended day2

##############################

        bias_hour_day2.append(mod_dom_2_bias_2)  ## hourly bias appended for each day day2
        mod_hour_day2.append(mod_dom_2_2.iloc[31:55,1:]) ;  obs_hour_day2.append(obs_3.iloc[31:55,1:])       

        bias_hour_day2_cor.append(mod_dom_2_bias_2_cor)  ## hourly bias appended for each day day2
        mod_hour_day2_cor.append(mod_dom_2_1_fcst_2.iloc[31:55,1:]) ;  obs_hour_day2.append(obs_3.iloc[31:55,1:])       
    
    else:
       print (dte) 
       print("No Data Exist")

################################### hourly Analysis ######################################################################### 
bias_hour_day_1=pd.concat(bias_hour_day1,axis=0) ; bias_hour_day_2=pd.concat(bias_hour_day2,axis=0)
mod_hour_day_1=pd.concat(mod_hour_day1,axis=0)   ; mod_hour_day_2=pd.concat(mod_hour_day2,axis=0)   ;
obs_hour_day_1=pd.concat(obs_hour_day1,axis=0)   ; mod_hour_day_2=pd.concat(mod_hour_day2,axis=0)   ;

bias_hour_day_1_cor=pd.concat(bias_hour_day1_cor,axis=0) ; bias_hour_day_2_cor=pd.concat(bias_hour_day2_cor,axis=0)
mod_hour_day_1_cor=pd.concat(mod_hour_day1_cor,axis=0)   ; mod_hour_day_2_cor=pd.concat(mod_hour_day2_cor,axis=0)   ; 

##############################################################################################

day_1_rmse=pd.concat(rmse_day1,axis=0) ; day_1_rmse_cor=pd.concat(rmse_day1_cor,axis=0)
day_2_rmse=pd.concat(rmse_day2,axis=0) ; day_2_rmse_cor=pd.concat(rmse_day2_cor,axis=0)

if ((obs_hour_day_1.index==mod_hour_day_1_cor.index).all()) & ((obs_hour_day_1.index==mod_hour_day_1.index).all()) :

    tmp_mod_cor_obs=pd.concat([obs_hour_day_1['TMP'],mod_hour_day_1['TMP'],bias_hour_day_1['TMP'],mod_hour_day_1_cor['TMP'],bias_hour_day_1_cor['TMP']],axis=1)
    tmp_mod_cor_obs.columns=['obs_tmp','uc_mod','uc_bias','cor_mod','cor_bias']
    tmp_mod_cor_obs.index=obs_hour_day_1.index

    mr_mod_cor_obs=pd.concat([obs_hour_day_1['mrio'],mod_hour_day_1['mrio'],bias_hour_day_1['mrio'],mod_hour_day_1_cor['mrio'],bias_hour_day_1_cor['mrio']],axis=1)
    mr_mod_cor_obs.columns=['obs_mr','uc_mod','uc_bias','cor_mod','cor_bias']
    mr_mod_cor_obs.index=obs_hour_day_1.index

    rh_mod_cor_obs=pd.concat([obs_hour_day_1['RH'],mod_hour_day_1['RH'],bias_hour_day_1['RH'],mod_hour_day_1_cor['RH'],bias_hour_day_1_cor['RH']],axis=1)
    rh_mod_cor_obs.columns=['obs_mr','uc_mod','uc_bias','cor_mod','cor_bias']
    rh_mod_cor_obs.index=obs_hour_day_1.index

####################### Winter data segregation #################################################################################
tmp_hour_day1_winter=tmp_mod_cor_obs['2017-11-01':'2018-03-31'] 
hourt = pd.to_timedelta(tmp_hour_day1_winter.index.hour,  unit='H')
mf=int(tmp_hour_day1_winter.shape[0]/24.0)

uc_tmp_rmse_hour_avg_day1_winter=(((tmp_hour_day1_winter['uc_bias']**2).groupby(hourt)).mean())**0.5
uc_tmp_rmse_hour_avg_day1_winter=pd.concat([uc_tmp_rmse_hour_avg_day1_winter]*mf)
uc_tmp_rmse_hour_avg_day1_winter.index=tmp_hour_day1_winter.index

cor_tmp_rmse_hour_avg_day1_winter=(((tmp_hour_day1_winter['cor_bias']**2).groupby(hourt)).mean())**0.5
cor_tmp_rmse_hour_avg_day1_winter=pd.concat([cor_tmp_rmse_hour_avg_day1_winter]*mf)
cor_tmp_rmse_hour_avg_day1_winter.index=tmp_hour_day1_winter.index

tmp_hour_day1_winter.insert(3,'uc_rmse',uc_tmp_rmse_hour_avg_day1_winter)
tmp_hour_day1_winter.insert(6,'cor_rmse',cor_tmp_rmse_hour_avg_day1_winter)

###########################################################################################################
mr_hour_day1_winter=mr_mod_cor_obs['2017-11-01':'2018-03-31'] 
hourt = pd.to_timedelta(mr_hour_day1_winter.index.hour,  unit='H')
mf=int(mr_hour_day1_winter.shape[0]/24.0)

uc_mr_rmse_hour_avg_day1_winter=(((mr_hour_day1_winter['uc_bias']**2).groupby(hourt)).mean())**0.5
uc_mr_rmse_hour_avg_day1_winter=pd.concat([uc_mr_rmse_hour_avg_day1_winter]*mf)
uc_mr_rmse_hour_avg_day1_winter.index=mr_hour_day1_winter.index

cor_mr_rmse_hour_avg_day1_winter=(((mr_hour_day1_winter['cor_bias']**2).groupby(hourt)).mean())**0.5
cor_mr_rmse_hour_avg_day1_winter=pd.concat([cor_mr_rmse_hour_avg_day1_winter]*mf)
cor_mr_rmse_hour_avg_day1_winter.index=mr_hour_day1_winter.index

mr_hour_day1_winter.insert(3,'uc_rmse',uc_mr_rmse_hour_avg_day1_winter)
mr_hour_day1_winter.insert(6,'cor_rmse',cor_mr_rmse_hour_avg_day1_winter)

###################################################################################################################

rh_hour_day1_winter=rh_mod_cor_obs['2017-11-01':'2018-03-31'] 
hourt = pd.to_timedelta(rh_hour_day1_winter.index.hour,  unit='H')
mf=int(rh_hour_day1_winter.shape[0]/24.0)

uc_rh_rmse_hour_avg_day1_winter=(((rh_hour_day1_winter['uc_bias']**2).groupby(hourt)).mean())**0.5
uc_rh_rmse_hour_avg_day1_winter=pd.concat([uc_rh_rmse_hour_avg_day1_winter]*mf)
uc_rh_rmse_hour_avg_day1_winter.index=rh_hour_day1_winter.index

cor_rh_rmse_hour_avg_day1_winter=(((rh_hour_day1_winter['cor_bias']**2).groupby(hourt)).mean())**0.5
cor_rh_rmse_hour_avg_day1_winter=pd.concat([cor_rh_rmse_hour_avg_day1_winter]*mf)
cor_rh_rmse_hour_avg_day1_winter.index=rh_hour_day1_winter.index

rh_hour_day1_winter.insert(3,'uc_rmse',uc_rh_rmse_hour_avg_day1_winter)
rh_hour_day1_winter.insert(6,'cor_rmse',cor_rh_rmse_hour_avg_day1_winter)


####################### Summer data segregation #################################################################################
tmp_hour_day1_summer=pd.concat([tmp_mod_cor_obs['2017-05-01':'2017-10-31'],tmp_mod_cor_obs['2018-04-01':'2018-06-30']],axis=0)

hourt = pd.to_timedelta(tmp_hour_day1_summer.index.hour,  unit='H')
mf=int(tmp_hour_day1_summer.shape[0]/24.0)

uc_tmp_rmse_hour_avg_day1_summer=(((tmp_hour_day1_summer['uc_bias']**2).groupby(hourt)).mean())**0.5
uc_tmp_rmse_hour_avg_day1_summer=pd.concat([uc_tmp_rmse_hour_avg_day1_summer[13:24],uc_tmp_rmse_hour_avg_day1_summer[0:13]])
uc_tmp_rmse_hour_avg_day1_summer=pd.concat([uc_tmp_rmse_hour_avg_day1_summer]*mf)
uc_tmp_rmse_hour_avg_day1_summer.index=tmp_hour_day1_summer.index

cor_tmp_rmse_hour_avg_day1_summer=(((tmp_hour_day1_summer['cor_bias']**2).groupby(hourt)).mean())**0.5
cor_tmp_rmse_hour_avg_day1_summer=pd.concat([cor_tmp_rmse_hour_avg_day1_summer[13:24],cor_tmp_rmse_hour_avg_day1_summer[0:13]])
cor_tmp_rmse_hour_avg_day1_summer=pd.concat([cor_tmp_rmse_hour_avg_day1_summer]*mf)
cor_tmp_rmse_hour_avg_day1_summer.index=tmp_hour_day1_summer.index

tmp_hour_day1_summer.insert(3,'uc_rmse',uc_tmp_rmse_hour_avg_day1_summer)
tmp_hour_day1_summer.insert(6,'cor_rmse',cor_tmp_rmse_hour_avg_day1_summer)

#######################################################################################################################################
mr_hour_day1_summer=pd.concat([mr_mod_cor_obs['2017-05-01':'2017-10-31'],mr_mod_cor_obs['2018-04-01':'2018-06-30']],axis=0)

hourt = pd.to_timedelta(mr_hour_day1_summer.index.hour,  unit='H')
mf=int(mr_hour_day1_summer.shape[0]/24.0)

uc_mr_rmse_hour_avg_day1_summer=(((mr_hour_day1_summer['uc_bias']**2).groupby(hourt)).mean())**0.5
uc_mr_rmse_hour_avg_day1_summer=pd.concat([uc_mr_rmse_hour_avg_day1_summer[13:24],uc_mr_rmse_hour_avg_day1_summer[0:13]])
uc_mr_rmse_hour_avg_day1_summer=pd.concat([uc_mr_rmse_hour_avg_day1_summer]*mf)
uc_mr_rmse_hour_avg_day1_summer.index=mr_hour_day1_summer.index

cor_mr_rmse_hour_avg_day1_summer=(((mr_hour_day1_summer['cor_bias']**2).groupby(hourt)).mean())**0.5
cor_mr_rmse_hour_avg_day1_summer=pd.concat([cor_mr_rmse_hour_avg_day1_summer[13:24],cor_mr_rmse_hour_avg_day1_summer[0:13]])
cor_mr_rmse_hour_avg_day1_summer=pd.concat([cor_mr_rmse_hour_avg_day1_summer]*mf)
cor_mr_rmse_hour_avg_day1_summer.index=mr_hour_day1_summer.index

mr_hour_day1_summer.insert(3,'uc_rmse',uc_mr_rmse_hour_avg_day1_summer)
mr_hour_day1_summer.insert(6,'cor_rmse',cor_mr_rmse_hour_avg_day1_summer)
########################################################################################################################################
rh_hour_day1_summer=pd.concat([rh_mod_cor_obs['2017-05-01':'2017-10-31'],rh_mod_cor_obs['2018-04-01':'2018-06-30']],axis=0)

hourt = pd.to_timedelta(rh_hour_day1_summer.index.hour,  unit='H')
mf=int(rh_hour_day1_summer.shape[0]/24.0)

uc_rh_rmse_hour_avg_day1_summer=(((rh_hour_day1_summer['uc_bias']**2).groupby(hourt)).mean())**0.5
uc_rh_rmse_hour_avg_day1_summer=pd.concat([uc_rh_rmse_hour_avg_day1_summer[13:24],uc_rh_rmse_hour_avg_day1_summer[0:13]])
uc_rh_rmse_hour_avg_day1_summer=pd.concat([uc_rh_rmse_hour_avg_day1_summer]*mf)
uc_rh_rmse_hour_avg_day1_summer.index=rh_hour_day1_summer.index

cor_rh_rmse_hour_avg_day1_summer=(((rh_hour_day1_summer['cor_bias']**2).groupby(hourt)).mean())**0.5
cor_rh_rmse_hour_avg_day1_summer=pd.concat([cor_rh_rmse_hour_avg_day1_summer[13:24],cor_rh_rmse_hour_avg_day1_summer[0:13]])
cor_rh_rmse_hour_avg_day1_summer=pd.concat([cor_rh_rmse_hour_avg_day1_summer]*mf)
cor_rh_rmse_hour_avg_day1_summer.index=rh_hour_day1_summer.index

rh_hour_day1_summer.insert(3,'uc_rmse',uc_rh_rmse_hour_avg_day1_summer)
rh_hour_day1_summer.insert(6,'cor_rmse',cor_rh_rmse_hour_avg_day1_summer)


#######################################################################################################################################
tmp_hour_day1_summer.to_csv('/home/vkvalappil/Data/oppModel/output/output/stat/corrected/corrected_rq/tmp_obs_mod_cor_uc_summer.csv')
tmp_hour_day1_winter.to_csv('/home/vkvalappil/Data/oppModel/output/output/stat/corrected/corrected_rq/tmp_obs_mod_cor_uc_winter.csv')

plot_bars_rmse_hw(tmp_hour_day1_winter.iloc[0:24,:],'Temperature','Hour_wise','RMSE','Winter' )
plot_bars_rmse_hw(tmp_hour_day1_summer.iloc[11:34,:],'Temperature','Hour_wise','RMSE','Summer' )


mr_hour_day1_summer.to_csv('/home/vkvalappil/Data/oppModel/output/output/stat/corrected/corrected_rq/mr_obs_mod_cor_uc_summer.csv')
mr_hour_day1_winter.to_csv('/home/vkvalappil/Data/oppModel/output/output/stat/corrected/corrected_rq/mr_obs_mod_cor_uc_winter.csv')

plot_bars_rmse_hw(mr_hour_day1_winter.iloc[0:24,:],'Mixingratio','Hour_wise','RMSE','Winter' )
plot_bars_rmse_hw(mr_hour_day1_summer.iloc[11:34,:],'Mixingratio','Hour_wise','RMSE','Summer' )

rh_hour_day1_summer.to_csv('/home/vkvalappil/Data/oppModel/output/output/stat/corrected/corrected_rq/rh_obs_mod_cor_uc_summer.csv')
rh_hour_day1_winter.to_csv('/home/vkvalappil/Data/oppModel/output/output/stat/corrected/corrected_rq/rh_obs_mod_cor_uc_winter.csv')

plot_bars_rmse_hw(rh_hour_day1_winter.iloc[0:24,:],'Rh','Hour_wise','RMSE','Winter' )
plot_bars_rmse_hw(rh_hour_day1_summer.iloc[11:34,:],'Rh','Hour_wise','RMSE','Summer' )

################################### Day Wise ########################################################################
day_1_bias=pd.concat(bias_day1,axis=0) ; day_1_bias_cor=pd.concat(bias_day1_cor,axis=0) ; 
day_2_bias=pd.concat(bias_day2,axis=0) ; day_2_bias_cor=pd.concat(bias_day2_cor,axis=0) ; 
#####################################################################################################################
tmp_bias=pd.concat([day_1_bias['tmp_02'],day_1_bias_cor['tmp_02']],axis=1)
tmp_bias.columns=['mod','cor']
tmp_bias.insert(0,'Date',day_1_bias.Date)                 
tmp_bias['Date']=tmp_bias['Date'].apply(pd.to_datetime,errors='coerce',format='%Y%m%d%H') 
tmp_bias.index=tmp_bias.Date
####################
tmp_rmse=pd.concat([day_1_rmse['tmp_02'],day_1_rmse_cor['tmp_02']],axis=1)
tmp_rmse.columns=['mod','cor']
tmp_rmse.insert(0,'Date',day_1_rmse.Date)                 
tmp_rmse['Date']=tmp_rmse['Date'].apply(pd.to_datetime,errors='coerce',format='%Y%m%d%H') 
tmp_rmse.index=tmp_bias.Date

tmp_daymean_bias_rmse=pd.concat([tmp_bias,tmp_rmse['mod'],tmp_rmse['cor']],axis=1)
tmp_daymean_bias_rmse.columns=['Date','uc_bias','cor_bias','uc_rmse','cor_rmse']
tmp_daymean_bias_rmse.to_csv('/home/vkvalappil/Data/oppModel/output/output/stat/corrected/corrected_rq/tmp_obs_mod_cor_uc_dailymean.csv',index=False)

dt_1='2017-05-01' ; dt_2='2017-05-31'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-06-01' ; dt_2='2017-06-30'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-07-01' ; dt_2='2017-07-31'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-08-01' ; dt_2='2017-08-31'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-09-01' ; dt_2='2017-09-30'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-10-01' ; dt_2='2017-10-31'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-11-01' ; dt_2='2017-11-30'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-12-01' ; dt_2='2017-12-31'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-01-01' ; dt_2='2018-01-31'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-02-01' ; dt_2='2018-02-28'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-03-01' ; dt_2='2018-03-31'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-04-01' ; dt_2='2018-04-30'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-05-01' ; dt_2='2018-05-31'
plot_bars_rmse_dy(tmp_daymean_bias_rmse[dt_1:dt_2],'Temperature','Day_wise','RMSE',dt_1[0:7])
########################################################################################################################

mr_bias=pd.concat([day_1_bias['mr_02'],day_1_bias_cor['mr_02']],axis=1)
mr_bias.columns=['mod','cor']
mr_bias.insert(0,'Date',day_1_bias.Date)                 
mr_bias['Date']=mr_bias['Date'].apply(pd.to_datetime,errors='coerce',format='%Y%m%d%H') 
mr_bias.index=mr_bias.Date
####################
mr_rmse=pd.concat([day_1_rmse['mr_02'],day_1_rmse_cor['mr_02']],axis=1)
mr_rmse.columns=['mod','cor']
mr_rmse.insert(0,'Date',day_1_rmse.Date)                 
mr_rmse['Date']=tmp_rmse['Date'].apply(pd.to_datetime,errors='coerce',format='%Y%m%d%H') 
mr_rmse.index=mr_bias.Date

mr_daymean_bias_rmse=pd.concat([mr_bias,mr_rmse['mod'],mr_rmse['cor']],axis=1)
mr_daymean_bias_rmse.columns=['Date','uc_bias','cor_bias','uc_rmse','cor_rmse']
mr_daymean_bias_rmse.to_csv('/home/vkvalappil/Data/oppModel/output/output/stat/corrected/corrected_rq/mr_obs_mod_cor_uc_dailymean.csv',index=False)

#########################################################################################################################

dt_1='2017-05-01' ; dt_2='2017-05-31'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-06-01' ; dt_2='2017-06-30'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-07-01' ; dt_2='2017-07-31'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-08-01' ; dt_2='2017-08-31'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-09-01' ; dt_2='2017-09-30'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-10-01' ; dt_2='2017-10-31'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-11-01' ; dt_2='2017-11-30'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-12-01' ; dt_2='2017-12-31'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-01-01' ; dt_2='2018-01-31'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-02-01' ; dt_2='2018-02-28'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-03-01' ; dt_2='2018-03-31'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-04-01' ; dt_2='2018-04-30'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-05-01' ; dt_2='2018-05-31'
plot_bars_rmse_dy(mr_daymean_bias_rmse[dt_1:dt_2],'Mixingratio','Day_wise','RMSE',dt_1[0:7])

######################################################################################################################################

rh_bias=pd.concat([day_1_bias['rh_02'],day_1_bias_cor['rh_02']],axis=1)
rh_bias.columns=['mod','cor']
rh_bias.insert(0,'Date',day_1_bias.Date)                 
rh_bias['Date']=rh_bias['Date'].apply(pd.to_datetime,errors='coerce',format='%Y%m%d%H') 
rh_bias.index=rh_bias.Date
####################
rh_rmse=pd.concat([day_1_rmse['rh_02'],day_1_rmse_cor['rh_02']],axis=1)
rh_rmse.columns=['mod','cor']
rh_rmse.insert(0,'Date',day_1_rmse.Date)                 
rh_rmse['Date']=rh_rmse['Date'].apply(pd.to_datetime,errors='coerce',format='%Y%m%d%H') 
rh_rmse.index=rh_bias.Date

rh_daymean_bias_rmse=pd.concat([rh_bias,rh_rmse['mod'],rh_rmse['cor']],axis=1)
rh_daymean_bias_rmse.columns=['Date','uc_bias','cor_bias','uc_rmse','cor_rmse']
rh_daymean_bias_rmse.to_csv('/home/vkvalappil/Data/oppModel/output/output/stat/corrected/corrected_rq/mr_obs_mod_cor_uc_dailymean.csv',index=False)

dt_1='2017-05-01' ; dt_2='2017-05-31'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-06-01' ; dt_2='2017-06-30'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-07-01' ; dt_2='2017-07-31'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-08-01' ; dt_2='2017-08-31'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-09-01' ; dt_2='2017-09-30'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-10-01' ; dt_2='2017-10-31'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-11-01' ; dt_2='2017-11-30'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2017-12-01' ; dt_2='2017-12-31'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-01-01' ; dt_2='2018-01-31'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-02-01' ; dt_2='2018-02-28'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-03-01' ; dt_2='2018-03-31'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-04-01' ; dt_2='2018-04-30'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

dt_1='2018-05-01' ; dt_2='2018-05-31'
plot_bars_rmse_dy(rh_daymean_bias_rmse[dt_1:dt_2],'Rh','Day_wise','RMSE',dt_1[0:7])

#########################################################################################################################
































