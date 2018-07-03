#!/usr/bin/python

import sys ; import os ; import numpy as np ; import sklearn as skl ; import datetime as dt ; from dateutil import rrule ; from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler ; from sklearn.neural_network import MLPClassifier; from sklearn.metrics import classification_report,confusion_matrix
from sklearn.neural_network import MLPRegressor

main='/home/vkvalappil/Data/metarData/_data_mr/' ; 

st_date=str(sys.argv[1]) ; no_days=-20 ; ed_date=dt.datetime.strptime(st_date,'%Y%m%d%H')+dt.timedelta(days=no_days)
st_date1=dt.datetime.strptime(st_date,'%Y%m%d%H') #+dt.timedelta(days=1)
date_list=[x.strftime('%Y%m%d') for x in rrule.rrule(rrule.DAILY,dtstart=ed_date,until=dt.datetime.strptime(st_date,'%Y%m%d%H'))]
date_list_hour=np.vstack([x.strftime('%Y-%m-%d %H:%M') for x in rrule.rrule(rrule.HOURLY,dtstart=ed_date,until=st_date1)])   #[0:-1]


fcst_st_date=dt.datetime.strptime(st_date,'%Y%m%d%H')+dt.timedelta(hours=1) ; fcst_ed_date=dt.datetime.strptime(st_date,'%Y%m%d%H')+dt.timedelta(hours=6) ; 
fcst_date_list=[x.strftime('%Y%m%d%H') for x in rrule.rrule(rrule.HOURLY,dtstart=fcst_st_date,until=fcst_ed_date)]

outpath='/home/vkvalappil/Data/metarData/nowcasting/'+fcst_date_list[0][0:8]+'/'
if not os.path.exists(outpath) :
    os.makedirs(outpath)
outFile=outpath+'visibility_'+fcst_date_list[0]+'_'+fcst_date_list[-1]+'.csv'

data_con=np.empty((0,24))
for dte in date_list[:] :
    fileNme=main+dte[0:6]+'/AbuDhabi_'+dte+'.csv'
    data=np.genfromtxt(fileNme,delimiter=',',dtype='S')
    data_con=np.concatenate([data_con,data[1:,:]],axis=0)
    indx=np.nonzero(np.in1d(data_con[:,1],date_list_hour))[0]
    data_con1=data_con[indx,:]

hours=np.array([x[-5:-3] for x in data_con1[:,1]]) 
 
x=np.concatenate([np.vstack(hours.astype(int)),data_con1[:,4:6].astype(float),np.vstack(data_con1[:,6].astype(float)),np.vstack(data_con1[:,8]).astype(float)],axis=1) ; 
y=data_con1[:,12].astype(float)
#x=np.concatenate([np.vstack(hours.astype(int)),data_con1[:,4:8].astype(float)],axis=1) ; y=data_con1[:,12].astype(float)
x_1=np.round(x) ; y_1=np.round(y) ; x=x_1[0:-6,:] ; y=y_1[6:]

#X_train, X_test, y_train, y_test = train_test_split(x, y)
X_train=x ; y_train=y ; X_test=x_1[-6:,:] 
scaler = StandardScaler()
# Fit only to the training data

scaler.fit(X_train,X_test) 
X_train = scaler.transform(X_train) ;  X_test = scaler.transform(X_test)

#mlp = MLPClassifier(hidden_layer_sizes=(30,30,30))
#mlp = MLPRegressor(hidden_layer_sizes=(30,30,30))
mlp=MLPRegressor(hidden_layer_sizes=(30,30,30), activation='relu', solver='adam', alpha=0.001, batch_size='auto',\
                 learning_rate='constant', learning_rate_init=0.001, power_t=0.5, max_iter=500, shuffle=False,\
                 random_state=None, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,\
                 early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

mlp.fit(X_train,y_train) ; predictions = mlp.predict(X_test)*1.61 
header="date,visibility" ; header=np.vstack(np.array(header.split(","))).T

fcst_data=np.concatenate([np.vstack(fcst_date_list),np.vstack(predictions)],axis=1)
fin_mat=np.concatenate([header,fcst_data],axis=0)
np.savetxt(outFile,fin_mat,delimiter=',',fmt='%s')

#clf = MLPRegressor(alpha=0.001, hidden_layer_sizes = (30,30,30), max_iter = 500,activation = 'relu', verbose = 'True', learning_rate = 'constant') ; 
#clf.fit(X_train, y_train) ; A3=clf.predict(X_test) ; 
#print (abs(A3.astype(float)-y_test.astype(float)).mean())



#A2=abs(predictions.astype(float)-y_test.astype(float)) ; print A2.mean() 
#print(confusion_matrix(y_test,predictions))

#A1=abs(predictions.astype(float)-y_test.astype(float)) ; A1.mean()

#A2=abs(predictions.astype(float)-y_test.astype(float)) ; A2.mean() 

