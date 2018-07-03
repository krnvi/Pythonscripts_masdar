#!/usr/bin/python

import sys ;import os ; import numpy as np ; import pandas as pd ; import datetime as dt ; from dateutil import tz, rrule ; import pytz
import matplotlib.pyplot as plt; from pylab import savefig 

import pickle
from sklearn.preprocessing import StandardScaler  
from sklearn.metrics import explained_variance_score, mean_absolute_error,  median_absolute_error ,mean_squared_error
from sklearn.model_selection import train_test_split  
from sklearn.neighbors import KNeighborsClassifier  ,KNeighborsRegressor


main='/home/vkvalappil/Data/oppModel' ; output=main+'/output/output/stat/' ; inp=main+'/output/output/'
date='2017103106'

date_1=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=0)
date_2=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=151)
date_list=[x.strftime('%Y%m%d%H') for x in rrule.rrule(rrule.DAILY,dtstart=date_1,until=date_2)]

bias_day1 = [] ; rmse_day1 = [] ; bias_day2 = [] ; rmse_day2 = [] ; bias_hour_day1=[] ; bias_hour_day2=[]
mod_hour_day1=[] ; obs_hour_day1=[] ; mod_hour_day2=[] ; obs_hour_day2=[] ;

for dte in date_list[:]:
    
    file_2=inp+'domain_2/surfaceLevel/hourly'+dte+'.csv'
    if (os.path.isfile(file_2)):

        mod_dom_2=pd.read_csv(file_2) ; #mod_dom_2=mod_dom_2.iloc[72:144,:] ; 

        o_date_1=dte ; 
        o_date_2=(dt.datetime.strptime(dte,'%Y%m%d%H')+dt.timedelta(days=1)).strftime('%Y%m%d%H')
        o_date_3=(dt.datetime.strptime(dte,'%Y%m%d%H')+dt.timedelta(days=2)).strftime('%Y%m%d%H')
        o_date_4=(dt.datetime.strptime(dte,'%Y%m%d%H')+dt.timedelta(days=3)).strftime('%Y%m%d%H')
    
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

        mod_dom_2_2=pd.concat([mod_dom_2_1['localTime'],mod_dom_2_1['TEMP'],mod_dom_2_1['DTEMP'],mod_dom_2_1['RH'],mod_dom_2_1['MXRATIO'],mod_dom_2_1['WDIR']*0.277],axis=1)    

        mod_dom_2_2.columns=obs_3.columns
        
################################### Calculating Daily bias and daily rmse ############################################################################
        mod_dom_2_bias_1=mod_dom_2_2.iloc[7:31,1:].sub(obs_3.iloc[7:31,1:],axis=0)
        
        mod_dom_2_rmse_1=((mod_dom_2_bias_1**2).mean(axis=0))**0.5


        mod_dom_2_bias_2=mod_dom_2_2.iloc[31:55,1:].sub(obs_3.iloc[31:55,1:],axis=0)      

        mod_dom_2_rmse_2=((mod_dom_2_bias_2**2).mean(axis=0))**0.5

##################################################################################################        

        bias_day_1=np.vstack(mod_dom_2_bias_1.mean(axis=0).values).T
        bias_day_1=pd.DataFrame(bias_day_1,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])
        bias_day_1.insert(0,'Date',dte)

        rmse_day_1=np.vstack(mod_dom_2_rmse_1.values).T
        rmse_day_1=pd.DataFrame(rmse_day_1,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])
        rmse_day_1.insert(0,'Date',dte)  

        bias_day1.append(bias_day_1) ;     rmse_day1.append(rmse_day_1) ####### daily bias day wise appended day1
       
########################################                
        bias_hour_day1.append(mod_dom_2_bias_1)  ####### hourly bias appended for each day day1
        mod_hour_day1.append(mod_dom_2_2.iloc[7:31,1:]) ;  obs_hour_day1.append(obs_3.iloc[7:31,1:])
####################################     
        bias_day_2=np.vstack(mod_dom_2_bias_2.mean(axis=0).values).T

        bias_day_2=pd.DataFrame(bias_day_2,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])

        bias_day_2.insert(0,'Date',dte)

        rmse_day_2=np.vstack(mod_dom_2_rmse_2.values).T 
        
        rmse_day_2=pd.DataFrame(rmse_day_2,columns=['tmp_02','dpt_02','rh_02','mr_02','sknt_02'])

        rmse_day_2.insert(0,'Date',dte)

        bias_day2.append(bias_day_2) ; rmse_day2.append(rmse_day_2) ## daily bias day wise appended day2
