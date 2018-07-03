#!/usr/bin/python

import sys ; import numpy as np ; import datetime as dt ; from dateutil import rrule ; 

main='/home/vkvalappil/Data/metarData/nowcasting/'

date=str(sys.argv[1]); date_n=(dt.datetime.strptime(date[0:8],'%Y%m%d')+dt.timedelta(days=01)).strftime('%Y%m%d')

date_1=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(hours=01)).strftime('%Y%m%d%H') ; 
date_2=(dt.datetime.strptime(date,'%Y%m%d%H')+dt.timedelta(hours=06)).strftime('%Y%m%d%H') ;


fcst_st_date=dt.datetime.strptime(date_1,'%Y%m%d%H') ; fcst_ed_date=dt.datetime.strptime(date_2,'%Y%m%d%H') 
fcst_date_list=np.vstack([x.strftime('%Y-%m-%d %H:%M') for x in rrule.rrule(rrule.HOURLY,dtstart=fcst_st_date,until=fcst_ed_date)])

nwc_file=main+date_1[0:8]+'/visibility_'+date_1+'_'+date_2+'.csv'
out_file=main+date_1[0:8]+'/acc_'+date_1+'_'+date_2+'.csv' ; print out_file
obs_file_1='/home/vkvalappil/Data/metarData/_data_mr/'+date[0:6]+'/AbuDhabi_'+date[0:8]+'.csv'
obs_file_2='/home/vkvalappil/Data/metarData/_data_mr/'+date_n[0:6]+'/AbuDhabi_'+date_n[0:8]+'.csv'

fcs_data=np.genfromtxt(nwc_file,delimiter=',',dtype='S') 

obs_data_1=np.genfromtxt(obs_file_1,delimiter=',',dtype='S') 
obs_data_2=np.genfromtxt(obs_file_2,delimiter=',',dtype='S') 
obs_data=np.concatenate([obs_data_1,obs_data_2],axis=0)

indx=np.nonzero(np.in1d(obs_data[:,1],fcst_date_list))[0]
obs_data=obs_data[indx,:] 

vis_obs=np.round(obs_data[:,12].astype(float)*1.61).astype(int) ; vis_fcs=np.round(fcs_data[1:,1].astype(float)).astype(int)
vis_diff=np.abs(vis_fcs-vis_obs) ; vis_mae=np.abs(vis_fcs-vis_obs).mean() ; vis_rmse=np.sqrt(np.square((vis_fcs-vis_obs)).mean())

vis_acc=np.zeros((8,4)).astype('S') ; vis_acc[0:6,1]=vis_diff ; vis_acc[6,1]=vis_mae ; vis_acc[7,1]=vis_rmse ; 
vis_acc[0:6,0]=fcs_data[1:,0] ; vis_acc[6,0]='mae' ; vis_acc[7,0]='rmse'
vis_acc[0:6,2]=vis_obs ; vis_acc[0:6,3]=vis_fcs ; vis_acc[6,2]='obs' ; vis_acc[6,3]='fcs'
np.savetxt(out_file,vis_acc,delimiter=',',fmt='%s')

quit()