#!/usr/bin/python

import sys ;import os ; import numpy as np ; import pandas as pd ; import datetime as dt ; from dateutil import tz, rrule ; import pytz


import tensorflow as tf  
from sklearn.metrics import explained_variance_score, mean_absolute_error,  median_absolute_error 
from sklearn.model_selection import train_test_split  


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

####################### Winter data segregation #################################################################################
A_bias_hour_day1_winter=pd.concat([bias_hour_day_1['2016-11-01':'2017-03-01'],bias_hour_day_1['2017-11-01':'2017-12-31']],axis=0)
hourt = pd.to_timedelta(A_bias_hour_day1_winter.index.hour,  unit='H')
rmse_hour_avg_day1_winter=(((A_bias_hour_day1_winter**2).groupby(hourt)).mean())**0.5
mf=int(A_bias_hour_day1_winter.shape[0]/24.0)
rmse_hour_avg_day1_winter=pd.concat([rmse_hour_avg_day1_winter]*mf)

mod_hour_day_1_winter=pd.concat([mod_hour_day_1['2016-11-01':'2017-03-01'],mod_hour_day_1['2017-11-01':'2017-12-31']],axis=0)
obs_hour_day_1_winter=pd.concat([obs_hour_day_1['2016-11-01':'2017-03-01'],obs_hour_day_1['2017-11-01':'2017-12-31']],axis=0)

## TEMP
rmse_hour_avg_day1_winter.index=mod_hour_day_1_winter.index
tmp_input_winter=pd.concat([mod_hour_day_1_winter['TMP'],obs_hour_day_1_winter['TMP'],A_bias_hour_day1_winter['TMP'],rmse_hour_avg_day1_winter['TMP']],axis=1)
tmp_input_winter.columns=['mod','obs','bias','rmse']
tmp_input_winter['hour']=mod_hour_day_1_winter.index.hour
tmp_input_winter.insert(0,'Date',(mod_hour_day_1_winter.index.strftime('%m')).astype(int))

tmp_inputt=tmp_input_winter ; 
tmp_input_1=pd.concat([(tmp_inputt.iloc[0:-24]).reset_index(drop=True),tmp_inputt['mod'].iloc[24:].reset_index(drop=True)],axis=1)
tmp_target=tmp_inputt['obs'].iloc[24:]
tmp_input_1.columns=['Date', 'mod.p', 'obs', 'bias', 'rmse', 'hour', 'mod']
###############################################################################################################################################
##################################### Summer Data Segregation ##################################################################################
#A_bias_hour_day1_summer=pd.concat([bias_hour_day_1['2016-05-04':'2016-10-31'],bias_hour_day_1['2017-04-01':'2017-10-31']],axis=0)
#hourt = pd.to_timedelta(A_bias_hour_day1_summer.index.hour,  unit='H')
#rmse_hour_avg_day1_summer=(((A_bias_hour_day1_summer**2).groupby(hourt)).mean())**0.5
#mf=int(A_bias_hour_day1_summer.shape[0]/24.0)
#rmse_hour_avg_day1_summer=pd.concat([rmse_hour_avg_day1_summer]*mf)
#
#mod_hour_day_1_summer=pd.concat([mod_hour_day_1['2016-05-04':'2016-10-31'],mod_hour_day_1['2017-04-01':'2017-10-31']],axis=0)
#obs_hour_day_1_summer=pd.concat([obs_hour_day_1['2016-05-04':'2016-10-31'],obs_hour_day_1['2017-04-01':'2017-10-31']],axis=0)
#
### TEMP
#rmse_hour_avg_day1_summer.index=mod_hour_day_1_summer.index
#tmp_input_summer=pd.concat([mod_hour_day_1_summer['TMP'],obs_hour_day_1_summer['TMP'],A_bias_hour_day1_summer['TMP'],rmse_hour_avg_day1_summer['TMP']],axis=1)
#tmp_input_summer.columns=['mod','obs','bias','rmse']
#tmp_input_summer['hour']=mod_hour_day_1_summer.index.hour
#tmp_input_summer.insert(0,'Date',(mod_hour_day_1_summer.index.strftime('%m')).astype(int))
#
#tmp_inputt=tmp_input_summer ; 
#tmp_input_1=pd.concat([(tmp_inputt.iloc[0:-24]).reset_index(drop=True),tmp_inputt['mod'].iloc[24:].reset_index(drop=True)],axis=1)
#tmp_target=tmp_inputt['obs'].iloc[24:]
#tmp_input_1.columns=['Date', 'mod.p', 'obs', 'bias', 'rmse', 'hour', 'mod']
##################################################################################################################################################