###################################
        bias_hour_day2.append(mod_dom_2_bias_2)  ## hourly bias appended for each day day2
        mod_hour_day2.append(mod_dom_2_2.iloc[31:55,1:]) ;  obs_hour_day2.append(obs_3.iloc[31:55,1:])
##################################
    else:
       print (dte) 
       print("No Data Exist")

#############################################################################################################################

def plot_bars(C,parm,parm1,metric,ds ):
    
    fig=plt.figure(figsize=(20,12),dpi=50,frameon=True); ax = fig.add_subplot(111,facecolor='white')

    pos_1  = np.arange(0,14*C.shape[0],14) ; wdh=3.5 ; opacity = 1.0 ; #ax.hold(True);

    ax.bar(pos_1+wdh,C['mod'],width=wdh, color='b',alpha=opacity,label='Dom 2 model')
    ax.bar(pos_1+2*wdh ,C['mod_cor'],width=wdh, color='r',alpha=opacity,label='Dom 2 model cor')
    ax.bar(pos_1+3*wdh ,C['obs'],width=wdh, color='g',alpha=opacity,label='Dom 2 model bias added')
    ax.bar(pos_1+4*wdh ,C['mod_cor_ba'],width=wdh, color='k',alpha=opacity,label='obs')


    ax.axhline(0, color="k")

    plt.tick_params(axis='y',which='both', left='on',  right='off', labelright='off')
    ax.tick_params(axis='y', colors='black',labelsize=16) ; ax.yaxis.set_ticks_position('left') ;

    #ax.set_yticks(np.arange(-10,45,10)) ; 
    ax.set_ylabel(metric,color='black',fontsize=16,fontweight='bold') ;
    ax.set_xlabel('TIME: UTC ',color='black',fontsize=16,fontweight='bold') ;

    ax.set_xticks(np.arange(0,14*C.shape[0],14)+2*wdh) ; 
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
def plot_bars_rmse(C,parm,parm1,metric,ds ):
    
    fig=plt.figure(figsize=(20,12),dpi=50,frameon=True); ax = fig.add_subplot(111,facecolor='white')

    pos_1  = np.arange(0,10*C.shape[0],10) ; wdh=2.5 ; opacity = 1.0 ; #ax.hold(True);

    ax.bar(pos_1+wdh,C['mod'],width=wdh, color='b',alpha=opacity,label='Dom 2 rmse')
    ax.bar(pos_1+2*wdh ,C['rmse_cor'],width=wdh, color='r',alpha=opacity,label='Dom 2 rmse cor')
    ax.bar(pos_1+3*wdh ,C['rmse_cor_ba'],width=wdh, color='g',alpha=opacity,label='Dom 2 rmse cor ba')


    ax.axhline(1, color="k")

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
    outFile=output+'/corrected/dom2_'+parm+'_'+parm1+'_'+metric+'_'+ds+'.png' 
    savefig(outFile);
    plt.close(fig) ; fig.clf(fig)    
############################################################################################################################    
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
    outFile=output+'/corrected/dom2_'+parm1+'_'+ds+'.png' 
    savefig(outFile);
    plt.close(fig) ; fig.clf(fig)    
################################### hourly Analysis ######################################################################### 
bias_hour_day_1=pd.concat(bias_hour_day1,axis=0) ; bias_hour_day_2=pd.concat(bias_hour_day2,axis=0)
mod_hour_day_1=pd.concat(mod_hour_day1,axis=0)   ; mod_hour_day_2=pd.concat(mod_hour_day2,axis=0)   ;
obs_hour_day_1=pd.concat(obs_hour_day1,axis=0)   ; mod_hour_day_2=pd.concat(mod_hour_day2,axis=0)   ;
##############################################################################################################################
#bias_hour_day_1.insert(0,'Date',bias_hour_day_1.index)

d_t_1='2018-01-31' ; d_t_2='2018-02-28' ; 

