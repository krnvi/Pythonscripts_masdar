#!/usr/bin/python

import sys ;import os ; import numpy as np ; import pandas as pd ; import datetime as dt ; from dateutil import tz, rrule ; import pytz
import matplotlib.pyplot as plt; from pylab import savefig 

import tensorflow as tf  
from sklearn.metrics import explained_variance_score, mean_absolute_error,  median_absolute_error ,mean_squared_error
from sklearn.model_selection import train_test_split  


main='/home/vkvalappil/Data/oppModel' ; output=main+'/output/output/stat/' ; inp=output=main+'/output/output/'
date='2018050106'

date_1=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=0)
date_2=dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(days=25)
date_list=[x.strftime('%Y%m%d%H') for x in rrule.rrule(rrule.DAILY,dtstart=date_1,until=date_2)]

bias_day1 = [] ; rmse_day1 = [] ; bias_day2 = [] ; rmse_day2 = [] ; bias_hour_day1=[] ; bias_hour_day2=[]
mod_hour_day1=[] ; obs_hour_day1=[] ; mod_hour_day2=[] ; obs_hour_day2=[] ;

for dte in date_list[:]:
    
    file_2=inp+'domain_2/surfaceLevel/hourly'+dte+'.csv'
    if (os.path.isfile(file_2)):

        mod_dom_2=pd.read_csv(file_2) ; mod_dom_2=mod_dom_2.iloc[72:144,:] ; 

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
       print("No Data Exist")

#############################################################################################################################

def plot_bars(C,parm,parm1,metric,ds ):
    
    fig=plt.figure(figsize=(20,12),dpi=50,frameon=True); ax = fig.add_subplot(111,facecolor='white')

    pos_1  = np.arange(0,4*C.shape[0],4) ;  ax.hold(True); wdh=2.5 ; opacity = 0.75

    ax.bar(pos_1,C.iloc[:],width=wdh, color='b',alpha=opacity,label='Dom 2')

    ax.axhline(0, color="k")

    plt.tick_params(axis='y',which='both', left='on',  right='off', labelright='off')
    ax.tick_params(axis='y', colors='black',labelsize=16) ; ax.yaxis.set_ticks_position('left') ;

    #ax.set_yticks(np.arange(-10,45,10)) ; 
    ax.set_ylabel(metric,color='black',fontsize=16,fontweight='bold') ;
    ax.set_xlabel('TIME: UTC ',color='black',fontsize=16,fontweight='bold') ;

    ax.set_xticks(np.arange(0,4*C.shape[0],4)) ; xTickMarks=pd.TimedeltaIndex.to_series(C.index).dt.components.hours 
    xtickNames =ax.set_xticklabels(xTickMarks,rotation=0,fontsize=14,fontweight='bold')

    #plt.tick_params(axis='x',which='both', bottom='off',  top='off', labelbottom='off')
    for n, row in enumerate(C.iloc[:]):
        plt.text(4*n, row, np.round(row,3), ha='center', rotation=0, va='bottom',fontsize=16,fontweight='bold')

    handles, labels = ax.get_legend_handles_labels()
    display = (0,1,2,3,4)

    leg=ax.legend(loc='upper right',fontsize=18)

    plt.tight_layout(pad=3) ;

    plt.title( metric+' : 2M '+parm,fontsize=16)
    outFile=output+'stat/dom2_'+parm1+'_'+metric+'_'+ds+'.png' 
    savefig(outFile);
    plt.close(fig) ; fig.clf(fig)

##############################################################################################################################

################################### hourly Analysis ######################################################################### 
bias_hour_day_1=pd.concat(bias_hour_day1,axis=0) ; bias_hour_day_2=pd.concat(bias_hour_day2,axis=0)
mod_hour_day_1=pd.concat(mod_hour_day1,axis=0)   ; mod_hour_day_2=pd.concat(mod_hour_day2,axis=0)   ;
obs_hour_day_1=pd.concat(obs_hour_day1,axis=0)   ; mod_hour_day_2=pd.concat(mod_hour_day2,axis=0)   ;
##############################################################################################################################
#bias_hour_day_1.insert(0,'Date',bias_hour_day_1.index)

d_t_1='2018-05-01' ; d_t_2='2018-05-26' ; 

A_bias_hour_day1_1=bias_hour_day_1[d_t_1:d_t_2] ;  B_bias_hour_day2_1=bias_hour_day_2[d_t_1:d_t_2] ;   

hourt = pd.to_timedelta(A_bias_hour_day1_1.index.hour,  unit='H')
bias_hour_avg_day1=A_bias_hour_day1_1.groupby(hourt).mean()           ###### bias for that particular hour , 01 means 01 UTC foracast , not forecast + 01 UTC

rmse_hour_avg_day1=(((A_bias_hour_day1_1**2).groupby(hourt)).mean())**0.5  
rmse_hour_avg_day1=pd.concat([rmse_hour_avg_day1.iloc[13:],rmse_hour_avg_day1[0:13]],axis=0)
rmse_hour_avg_day1=pd.concat([rmse_hour_avg_day1]*24)