X=tmp_input_1.dropna(how='any').reset_index(drop=True)  ; Y=tmp_target.dropna(how='any').reset_index(drop=True)  ; 
#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.005, random_state=0,stratify=None)  
#X_val=X_test ; y_val=y_test

#X_train_norm=tf.keras.utils.normalize(X_train.values,axis=0,order=3)
#Y_train_norm=tf.keras.utils.normalize(X_train.values,axis=0,order=3)
#############################################################################################################################

min_X = np.min(X,axis=0) ; max_X = np.max(X,axis=0) ;
norm_X = (X - min_X) / (max_X - min_X)

min_mnth=1.0 ; max_mnth=12.0
norm_mnth=(X['Date']- min_mnth) /(max_mnth - min_mnth )
norm_X['Date']=norm_mnth

min_Y = np.min(Y,axis=0) ; max_Y = np.max(Y,axis=0) ;
norm_Y = (Y - min_Y) / (max_Y - min_Y)

X_train, X_test, y_train, y_test = train_test_split(norm_X, norm_Y, test_size=0.005, random_state=0,stratify=None)  
X_val=X_test ; y_val=y_test

##################################################################################################################

#X_train=X ; Y_train=Y
#X_train_norm=tf.keras.utils.normalize(X_train.values,axis=0,order=3)

#############################################################################################################################

feature_cols = [tf.feature_column.numeric_column(col) for col in X_train.columns]  


########### Linear dnn combined regressor ############################################
epochs = 2000 ;
h_size1=30 ; h_size2=20 ; itrn=50
m_dir='tmp_linear_dnn_bias-cor_full_'+str(itrn)+'.bsz_ep.'+str(epochs)+'_hu.'+str(h_size1)+'.'+str(h_size1)+'.'+str(h_size2)+'.1_Mn_2016_2017_winter'
#m_dir='tmp_linear_dnn_bias-cor_full_'+str(itrn)+'.bsz_ep.'+str(epochs)+'_hu.'+str(h_size1)+'.'+str(h_size1)+'.'+str(h_size1)+'.'+str(h_size2)+'.1_Mn_2016_2017_winter'
    
reg_linear_dnn = tf.estimator.DNNLinearCombinedRegressor(linear_feature_columns=feature_cols,linear_optimizer='Ftrl',\
                 dnn_feature_columns=feature_cols,dnn_hidden_units=[h_size1,h_size1,h_size2,1],dnn_activation_fn=tf.nn.relu,\
                 dnn_optimizer='Adagrad',model_dir=m_dir)

#reg_linear=tf.estimator.LinearRegressor(feature_columns=feature_cols, optimizer='Adagrad',model_dir='linear_bias-cor'   )
############## Input function ##############################
def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=400):  
  
    return tf.estimator.inputs.pandas_input_fn(x=X, y=y, num_epochs=num_epochs,  shuffle=shuffle,  batch_size=batch_size)

eval_ln_dnn=[] ; 
for i in range(0,itrn) :
    reg_linear_dnn.train(input_fn=wx_input_fn(X_train, y=y_train), steps=epochs)
    eval_ln_dnn.append(reg_linear_dnn.evaluate(input_fn=wx_input_fn(X_val, y_val, num_epochs=1,  shuffle=False)))

##############################################################################################################################################
quit()
import matplotlib.pyplot as plt; from pylab import savefig 
evaluations=eval_ln_dnn
# manually set the parameters of the figure to and appropriate size
plt.rcParams['figure.figsize'] = [14, 10]

loss_values = [ev['loss'] for ev in evaluations]  
training_steps = [ev['global_step'] for ev in evaluations]

plt.scatter(x=training_steps, y=loss_values)  
plt.xlabel('Training steps (Epochs = steps / 2)')  
plt.ylabel('Loss (SSE)')  
#savefig(str(total_batch)+'.bsz_ep.'+str(epochs)+'_hu.100.100.1.png',dpi=50)
plt.show()  