A_bias_hour_day1_1=bias_hour_day_1[d_t_1:d_t_2] ;  B_bias_hour_day2_1=bias_hour_day_2[d_t_1:d_t_2] ;   

hourt = pd.to_timedelta(A_bias_hour_day1_1.index.hour,  unit='H')
bias_hour_avg_day1=A_bias_hour_day1_1.groupby(hourt).mean()           ###### bias for that particular hour , 01 means 01 UTC foracast , not forecast + 01 UTC

rmse_hour_avg_day1=(((A_bias_hour_day1_1**2).groupby(hourt)).mean())**0.5  
rmse_hour_avg_day1=pd.concat([rmse_hour_avg_day1.iloc[13:],rmse_hour_avg_day1[0:13]],axis=0)
mf=int(mod_hour_day_1.shape[0]/24.0)
rmse_hour_avg_day1=pd.concat([rmse_hour_avg_day1]*mf)

################### 
hourt = pd.to_timedelta(B_bias_hour_day2_1.index.hour,  unit='H')
bias_hour_avg_day2=B_bias_hour_day2_1.groupby(hourt).mean()           ###### bias for that particular hour , 01 means 01 UTC foracast , not forecast + 01 UTC
rmse_hour_avg_day2=(((B_bias_hour_day2_1**2).groupby(hourt)).mean())**0.5  

################################################### add avg hourly bias with forecast ############################################
 
hour_avg_bias=pd.read_csv('/home/vkvalappil/Data/oppModel/output/output/stat/hour_avgbias_day_1_201705.csv')

## TEMP
rmse_hour_avg_day1.index=mod_hour_day_1.index
tmp_input=pd.concat([mod_hour_day_1['TMP'],obs_hour_day_1['TMP'],bias_hour_day_1['TMP'],rmse_hour_avg_day1['TMP']],axis=1)
tmp_input.columns=['mod','obs','bias','rmse']
tmp_input['hour']=mod_hour_day_1.index.hour
tmp_input.insert(0,'Date',(mod_hour_day_1.index.strftime('%m')).astype(int)) 

#tmp_input=pd.concat([mod_hour_day_1['TMP'],obs_hour_day_1['TMP'],bias_hour_day_1['TMP']],axis=1)
#tmp_input.columns=['mod','obs','bias']
#tmp_input['hour']=mod_hour_day_1.index.hour
#tmp_input.insert(0,'Date',(mod_hour_day_1.index.strftime('%m')).astype(int)) 


tmp_input=tmp_input[d_t_1:d_t_2]
tmp_input=tmp_input.dropna(how='any')
######################################################################################################

date_index=tmp_input.index[::24] ; rmse_cor=[] ;
date_index_req=date_index[1:]
filename = '/home/vkvalappil/Data/workspace/pythonScripts/knn/knn_model.sav'
knn_reg = pickle.load(open(filename, 'rb'))
for ii in range(0,len(date_index_req)):

    #dte1=(dt.datetime.strptime(dte,'%Y%m%d%H')+dt.timedelta(days=0)).strftime('%Y-%m-%d %H')
    #prev_dt=(dt.datetime.strptime(dte,'%Y-%m-%d %H')+dt.timedelta(days=-1)).strftime('%Y-%m-%d %H')
    
    dte=date_index_req[ii] ; #dte1=date_index[ii+2]

    dte1=(dt.datetime.strptime(dte.strftime('%Y%m%d %H:%M:%S'),'%Y%m%d %H:%M:%S')+dt.timedelta(days=-1)).strftime('%Y-%m-%d %H:%M:%S')
    dte2=(dt.datetime.strptime(dte.strftime('%Y%m%d %H:%M:%S'),'%Y%m%d %H:%M:%S')+dt.timedelta(days=+1)).strftime('%Y-%m-%d %H:%M:%S')
    
    dt_tmp_input_1=tmp_input[dte1:dte2] ;  
   
    if dt_tmp_input_1.shape >= (48,6) :
        dt_tmp_input=dt_tmp_input_1 ;
    else:
        dte_t=(dt.datetime.strptime(dte.strftime('%Y%m%d %H:%M:%S'),'%Y%m%d %H:%M:%S')+dt.timedelta(days=-2)).strftime('%Y-%m-%d %H:%M:%S')
        dt_tmp_input=tmp_input[dte_t:dte2]


    tmp_input_1=pd.concat([(dt_tmp_input.iloc[0:24]).reset_index(drop=True),dt_tmp_input['mod'].iloc[24:48].reset_index(drop=True)],axis=1)
    tmp_target=dt_tmp_input['obs'].iloc[24:48].reset_index(drop=True) 

