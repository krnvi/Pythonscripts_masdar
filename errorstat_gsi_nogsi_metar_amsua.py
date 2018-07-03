#!/usr/bin/python

import os ; import numpy as np ; import datetime as dt ; from dateutil import tz, rrule ; 
#import matplotlib.pyplot as plt; #import seaborn as sns ;

date_list=[x.strftime('%Y%m%d') for x in rrule.rrule(rrule.DAILY,dtstart=dt.datetime.strptime('20170601','%Y%m%d'),until=dt.datetime.strptime('20170630','%Y%m%d'))]
l_idx_s=6; l_idx_e=30 ;

for dte in date_list[:]: 

    main='/home/vkvalappil/Data/' ; date=dte+'06' ; 
    output=main+'modelWRF/ARW/output/gsi_plots/rad_sens/amsua_iasi_J/' +str(l_idx_s)+'_'+str(l_idx_e)+'hour/'+date+'/'
    if not os.path.exists(output)   :
        os.makedirs(output)

    gsiFile_1=main+'modelWRF/ARW/output/GFS_ENKF/gsi_opp/newBe/gsi_radiance_sensitivity/amsua_J/hourly'+date+'_d02_amsua_J.csv'
    gsiFile_2=main+'modelWRF/ARW/output/GFS_ENKF/gsi_opp/newBe/gsi_radiance_sensitivity/iasi_J/hourly'+date+'_d02_iasi_J.csv'
    gsiFile_3=main+'modelWRF/ARW/output/GFS_ENKF/gsi_opp/newBe/gsi_radiance_sensitivity/amsua+iasi_J/hourly'+date+'_d02_amsua+iasi_J.csv'

    #gsiFile_3=main+'modelWRF/ARW/output/GFS_ENKF/gsi_opp/newBe/gsi_radiance_sensitivity/'+date+'/hourly'+date+'_d02_iasi.csv'
    #gsiFile_5=main+'modelWRF/ARW/output/GFS_ENKF/gsi_opp/newBe/gsi_radiance_sensitivity/'+date+'/hourly'+date+'_d02_seviri.csv'
    #gsiFile_4=main+'modelWRF/ARW/output/GFS_ENKF/gsi_opp/newBe/gsi_radiance_sensitivity/'+date+'/hourly'+date+'_d02_amsua+iasi.csv'
    #gsiFile_7=main+'modelWRF/ARW/output/GFS_ENKF/gsi_opp/newBe/gsi_radiance_sensitivity/'+date+'/hourly'+date+'_d02_amsua+hirs.csv'
