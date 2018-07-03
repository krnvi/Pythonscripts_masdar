#!/usr/bin/python

import sys ;import os ; import numpy as np ; import pandas as pd ; import datetime as dt ; from dateutil import tz, rrule ; import pytz

from sklearn.preprocessing import StandardScaler  
from sklearn.metrics import explained_variance_score, mean_absolute_error,  median_absolute_error 
from sklearn.model_selection import train_test_split  
from sklearn.neighbors import KNeighborsClassifier  ,KNeighborsRegressor, RadiusNeighborsRegressor  
knn_reg.fit(X_train, y_train)
y_pred=knn_reg.predict(X_test)  
np.sqrt(np.mean((y_test-y_pred)**2))
import pickle

main='/home/vkvalappil/Data/oppModel' ; output=main+'/output/output/stat/' ; inp=output=main+'/output/output/'
date='2016050106'

date_1=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=0)
date_2=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=610)
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
       print dte 
       print("No Data Exist")

#############################################################################################################################
################################### hourly Analysis ######################################################################### 
bias_hour_day_1=pd.concat(bias_hour_day1,axis=0) ; bias_hour_day_2=pd.concat(bias_hour_day2,axis=0)
mod_hour_day_1=pd.concat(mod_hour_day1,axis=0)   ; mod_hour_day_2=pd.concat(mod_hour_day2,axis=0)   ;
obs_hour_day_1=pd.concat(obs_hour_day1,axis=0)   ; mod_hour_day_2=pd.concat(mod_hour_day2,axis=0)   ;
##############################################################################################################################
#bias_hour_day_1.insert(0,'Date',bias_hour_day_1.index)

d_t_1='2016-11-01' ; d_t_2='2017-02-28' ; 

A_bias_hour_day1_1=bias_hour_day_1[d_t_1:d_t_2] ;  B_bias_hour_day2_1=bias_hour_day_2[d_t_1:d_t_2] ;   

mod_hour_day_1=mod_hour_day_1[d_t_1:d_t_2]
obs_hour_day_1=obs_hour_day_1[d_t_1:d_t_2]
bias_hour_day_1=bias_hour_day_1[d_t_1:d_t_2]


hourt = pd.to_timedelta(A_bias_hour_day1_1.index.hour,  unit='H')
bias_hour_avg_day1=A_bias_hour_day1_1.groupby(hourt).mean()           ###### bias for that particular hour , 01 means 01 UTC foracast , not forecast + 01 UTC
rmse_hour_avg_day1=(((A_bias_hour_day1_1**2).groupby(hourt)).mean())**0.5  
rmse_hour_avg_day1=pd.concat([rmse_hour_avg_day1.iloc[13:],rmse_hour_avg_day1[0:13]],axis=0)
mf=int(mod_hour_day_1.shape[0]/24.0)
rmse_hour_avg_day1=pd.concat([rmse_hour_avg_day1]*mf)

#################### 
#hourt = pd.to_timedelta(B_bias_hour_day2_1.index.hour,  unit='H')
#bias_hour_avg_day2=B_bias_hour_day2_1.groupby(hourt).mean()           ###### bias for that particular hour , 01 means 01 UTC foracast , not forecast + 01 UTC
#rmse_hour_avg_day2=(((B_bias_hour_day2_1**2).groupby(hourt)).mean())**0.5  


## TEMP
rmse_hour_avg_day1.index=mod_hour_day_1.index
tmp_input=pd.concat([mod_hour_day_1['TMP'],obs_hour_day_1['TMP'],bias_hour_day_1['TMP'],rmse_hour_avg_day1['TMP']],axis=1)
tmp_input.columns=['mod','obs','bias','rmse']
tmp_input['hour']=mod_hour_day_1.index.hour
tmp_input.insert(0,'Date',(mod_hour_day_1.index.strftime('%m')).astype(int))


## TEMP
#cor=mod_hour_day_1['TMP'].corr(obs_hour_day_1['TMP'],)
# 
#tmp_input=pd.concat([mod_hour_day_1['TMP'],obs_hour_day_1['TMP'],bias_hour_day_1['TMP']],axis=1)
#tmp_input.columns=['mod','obs','bias']
#tmp_input['hour']=mod_hour_day_1.index.hour
#tmp_input.insert(0,'Date',(mod_hour_day_1.index.strftime('%m')).astype(int))



######################################################
d_t_1='2016-11-01 00' ; d_t_2='2017-02-28 23' ;

tmp_inputt=tmp_input[d_t_1:d_t_2]
obs_hour_day_1t=obs_hour_day_1[d_t_1:d_t_2]

tmp_input_1=pd.concat([(tmp_inputt.iloc[0:-24]).reset_index(drop=True),tmp_inputt['mod'].iloc[24:].reset_index(drop=True)],axis=1)
tmp_target=obs_hour_day_1t['TMP'].iloc[24:]
###############################################################
#tmp_input_1.columns=['Date','mod.1','obs','bias','hour','mod'] 
#tmp_input_1=pd.concat([(tmp_input.iloc[0:8664]).reset_index(drop=True),tmp_input['mod'].iloc[24:].reset_index(drop=True)],axis=1)
#tmp_target=obs_hour_day_1['TMP'].iloc[24:]

cols=pd.Series(tmp_input_1.columns)
for dup in tmp_input_1.columns.get_duplicates():
#    cols[tmp_input_1.columns.get_loc(dup)]=[dup+'.'+str(d_idx) if d_idx!=0 else dup for d_idx in range(tmp_input_1.columns.get_loc(dup).sum())]
    cols[tmp_input_1.columns.get_loc(dup)]=[dup if d_idx==0 else dup+'.'+str(d_idx) for d_idx in range(tmp_input_1.columns.get_loc(dup).sum())]
    
tmp_input_1.columns=cols


##############################################################################################################
X=tmp_input_1.dropna(how='any').reset_index(drop=True)  ; Y=tmp_target.dropna(how='any').reset_index(drop=True)  ; 
#############################################################################################################################
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0,stratify=None)  
X_val=X_test ; y_val=y_test

scaler = StandardScaler()  ; scaler.fit(X_train)

#classifier = KNeighborsClassifier(n_neighbors=5)  
#classifier.fit(X_train, y_train)
#y_pred = classifier.predict(X_test)  
#np.sqrt(np.mean((y_test-y_pred)**2))

knn_reg = KNeighborsRegressor(n_neighbors=7,weights='distance',algorithm='auto')  
knn_reg.fit(X_train, y_train)
y_pred=knn_reg.predict(X_test)  
np.sqrt(np.mean((y_test-y_pred)**2))

# save the model to disk
filename = '/home/vkvalappil/Data/workspace/pythonScripts/knn/knn_model.sav'
pickle.dump(knn_reg, open(filename, 'wb')) 





