#    tmp_input_1.columns=['Date','mod.1','obs','bias','hour','mod'] 

    cols=pd.Series(tmp_input_1.columns)
    for dup in tmp_input_1.columns.get_duplicates(): 
        cols[tmp_input_1.columns.get_loc(dup)]=[dup+'.'+str(d_idx) if d_idx!=0 else dup for d_idx in range(tmp_input_1.columns.get_loc(dup).sum())]
    tmp_input_1.columns=cols
#  

    ##################### new Forecast Bias added ######################################################################
    hour_avg_bias_1=(pd.concat([hour_avg_bias['TMP'][13:],hour_avg_bias['TMP'][1:13]],axis=0)).reset_index(drop=True)
    b_add_tmp=tmp_input_1['mod']- hour_avg_bias_1
     
##############################################################################################################
    X=tmp_input_1.dropna(how='any').reset_index(drop=True)  ; Y=tmp_target.dropna(how='any').reset_index(drop=True)  ; 
    scaler = StandardScaler()  ; scaler.fit(X)

    y_new_l_dnn =knn_reg.predict(X)
##############################Loading and Predict Linear regressor #############################################################

    print dte
    print("The Mean Absolute Error: %.2f degrees Celcius" % mean_absolute_error(Y,np.round(y_new_l_dnn)))  
    print("The Mean square Error: %.2f degrees Celcius" % np.sqrt(mean_squared_error(Y,np.round(y_new_l_dnn))) )

    print("The Mean Absolute Error: %.2f degrees Celcius" % mean_absolute_error(Y,tmp_input_1['mod']))  
    print("The Mean square Error: %.2f degrees Celcius" % np.sqrt(mean_squared_error(Y,tmp_input_1['mod']))) 
    print("#################################### ##############################################")
   
################################################################################################################################# 
    bias_new=pd.DataFrame(np.round(np.vstack(y_new_l_dnn))-np.vstack(Y.as_matrix()))
    rmse_new=(np.sqrt(mean_squared_error(Y,np.round(y_new_l_dnn))))
    rmse_mod=(np.sqrt(mean_squared_error(Y,X['mod'])))
 
    bias_ba=pd.DataFrame(np.round(np.vstack(b_add_tmp))-np.vstack(Y.as_matrix()))
    rmse_ba=np.sqrt(np.nanmean((Y-np.round(b_add_tmp))**2))
      
    rmse_cor.append([rmse_mod,rmse_new,rmse_ba])

    tmp_data_new=pd.concat([tmp_input_1['mod'],pd.DataFrame(np.round(y_new_l_dnn)),pd.DataFrame(np.round(b_add_tmp)),Y,dt_tmp_input['bias'].iloc[24:48].reset_index(drop=True),\
                 bias_new,bias_ba],axis=1)
    tmp_data_new.columns=['mod','mod_cor','mod_cor_ba','obs','bias_mod','bias_cor','bias_ba']
    tmp_data_new.index=dt_tmp_input.index[24:48]
    tmp_data_new.insert(0,'Date',tmp_data_new.index)
    
    #plot_bars(tmp_data_new,'tmperature','tmp_mod','day_1',tmp_data_new.index.strftime('%Y%m%d')[0] )
    plot_line(tmp_data_new,'Temperature','Temperature',tmp_data_new.index.strftime('%Y%m%d')[0])
    plot_bars_bias(tmp_data_new,'tmperature','bias','day_1',tmp_data_new.index.strftime('%Y%m%d')[0])
#####################################################################################################################################
     

rmse_cor=pd.DataFrame(rmse_cor,columns=['mod','rmse_cor','rmse_cor_ba']) 
rmse_cor.index=date_index_req ; rmse_cor.insert(0,'Date',rmse_cor.index)
plot_bars_rmse(rmse_cor,'tmperature','day_1','rmse',rmse_cor.index.strftime('%Y%m')[0])