################### 
hourt = pd.to_timedelta(B_bias_hour_day2_1.index.hour,  unit='H')
bias_hour_avg_day2=B_bias_hour_day2_1.groupby(hourt).mean()           ###### bias for that particular hour , 01 means 01 UTC foracast , not forecast + 01 UTC
rmse_hour_avg_day2=(((B_bias_hour_day2_1**2).groupby(hourt)).mean())**0.5  


## TEMP
rmse_hour_avg_day1.index=mod_hour_day_1.index
tmp_input=pd.concat([mod_hour_day_1['TMP'],obs_hour_day_1['TMP'],bias_hour_day_1['TMP'],rmse_hour_avg_day1['TMP']],axis=1)
tmp_input.columns=['mod','obs','bias','rmse']
tmp_input['hour']=mod_hour_day_1.index.hour

 
tmp_input_1=pd.concat([(tmp_input.iloc[0:552]).reset_index(drop=True),tmp_input['mod'].iloc[24:].reset_index(drop=True)],axis=1)
tmp_target=obs_hour_day_1['TMP'].iloc[24:]
cols=pd.Series(tmp_input_1.columns)
for dup in tmp_input_1.columns.get_duplicates(): 
    cols[tmp_input_1.columns.get_loc(dup)]=[dup+'.'+str(d_idx) if d_idx!=0 else dup for d_idx in range(tmp_input_1.columns.get_loc(dup).sum())]
tmp_input_1.columns=cols
#tmp_input_1=tmp_input_1.drop('rmse',axis=1)
#tmp_input_1=tmp_input_1.drop('hour',axis=1)
#tmp_input_1=tmp_input_1.drop('bias',axis=1)

##############################################################################################################
X=tmp_input_1.dropna(how='any').reset_index(drop=True)  ; Y=tmp_target.dropna(how='any').reset_index(drop=True)  ; 

############## Normalise input and target ##############################################################################################
min_X = np.min(X,axis=0) ; max_X = np.max(X,axis=0) ; 
norm_X = (X - min_X) / (max_X - min_X)

min_Y = np.min(Y,axis=0) ; max_Y = np.max(Y,axis=0) ; 
norm_Y = (Y - min_Y) / (max_Y - min_Y)

##########################################################################################################
x_size = X.shape[1]           # Number of input nodes: 4 features and 1 bias
h_size =10000           # Number of hidden nodes
y_size = 1                    #y_train.shape[1] # Number of outcomes (3 iris flowers)

# Symbols
x = tf.placeholder("float", shape=[None, x_size])
y = tf.placeholder("float", shape=[None, y_size])

sess=tf.Session()
init = tf.global_variables_initializer()
saver = tf.train.import_meta_graph('/home/vkvalappil/Data/workspace/pythonScripts/mlp_bias_cor_1/mlp_bias_cor.meta') 
saver.restore(sess,tf.train.latest_checkpoint('/home/vkvalappil/Data/workspace/pythonScripts/mlp_bias_cor_1/'))

graph = tf.get_default_graph() 
w1 = graph.get_tensor_by_name("W1:0")
w2 = graph.get_tensor_by_name("W2:0")
b1 =graph.get_tensor_by_name("b1:0")
b2 =graph.get_tensor_by_name("b2:0")

hidden_out = tf.nn.tanh(tf.add(tf.matmul(x, w1), b1))
#y_=tf.add(tf.matmul(hidden_out,w2), b2 )   

y_ = tf.nn.tanh(tf.add(tf.matmul(hidden_out, w2), b2)) 

feed_dict ={x:norm_X }
y_new=y_.eval(feed_dict=feed_dict,session=sess) 

y_new = y_new * (max_Y - min_Y) + min_Y

 
print("The Mean Absolute Error: %.2f degrees Celcius" % mean_absolute_error(Y,y_new))  
print("The Mean square Error: %.2f degrees Celcius" % np.sqrt(mean_squared_error(Y,np.round(y_new))) )

print("The Mean Absolute Error: %.2f degrees Celcius" % mean_absolute_error(Y,tmp_input_1['mod.1']))  
print("The Mean square Error: %.2f degrees Celcius" % np.sqrt(mean_squared_error(Y,tmp_input_1['mod.1']))) 

#####################################################################################################################################
sess.close()
##Now, access the op that you want to run. 
#op_to_restore = graph.get_tensor_by_name("op_to_restore:0")
#sess.run(op_to_restore,feed_dict)
#
#
#
#
#logits = tf.get_default_graph().get_operation_by_name("op_to_restore")
#x = tf.get_default_graph().get_operation_by_name("x:0")
#accuracy = tf.get_default_graph().get_operation_by_name("mse")
#
#sess.run([logits, accuracy], feed_dict={x: X.iloc[0]})
#
#
#
#prediction=tf.argmax(y_,1)
#prediction.eval(feed_dict=feed_dict, session=sess)
#
#prediction=tf.argmax(y_,1)
#best = sess.run([prediction],feed_dict)
#        
