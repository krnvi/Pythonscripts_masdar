#!/usr/bin/python

import sys ;import os ; import numpy as np ; import pandas as pd ; import datetime as dt ; from dateutil import tz, rrule ; import pytz

import tensorflow as tf  
from sklearn.metrics import explained_variance_score, mean_absolute_error,  median_absolute_error 
from sklearn.model_selection import train_test_split  
from sklearn.preprocessing import StandardScaler 

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
A_bias_hour_day1_winter=pd.concat([bias_hour_day_1['2016-11-01':'2017-03-31'],bias_hour_day_1['2017-11-01':'2017-12-31']],axis=0)
hourt = pd.to_timedelta(A_bias_hour_day1_winter.index.hour,  unit='H')
rmse_hour_avg_day1_winter=(((A_bias_hour_day1_winter**2).groupby(hourt)).mean())**0.5
mf=int(A_bias_hour_day1_winter.shape[0]/24.0)
rmse_hour_avg_day1_winter=pd.concat([rmse_hour_avg_day1_winter]*mf)

mod_hour_day_1_winter=pd.concat([mod_hour_day_1['2016-11-01':'2017-03-31'],mod_hour_day_1['2017-11-01':'2017-12-31']],axis=0)
obs_hour_day_1_winter=pd.concat([obs_hour_day_1['2016-11-01':'2017-03-31'],obs_hour_day_1['2017-11-01':'2017-12-31']],axis=0)

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

############## Normalise input and target ##############################################################################################
min_X = np.min(X,axis=0) ; max_X = np.max(X,axis=0) ; 
norm_X = (X - min_X) / (max_X - min_X)

min_mnth=1.0 ; max_mnth=12.0
norm_mnth=(X['Date']- min_mnth) /(max_mnth - min_mnth )

norm_X['Date']=norm_mnth

min_Y = np.min(Y,axis=0) ; max_Y = np.max(Y,axis=0) ; 
norm_Y = (Y - min_Y) / (max_Y - min_Y)
#######################################################################################################################################
X_train, X_test, y_train, y_test = train_test_split(norm_X, norm_Y, test_size=0.005, random_state=0)  
X_val=X_test ; y_val=y_test

X_train=norm_X ; y_train=norm_Y
y_train=np.vstack(y_train) ; y_test=np.vstack(y_test)


#scaler = StandardScaler()
#scaler.fit(X_train,X_test)
#X_train = scaler.transform(X_train) ;  X_test = scaler.transform(X_test)
#scaler.inverse_transform(X_train)
######################### set some variables #######################

x_size = X_train.shape[1]     # Number of input nodes: 4 features and 1 bias
h_size =3500                  # Number of hidden nodes
y_size = 1                    #y_train.shape[1] # Number of outcomes (3 iris flowers)


#x = tf.placeholder(tf.float32, [None, 5], name='x')  # 3 features
#y = tf.placeholder(tf.float32, [None, 1], name='y')  # 3 outputs

# Symbols
x = tf.placeholder("float", shape=[None, x_size])
y = tf.placeholder("float", shape=[None, y_size])

# hidden layer 1
W1 = tf.Variable(tf.truncated_normal([x_size, h_size], stddev=0.03), name='W1')
b1 = tf.Variable(tf.truncated_normal([h_size]), name='b1')

# output hidden layer 1
hidden_out = tf.nn.tanh(tf.add(tf.matmul(x, W1), b1))


# hidden layer 2
W2 = tf.Variable(tf.truncated_normal([h_size, h_size], stddev=0.03), name='W2')
b2 = tf.Variable(tf.truncated_normal([h_size]), name='b2')

hidden_out2 = tf.nn.tanh(tf.add(tf.matmul(hidden_out, W2), b2))

# hidden layer 2
W3 = tf.Variable(tf.truncated_normal([h_size, y_size], stddev=0.03), name='W3')
b3 = tf.Variable(tf.truncated_normal([y_size]), name='b3')

######################## Activations, outputs ######################



# total output
#y_ = tf.nn.tanh(tf.add(tf.matmul(hidden_out2, W3), b3))  # output layer activation relu

#y_ =tf.matmul(hidden_out,W2) + b2                              # output layer activation Linear 
y_ =tf.add(tf.matmul(hidden_out2,W3), b3)                              
####################### Loss Function  #########################
mse = tf.losses.mean_squared_error(y, y_)                      # minimmisation criteria

#cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))

# accuracy for the test set
#accuracy = tf.reduce_mean(tf.square(tf.subtract(y, y_)))  # or could use tf.losses.mean_squared_error

####################### Optimizer      #########################
learning_rate = 0.0005 ; epochs = 5000 ; batch_size = 100 
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(mse)

###################### Initialize, Accuracy and Run #################
# initialize variables
sess=tf.Session() 
init_op = tf.global_variables_initializer()
saver = tf.train.Saver()
sess.run(init_op)
total_batch = int(len(y_train) / batch_size)
cost_f=[]
for epoch in range(epochs):
    avg_cost = 0

    #for i in range(total_batch):

        #batch_x, batch_y = X_train.iloc[i * batch_size:min(i * batch_size + batch_size, len(X_train)) ], \
        #                 y_train[i * batch_size:min(i * batch_size + batch_size, len(y_train)) ]


#        _, c = sess.run([optimizer, mse], feed_dict={x: batch_x, y: batch_y })
    _, c = sess.run([optimizer, mse], feed_dict={x: X_train, y: y_train })
    avg_cost += c #/ total_batch
    print(avg_cost)    
    if epoch % 10 == 0:
      print 'Epoch:', (epoch + 1), 'cost =', '{:.3f}'.format(avg_cost)
      cost_f.append(avg_cost)
   
    if avg_cost==0:
       print("avg_cost reached 0: exiting") 
       break    
#print sess.run(mse, feed_dict={x: X_test, y: y_test})

 
## Test model
#correct_prediction = tf.equal(tf.argmax(y_, 1), tf.argmax(y, 1))
## Calculate accuracy
#accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
#print("Accuracy:", accuracy.eval(session=sess,feed_dict={x: X_test, y: y_test}))

# Save model weights to disk
 
if not os.path.exists('/home/vkvalappil/Data/workspace/pythonScripts/MLP/mlp_bias_cor_'+str(h_size)+'N'):
        os.makedirs('/home/vkvalappil/Data/workspace/pythonScripts/MLP/mlp_bias_cor_'+str(h_size)+'N')

save_path = saver.save(sess, '/home/vkvalappil/Data/workspace/pythonScripts/MLP/mlp_bias_cor_'+str(h_size)+'N/mlp_bias_cor_'+str(h_size)+'N')
sess.close() 














