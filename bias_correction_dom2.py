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

#roll = pd.cut(X.index, range(0,len(X), 24),right=False,retbins=False) 

#X.rolling(window=24, min_periods=20)
#groups = X.groupby(pd.cut(X.index, range(0,len(X)+1, 24),right=True,retbins=False))
#g_keys=groups.groups.keys()
#g_keys = [name for name,unused_df in groups]
#g_min=groups.min()

#min_X=groups.min() ; max_X=groups.max()
#norm_X=(groups-min_X)/(max_X-min_X)

min_X = np.min(X,axis=0) ; max_X = np.max(X,axis=0) ;
norm_X = (X - min_X) / (max_X - min_X)

min_Y = np.min(Y,axis=0) ; max_Y = np.max(Y,axis=0) ;
norm_Y = (Y - min_Y) / (max_Y - min_Y)
##################################################################################################################
#X_train, X_test, y_train, y_test = train_test_split(norm_X, norm_Y, test_size=0.1, random_state=0,stratify=None)  
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0,stratify=None)  

#X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.5, random_state=None)
X_val=X_test ; y_val=y_test

#X_train=X ; Y_train=Y
#X_train_norm=tf.keras.utils.normalize(X_train.values,axis=0,order=3)

#############################################################################################################################
feature_cols = [tf.feature_column.numeric_column(col) for col in X.columns]  

#optimizer=tf.train.GradientDescentOptimizer( learning_rate=.001 ),

#reg_dnn = tf.estimator.DNNRegressor(feature_columns=feature_cols, hidden_units=[10,10,1], optimizer='Adagrad', \
#            model_dir='dnn_bias-cor',activation_fn=tf.nn.leaky_relu)

########### Linear dnn combined regressor ############################################
reg_linear_dnn = tf.estimator.DNNLinearCombinedRegressor(linear_feature_columns=feature_cols,linear_optimizer='Ftrl',\
                 dnn_feature_columns=feature_cols,dnn_hidden_units=[50,50,1],dnn_activation_fn=tf.nn.relu,\
                 dnn_optimizer='Adagrad',model_dir='linear_dnn_bias-cor_full.bsz_ep.2000_hu.50.50.1_Mn_2016_2017_winter')

#reg_linear=tf.estimator.LinearRegressor(feature_columns=feature_cols, optimizer='Adagrad',model_dir='linear_bias-cor'   )
############## Input function ##############################
def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=400):  
  
    return tf.estimator.inputs.pandas_input_fn(x=X, y=y, num_epochs=num_epochs,  shuffle=shuffle,  batch_size=batch_size)

##################################################
eval_dnn = []  ; eval_ln_dnn=[] ; eval_ln = []  ;
epochs = 2000 ; batch_size = 50  ; total_batch = int(len(y_train) / batch_size) 

for i in range(0,25) :
    reg_linear_dnn.train(input_fn=wx_input_fn(X_train, y=y_train), steps=epochs)
    eval_ln_dnn.append(reg_linear_dnn.evaluate(input_fn=wx_input_fn(X_val, y_val, num_epochs=1,  shuffle=False)))

for i in range(total_batch):  
    
    batch_x, batch_y = X_train.iloc[i * batch_size:min(i * batch_size + batch_size, len(X_train)) ], \
                         y_train[i * batch_size:min(i * batch_size + batch_size, len(y_train)) ] 
    
    #reg_dnn.train(input_fn=wx_input_fn(batch_x, y=batch_y), steps=epochs) 
    
    #eval_dnn.append(reg_dnn.evaluate(input_fn=wx_input_fn(X_val, y_val, num_epochs=1,  shuffle=False)))

    reg_linear_dnn.train(input_fn=wx_input_fn(batch_x, y=batch_y), steps=epochs) 
    
    eval_ln_dnn.append(reg_linear_dnn.evaluate(input_fn=wx_input_fn(X_val, y_val, num_epochs=1,  shuffle=False)))

    #reg_linear.train(input_fn=wx_input_fn(batch_x, y=batch_y), steps=epochs) 
    
    #eval_ln.append(reg_linear.evaluate(input_fn=wx_input_fn(X_val, y_val, num_epochs=1,  shuffle=False)))

 

#A=reg_dnn.predict(input_fn=wx_input_fn(X_val, y_val, num_epochs=1,  shuffle=False))
#for i in A:
#    print i['predictions']

##########################################################################################################################
import matplotlib.pyplot as plt; from pylab import savefig 
evaluations=eval_ln_dnn
# manually set the parameters of the figure to and appropriate size
plt.rcParams['figure.figsize'] = [14, 10]

loss_values = [ev['loss'] for ev in evaluations]  
training_steps = [ev['global_step'] for ev in evaluations]

plt.scatter(x=training_steps, y=loss_values)  
plt.xlabel('Training steps (Epochs = steps / 2)')  
plt.ylabel('Loss (SSE)')  
savefig(str(total_batch)+'.bsz_ep.'+str(epochs)+'_hu.100.100.1.png',dpi=50)
plt.show()  

###########################################################################################
#pred = reg_linear_dnn.predict(input_fn=wx_input_fn(X_test, num_epochs=1,  shuffle=False))
#predictions = np.array([p['predictions'][0] for p in pred])

########################################################################################################################
#print("The Explained Variance: %.2f" % explained_variance_score(  
#                                            y_test, predictions))  
#print("The Mean Absolute Error: %.2f degrees Celcius" % mean_absolute_error(  
#                                            y_test, predictions))  
#print("The Mean square Error: %.2f degrees Celcius" % np.sqrt(mean_squared_error(  
#                                            y_test, predictions)) ) 
#                                            
#print("The Median Absolute Error: %.2f degrees Celcius" % median_absolute_error(  
#                                            y_test, predictions))



########################################################################################################################