#   gsiFile_8=main+'modelWRF/ARW/output/GFS_ENKF/gsi_opp/newBe/gsi_radiance_sensitivity/'+date+'/hourly'+date+'_d02_amsua+mhs.csv'


    #gsiFile=main+'modelWRF/oppModel/ARW/output/hourly'+date+'_d02.csv'

    nogFile=main+'modelWRF_2/ARW/output/no_gsi_0.25/hourly'+date+'_d02.csv'

    lstFile=main+'modelWRF/scripts/master_uae.csv'

    lst_f=np.genfromtxt(lstFile,delimiter=',',dtype='S')
    g_data_1=np.genfromtxt(gsiFile_1,delimiter=',',dtype='S') ; 
    g_data_2=np.genfromtxt(gsiFile_2,delimiter=',',dtype='S') ; 
    g_data_3=np.genfromtxt(gsiFile_3,delimiter=',',dtype='S') ; 

    #g_data_4=np.genfromtxt(gsiFile_4,delimiter=',',dtype='S') ; 
    #g_data_5=np.genfromtxt(gsiFile_5,delimiter=',',dtype='S') ; 
    #g_data_6=np.genfromtxt(gsiFile_6,delimiter=',',dtype='S') ; 
    #g_data_7=np.genfromtxt(gsiFile_7,delimiter=',',dtype='S') ; 
    #g_data_8=np.genfromtxt(gsiFile_8,delimiter=',',dtype='S') ; 

    ng_data=np.genfromtxt(nogFile,delimiter=',',dtype='S')

    temp_cons_bias=np.empty((0,5)) ; rh_cons_bias=np.empty((0,5)) ; 
    dt_cons_bias=np.empty((0,5)) ; mr_cons_bias=np.empty((0,5)) ; 
    temp_cons_mae=np.empty((0,5)) ; temp_cons_rmse=np.empty((0,5)) ; 
    rh_cons_mae=np.empty((0,5)) ; rh_cons_rmse=np.empty((0,5)) ; 
    dt_cons_mae=np.empty((0,5)) ; dt_cons_rmse=np.empty((0,5)) ; 
    mr_cons_mae=np.empty((0,5)) ; mr_cons_rmse=np.empty((0,5)) ; 

    for ii in range(0,lst_f.shape[0]) : 
        tid=lst_f[ii,0] ; locNme=lst_f[ii,-1]  ; 
        g_req_data_1=g_data_1[np.where(g_data_1[:,0]==tid)[0],:]    
        g_req_data_2=g_data_2[np.where(g_data_2[:,0]==tid)[0],:]    
        g_req_data_3=g_data_3[np.where(g_data_3[:,0]==tid)[0],:]    

    #    g_req_data_4=g_data_4[np.where(g_data_4[:,0]==tid)[0],:]    
    #    g_req_data_5=g_data_5[np.where(g_data_5[:,0]==tid)[0],:]    
    #    g_req_data_6=g_data_6[np.where(g_data_6[:,0]==tid)[0],:]    
    #    g_req_data_7=g_data_7[np.where(g_data_7[:,0]==tid)[0],:]    
    #    g_req_data_8=g_data_8[np.where(g_data_8[:,0]==tid)[0],:]
    
        ng_req_data=ng_data[np.where(ng_data[:,0]==tid)[0],:]    
 
        f_date=g_req_data_1[:,3][::24] ; date_1=dt.datetime.strptime(f_date[0],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
        date_2=dt.datetime.strptime(f_date[1],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d') ; 
        date_3=dt.datetime.strptime(f_date[2],'%Y-%m-%d %H:%M:%S').strftime('%Y%m%d');
    
        rs_file_1='/home/vkvalappil/Data/metarData/'+date_1[0:6]+'/'+locNme+'_'+date_1+'.csv'
        rs_file_2='/home/vkvalappil/Data/metarData/'+date_2[0:6]+'/'+locNme+'_'+date_2+'.csv'
        rs_file_3='/home/vkvalappil/Data/metarData/'+date_3[0:6]+'/'+locNme+'_'+date_3+'.csv' 
    
        rs_data_1=np.genfromtxt(rs_file_1,delimiter=',',dtype='S')
        rs_data_2=np.genfromtxt(rs_file_2,delimiter=',',dtype='S')
        rs_data_3=np.genfromtxt(rs_file_3,delimiter=',',dtype='S')
    
        rs_data=np.concatenate([rs_data_1[1:,:],rs_data_2[1:,:],rs_data_3[1:,:]],axis=0)    
    
        from_zone = tz.gettz('Asia/Dubai') ; to_zone = tz.gettz('UTC') ;
        date_list=np.array([(dt.datetime.strptime(x,'%Y-%m-%d %H:%M:%S')).replace(tzinfo=from_zone).astimezone(to_zone).strftime('%Y-%m-%d %H:%M') for x in g_req_data_1[:,3]]); 
        rs_req_data=rs_data[np.where(np.in1d(rs_data[:,1],date_list))[0],:]    
     
    
##################################################Temperature ##########################################################################################    
    
   
        data_1=g_req_data_1[l_idx_s:l_idx_e,5].astype(float) ; 
        data_2=g_req_data_2[l_idx_s:l_idx_e,5].astype(float) ; 
        data_3=g_req_data_3[l_idx_s:l_idx_e,5].astype(float) ; 

    #    data_4=g_req_data_4[l_idx_s:l_idx_e,5].astype(float) ; 
    #    data_5=g_req_data_5[l_idx_s:l_idx_e,5].astype(float) ; 
    #    data_6=g_req_data_6[l_idx_s:l_idx_e,5].astype(float) ; 
    #    data_7=g_req_data_7[l_idx_s:l_idx_e,5].astype(float) ; 
    #    data_8=g_req_data_8[l_idx_s:l_idx_e,5].astype(float) ; 
   
        data_ng=ng_req_data[l_idx_s:l_idx_e,5].astype(float) ; obs=rs_req_data[l_idx_s:l_idx_e,4].astype(float)

        temp_bias_1=(data_1-obs).mean() ; 
        temp_bias_2=(data_2-obs).mean() ; 
        temp_bias_3=(data_3-obs).mean() ; 
        temp_bias_ng=(data_ng-obs).mean() ; 
   
   
        temp_mae_1=np.abs(data_1-obs).mean() ; 
        temp_mae_2=np.abs(data_2-obs).mean() ; 
        temp_mae_3=np.abs(data_3-obs).mean() ; 

    #    temp_mae_4=np.abs(data_4-obs).mean() ; 
        temp_mae_ng=np.abs(data_ng-obs).mean() ; 
 
        temp_rmse_1=np.sqrt(np.square(data_1-obs).mean()) ; 
        temp_rmse_2=np.sqrt(np.square(data_2-obs).mean()) ; 
        temp_rmse_3=np.sqrt(np.square(data_3-obs).mean()) ; 

    #    temp_rmse_4=np.sqrt(np.square(data_4-obs).mean()) ; 
        temp_rmse_ng=np.sqrt(np.square(data_ng-obs).mean()) ; 

        temp_bias=np.vstack([locNme,temp_bias_1,temp_bias_2,temp_bias_3,temp_bias_ng]).T
        temp_mae=np.vstack([locNme,temp_mae_1,temp_mae_2,temp_mae_3,temp_mae_ng]).T
        temp_rmse=np.vstack([locNme,temp_rmse_1,temp_rmse_2,temp_rmse_3,temp_rmse_ng]).T

        temp_cons_bias=np.concatenate([temp_cons_bias,temp_bias],axis=0)
        temp_cons_mae=np.concatenate([temp_cons_mae,temp_mae],axis=0)
        temp_cons_rmse=np.concatenate([temp_cons_rmse,temp_rmse],axis=0)

    
##########################################Relative Hum #############################################################    
    
   
    
        data_1=g_req_data_1[l_idx_s:l_idx_e,7].astype(float) ; 
        data_2=g_req_data_2[l_idx_s:l_idx_e,7].astype(float) ; 
        data_3=g_req_data_3[l_idx_s:l_idx_e,7].astype(float) ; 

    #    data_4=g_req_data_4[l_idx_s:l_idx_e,7].astype(float) ; 
    #    data_5=g_req_data_5[l_idx_s:l_idx_e,7].astype(float) ; 
    #    data_6=g_req_data_6[l_idx_s:l_idx_e,7].astype(float) ; 
    #    data_7=g_req_data_7[l_idx_s:l_idx_e,7].astype(float) ; 
    #    data_8=g_req_data_8[l_idx_s:l_idx_e,7].astype(float) ; 
    
        data_ng=ng_req_data[l_idx_s:l_idx_e,7].astype(float) ; obs=np.round(rs_req_data[l_idx_s:l_idx_e,6].astype(float))


        rh_bias_1=(data_1-obs).mean() ; 
        rh_bias_2=(data_2-obs).mean() ; 
        rh_bias_3=(data_3-obs).mean() ; 
        rh_bias_ng=(data_ng-obs).mean() 
    
        rh_mae_1=np.abs(data_1-obs).mean() ; 
        rh_mae_2=np.abs(data_2-obs).mean() ; 
        rh_mae_3=np.abs(data_3-obs).mean() ; 

    #    rh_mae_4=np.abs(data_4-obs).mean() ; 
        rh_mae_ng=np.abs(data_ng-obs).mean() ; 
 
        rh_rmse_1=np.sqrt(np.square(data_1-obs).mean()) ; 
        rh_rmse_2=np.sqrt(np.square(data_2-obs).mean()) ; 
        rh_rmse_3=np.sqrt(np.square(data_3-obs).mean()) ; 

    #    rh_rmse_4=np.sqrt(np.square(data_4-obs).mean()) ; 
        rh_rmse_ng=np.sqrt(np.square(data_ng-obs).mean()) ; 

        rh_bias=np.vstack([locNme,rh_bias_1,rh_bias_2,rh_bias_3,rh_bias_ng]).T
        rh_mae=np.vstack([locNme,rh_mae_1,rh_mae_2,rh_mae_3,rh_mae_ng]).T
        rh_rmse=np.vstack([locNme,rh_rmse_1,rh_rmse_2,rh_rmse_3,rh_rmse_ng]).T    
    
        rh_cons_mae=np.concatenate([rh_cons_mae,rh_mae],axis=0)
        rh_cons_rmse=np.concatenate([rh_cons_rmse,rh_rmse],axis=0)
        rh_cons_bias=np.concatenate([rh_cons_bias,rh_bias],axis=0)
    
    
    
###################################################Dew temp ######################################################    
    
        data_1=g_req_data_1[l_idx_s:l_idx_e,6].astype(float) ; 
        data_2=g_req_data_2[l_idx_s:l_idx_e,6].astype(float) ; 
        data_3=g_req_data_3[l_idx_s:l_idx_e,6].astype(float) ; 

    #    data_4=g_req_data_4[l_idx_s:l_idx_e,6].astype(float) ; 
    #    data_5=g_req_data_5[l_idx_s:l_idx_e,6].astype(float) ; 
    #    data_6=g_req_data_6[l_idx_s:l_idx_e,6].astype(float) ; 
    #    data_7=g_req_data_7[l_idx_s:l_idx_e,6].astype(float) ; 
    #    data_8=g_req_data_8[l_idx_s:l_idx_e,6].astype(float) ; 
    
    
        data_ng=ng_req_data[l_idx_s:l_idx_e,6].astype(float) ; obs=np.round(rs_req_data[l_idx_s:l_idx_e,5].astype(float))
    
        dt_bias_1=(data_1-obs).mean() ; 
        dt_bias_2=(data_2-obs).mean() ; 
        dt_bias_3=(data_3-obs).mean() ; 
        dt_bias_ng=(data_ng-obs).mean() ; 

        dt_mae_1=np.abs(data_1-obs).mean() ; 
        dt_mae_2=np.abs(data_2-obs).mean() ; 
        dt_mae_3=np.abs(data_3-obs).mean() ; 

#       dt_mae_4=np.abs(data_4-obs).mean() ; 
        dt_mae_ng=np.abs(data_ng-obs).mean() ; 
 
        dt_rmse_1=np.sqrt(np.square(data_1-obs).mean()) ; 
        dt_rmse_2=np.sqrt(np.square(data_2-obs).mean()) ; 
        dt_rmse_3=np.sqrt(np.square(data_3-obs).mean()) ; 

#    dt_rmse_4=np.sqrt(np.square(data_4-obs).mean()) ; 
        dt_rmse_ng=np.sqrt(np.square(data_ng-obs).mean()) ; 

        dt_bias=np.vstack([locNme,dt_bias_1,dt_bias_2,dt_bias_3,dt_bias_ng]).T
        dt_mae=np.vstack([locNme,dt_mae_1,dt_mae_2,dt_mae_3,dt_mae_ng]).T
        dt_rmse=np.vstack([locNme,dt_rmse_1,dt_rmse_2,dt_rmse_3,dt_rmse_ng]).T    
    
        dt_cons_mae=np.concatenate([dt_cons_mae,dt_mae],axis=0)
        dt_cons_rmse=np.concatenate([dt_cons_rmse,dt_rmse],axis=0)
        dt_cons_bias=np.concatenate([dt_cons_bias,dt_bias],axis=0)


############################################### Mix ratio #######################################################    
    
        data_1=g_req_data_1[l_idx_s:l_idx_e,10].astype(float) ; 
        data_2=g_req_data_2[l_idx_s:l_idx_e,10].astype(float) ; 
        data_3=g_req_data_3[l_idx_s:l_idx_e,10].astype(float) ; 

    #    data_4=g_req_data_4[l_idx_s:l_idx_e,10].astype(float) ; 
    #    data_5=g_req_data_5[l_idx_s:l_idx_e,10].astype(float) ; 
    #    data_6=g_req_data_6[l_idx_s:l_idx_e,10].astype(float)  ; 
    #    data_7=g_req_data_7[l_idx_s:l_idx_e,10].astype(float)  ; 
    #    data_8=g_req_data_8[l_idx_s:l_idx_e,10].astype(float)  ; 
    #    
    
        data_ng=ng_req_data[l_idx_s:l_idx_e,10].astype(float) ; obs=rs_req_data[l_idx_s:l_idx_e,11].astype(float) 
    
        mr_bias_1=np.abs(data_1-obs).mean() ; 
        mr_bias_2=np.abs(data_2-obs).mean() ; 
        mr_bias_3=np.abs(data_3-obs).mean() ; 
        mr_bias_ng=np.abs(data_ng-obs).mean() ; 
    
        mr_mae_1=np.abs(data_1-obs).mean() ; 
        mr_mae_2=np.abs(data_2-obs).mean() ; 
        mr_mae_3=np.abs(data_3-obs).mean() ; 

    #    mr_mae_4=np.abs(data_4-obs).mean() ; 
        mr_mae_ng=np.abs(data_ng-obs).mean() ; 
 
        mr_rmse_1=np.sqrt(np.square(data_1-obs).mean()) ; 
        mr_rmse_2=np.sqrt(np.square(data_2-obs).mean()) ; 
        mr_rmse_3=np.sqrt(np.square(data_3-obs).mean()) ; 

    #    mr_rmse_4=np.sqrt(np.square(data_4-obs).mean()) ; 
        mr_rmse_ng=np.sqrt(np.square(data_ng-obs).mean()) ; 

        mr_bias=np.vstack([locNme,mr_bias_1,mr_bias_2,mr_bias_3,mr_bias_ng]).T
        mr_mae=np.vstack([locNme,mr_mae_1,mr_mae_2,mr_mae_3,mr_mae_ng]).T
        mr_rmse=np.vstack([locNme,mr_rmse_1,mr_rmse_2,mr_rmse_3,mr_rmse_ng]).T    

        mr_cons_mae=np.concatenate([mr_cons_mae,mr_mae],axis=0)
        mr_cons_rmse=np.concatenate([mr_cons_rmse,mr_rmse],axis=0)
        mr_cons_bias=np.concatenate([mr_cons_bias,mr_bias],axis=0)


    header='locname,amsua,iasi,iasi+amsua,noDa' ; 
    header=np.vstack(np.array(header.split(","))).T

    temp_cons_bias=np.concatenate([header,temp_cons_bias],axis=0)
    rh_cons_bias=np.concatenate([header,rh_cons_bias],axis=0)
    dt_cons_bias=np.concatenate([header,dt_cons_bias],axis=0)
    mr_cons_bias=np.concatenate([header,mr_cons_bias],axis=0)

    temp_cons_mae=np.concatenate([header,temp_cons_mae],axis=0)
    rh_cons_mae=np.concatenate([header,rh_cons_mae],axis=0)
    dt_cons_mae=np.concatenate([header,dt_cons_mae],axis=0)
    mr_cons_mae=np.concatenate([header,mr_cons_mae],axis=0)

    temp_cons_rmse=np.concatenate([header,temp_cons_rmse],axis=0)
    rh_cons_rmse=np.concatenate([header,rh_cons_rmse],axis=0)
    dt_cons_rmse=np.concatenate([header,dt_cons_rmse],axis=0)
    mr_cons_rmse=np.concatenate([header,mr_cons_rmse],axis=0)

    outFile_mr_bias=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'bias_mixr_2m_'+date+'.csv'
    outFile_dt_bias=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'bias_dewtemp_2m_'+date+'.csv' 
    outFile_rh_bias=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'bias_rh_2m_'+date+'.csv' 
    outFile_temp_bias=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'bias_temperature_2m_'+date+'.csv'

    outFile_mr_mae=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'mae_mixr_2m_'+date+'.csv'
    outFile_dt_mae=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'mae_dewtemp_2m_'+date+'.csv' 
    outFile_rh_mae=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'mae_rh_2m_'+date+'.csv' 
    outFile_temp_mae=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'mae_temperature_2m_'+date+'.csv'


    outFile_mr_rmse=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'rmse_mixr_2m_'+date+'.csv'
    outFile_dt_rmse=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'rmse_dewtemp_2m_'+date+'.csv' 
    outFile_rh_rmse=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'rmse_rh_2m_'+date+'.csv' 
    outFile_temp_rmse=output+'/'+str(l_idx_s)+'_'+str(l_idx_e)+'rmse_temperature_2m_'+date+'.csv'


    np.savetxt(outFile_temp_bias,temp_cons_bias,delimiter=',',fmt='%s')
    np.savetxt(outFile_rh_bias,rh_cons_bias,delimiter=',',fmt='%s')
    np.savetxt(outFile_dt_bias,dt_cons_bias,delimiter=',',fmt='%s')
    np.savetxt(outFile_mr_bias,mr_cons_bias,delimiter=',',fmt='%s')

    np.savetxt(outFile_temp_mae,temp_cons_mae,delimiter=',',fmt='%s')
    np.savetxt(outFile_rh_mae,rh_cons_mae,delimiter=',',fmt='%s')
    np.savetxt(outFile_dt_mae,dt_cons_mae,delimiter=',',fmt='%s')
    np.savetxt(outFile_mr_mae,mr_cons_mae,delimiter=',',fmt='%s')

    np.savetxt(outFile_temp_rmse,temp_cons_rmse,delimiter=',',fmt='%s')
    np.savetxt(outFile_rh_rmse,rh_cons_rmse,delimiter=',',fmt='%s')
    np.savetxt(outFile_dt_rmse,dt_cons_rmse,delimiter=',',fmt='%s')
    np.savetxt(outFile_mr_rmse,mr_cons_rmse,delimiter=',',fmt='%s')



#################################################################################################################



    