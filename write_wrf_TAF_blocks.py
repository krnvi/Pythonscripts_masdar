#/usr/bin/python
# script for extracting data frpm WRF UPP output and write TAF for Abu Dhabi airport.
# sends TAF as a mail .
# date:24/05/17
#####################################################################################################################################

import sys ; import numpy as np ; import datetime as dt ; from scipy.interpolate import interp2d
import netCDF4 as nf ; from pytz import timezone

############################################### Defining location, files ############################################################

main='/home/vkvalappil/Data/' ; scripts=main+'modelWRF/scripts/' ; output='/home/oceanColor/Fog/WRFmodel_forecast/TAF/'
inp='/home/oceanColor/Fog/WRFmodel_forecast/wrfouput_weatherforcast/Archivenetcdf/' ; 
#date=dt.datetime.now().strftime('%Y%m%d')+'06' ; outFle=output+'wrf_TAF_'+date+'.txt' ; lstFle=scripts+'master_uae.csv'

date=str(sys.argv[1]) ; outFle=output+'wrf_TAF_'+date+'.txt'; lstFle=scripts+'master_uae.csv'
wndFle=inp+'windspeed_'+date+'.nc';visFle=inp+'Visibility_'+date+'.nc';uwndFle=inp+'windUcomp_'+date+'.nc';vwndFle=inp+'windVcomp_'+date+'.nc'

email_id=["mtemimi@masdar.ac.ae","mjweston@masdar.ac.ae","jzhao@masdar.ac.ae","nchaouch@masdar.ac.ae","vkvalappil@masdar.ac.ae"] 
#email_id=["vineethpk202@gmail.com","vkvalappil@masdar.ac.ae"]
##############################################Send mail as text ########################################################################

def sendmail(file_taf,email_list) :
           from smtplib import SMTP ; from smtplib import SMTPException ; 
           from email.mime.multipart import MIMEMultipart ; from email.mime.text import MIMEText      

           _from         =   "alerts.cesamlab@gmail.com" ;
           _to           =   email_list;
           _sub          =   "TAF (WRF CESAM LAB)  "
           _attach       =   file_taf
           #_content      =   "WRF TAF DATA"
           _username     =   'alerts.cesamlab' ;
           _password     =   'alert@123'
           _smtp         = "smtp.gmail.com:587" ;
           #_text_subtype = "plain"

           mail=MIMEMultipart()
           mail["Subject"]  =  _sub
           mail["From"]     =  _from
           mail["To"]       =  ','.join(_to)
           #body = MIMEMultipart('alternative')
           #body.attach(MIMEText(_content, _text_subtype ))
           mail.attach(MIMEText(file(_attach).read()))
           try:
               smtpObj = SMTP(_smtp)
               #Identify yourself to GMAIL ESMTP server.
               smtpObj.ehlo()
               #Put SMTP connection in TLS mode and call ehlo again.
               smtpObj.starttls()
               smtpObj.ehlo()
               #Login to service
               smtpObj.login(user=_username, password=_password)
               #Send email
               smtpObj.sendmail(_from, _to, mail.as_string())
               #close connection and session.
               smtpObj.quit()
           except SMTPException as error:
               print "Error: unable to send email :  {err}".format(err=error)   

################################################# Reads Data from WRF UPP outputs ######################################################
ncfile=nf.Dataset(wndFle,'r') ; 
lat=ncfile.variables['lat'][:] ; lon=ncfile.variables['lon'][:] ; 
wspd=ncfile.variables['wspeed'][:] ; tim=ncfile.variables['time'][:] ;tim_unit=ncfile.variables['time'].units
ncfile.close()

ncfile=nf.Dataset(visFle,'r') ; vis=ncfile.variables['visib'][:] ;  ncfile.close()
ncfile=nf.Dataset(uwndFle,'r') ; uwnd=ncfile.variables['u10m'][:] ; ncfile.close()
ncfile=nf.Dataset(vwndFle,'r') ; vwnd=ncfile.variables['v10m'][:] ; ncfile.close()

##############################################   Extracting Data and interpolating to locations ###########################################
lst_f=np.genfromtxt(lstFle,delimiter=',', dtype="S") ; lst_f=lst_f[lst_f[:,0].argsort(kind='mergesort')]  
points=lst_f[:,1:3].astype(float) ; noloc=points.shape[0] 

date_list=[d.strftime('%Y%m%d%H') for d in nf.num2date(tim,units = tim_unit)] ; 
date_list=np.delete(date_list,-1)
date_list=np.vstack(np.tile(date_list,noloc))

tid=np.vstack(np.repeat(lst_f[:,0],72))  ; pre_mat=np.concatenate([tid,date_list],axis=1)

stim=0 ; etim=72 ; tint=1
ws=np.empty((0,noloc)) ; u=np.empty((0,noloc)) ; v=np.empty((0,noloc)) ; visib=np.empty((0,noloc))

for i in range(stim,etim):
    wspd_f=interp2d(lon,lat, wspd[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    uwnd_f=interp2d(lon,lat, uwnd[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    vwnd_f=interp2d(lon,lat, vwnd[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    #vis_f=interp2d(lon,lat, vis[i,:,:],kind='linear',copy=False,bounds_error=True ) ; 
    
    ws=np.concatenate([ws,(np.array([wspd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    u=np.concatenate([u,(np.array([uwnd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    v=np.concatenate([v,(np.array([vwnd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    #visib=np.concatenate([visib,(np.array([vis_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
##############################################################################################################################

rem_data=np.genfromtxt(main+'/modelWRF/ARW/output/visibility_'+date+'.csv',delimiter=',',dtype='S')
visib=rem_data[1:,8] ; cil=rem_data[1:,11] ; cfr=rem_data[1:,10].astype(float)
meancld=np.vstack(cfr) ; cil=np.vstack(cil)
##############################################################################################################################
wdir=np.round(270-(np.arctan2(v,u))*(180/3.14)).astype(int)   ; wdir[wdir>360]=wdir[wdir>360]-360

wdir=np.round(wdir[0::tint]).astype(int) ; wdir=np.vstack(wdir.flatten('F'))
wispd=np.round(ws[0::tint]).astype(int) ; wispd=np.vstack(wispd.flatten('F'))
vis1=np.vstack(visib)  ; vis2=(vis1.astype(int)/1.60).astype(str)

wispd_km=np.round(wispd*3.6).astype(int) ; wispd_mi=np.round(wispd*2.25).astype(int) ; 
wispd_kn=np.round(wispd*1.94).astype(int)

#wind short and long 
wndshrt=np.empty((wdir.shape[0],wdir.shape[1])).astype("S") ; wndlong=np.empty((wdir.shape[0],wdir.shape[1])).astype("S")
wndshrt[(wdir >25)  & (wdir <=70)]="NE"   ; wndlong[(wdir >25)  & (wdir <=70)]="NorthEast"
wndshrt[(wdir >70)  & (wdir <=110)]="E"   ; wndlong[(wdir >70)  & (wdir <=110)]="East"
wndshrt[(wdir >110) & (wdir <=160)]="SE"  ; wndlong[(wdir >110) & (wdir <=160)]="SouthEast"
wndshrt[(wdir >160) & (wdir <=200)]="S"   ; wndlong[(wdir >160) & (wdir <=200)]="South"
wndshrt[(wdir >200) & (wdir <=250)]="SW"  ; wndlong[(wdir >200) & (wdir <=250)]="SouthWest"
wndshrt[(wdir >250) & (wdir <=290)]="W"   ; wndlong[(wdir >250) & (wdir <=290)]="West"
wndshrt[(wdir >290) & (wdir <=340)]="NW"  ; wndlong[(wdir >290) & (wdir <=340)]="NorthWest"
wndshrt[((wdir >340) & (wdir <=360)) |((wdir >0) & (wdir <=25))]="N"  ;
wndlong[((wdir >340) & (wdir <=360)) |((wdir >0) & (wdir <=25))]="North"


#calculating different conditions ; 
#sky condition, skyno, iconname
meancld[meancld>1]=1 ;
skycnd=np.empty((meancld.shape[0],meancld.shape[1])).astype("S") ;

skycnd[meancld<=0.125]='MISSING'             
skycnd[(meancld >0.125) & (meancld <=0.37)]='FEW'                         ;
skycnd[(meancld >0.37) & (meancld <=0.6)]='SCT'                  ;  
skycnd[(meancld >0.6) & (meancld <=0.88)]='BKN'                  ;
skycnd[(meancld >0.88) & (meancld <=1.0)]='OVC'                 


wcnd=np.empty((vis1.shape[0],vis1.shape[1])).astype("S") ;

wcnd[vis1.astype(int)<=1]='FG'                                      ;
wcnd[(vis1.astype(int) >1) & (vis1.astype(int)<=2)]='BR'                  ;  
wcnd[(vis1.astype(int) >2) & (vis1.astype(int) <=4)]='HZ'                  ;
wcnd[(vis1.astype(int) >4) & (vis1.astype(int) <=10)]='NSW(no significant weather)'                 


fin_mat=np.concatenate([pre_mat,wispd,wispd_km,wispd_mi,wispd_kn,wdir,wndshrt,vis1,vis2,skycnd,cil,wcnd],axis=1)


################################################# Writing TAF ####################################################################
req_data_1=fin_mat[0:4,:] ;   # choosing data for AbuDhabi  for required time ; need to change later , location wise 
                                                         # seperation has to be done 

d_1=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')
d_2=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H%M')+'Z'
d_3=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_4=((dt.datetime.strptime(req_data_1[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %d %b %Y')

d_5=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H')

req_data_1_1=fin_mat[23:27,:] ;
d_6=((dt.datetime.strptime(req_data_1_1[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H')

windcnd=np.vstack(req_data_1[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_1[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_1[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_1[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data_1[0,6]) ; wd_shrt=(req_data_1[0,7])   ; ws_m=(req_data_1[0,2]) ; ws_mi=(req_data_1[0,4]) ; ws_kn=(req_data_1[0,5]) ;

req_data=np.vstack(req_data_1[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_1[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;

taf_block_1="""  
WRF CESAM LAB TAF Data  
Data at: {}
TAF for:OMAA (Abu Dhabi Intl, --, ER)  issued at {}
Text:TAF OMAA {} {}/{} {}0{}KT 8000 NSC
Forecast period:{} to {}
Forecast type:FROM: standard forecast or significant change
Winds:from the {} ({} degrees) at   {} MPH ({} knots;  {} m/s)
Visibility: {} sm  (  {} km)
Clouds:{}  
Weather:{}       """.format(d_1,d_2,d_2,d_5,d_6,wd,ws_kn,d_3,d_4,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn)

####################################################################################################################################
req_data_2=fin_mat[3:7,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')

d_2=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y') 
d_3=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H%M') + 'Z'

d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data_2[0,6]) ; wd_shrt=(req_data_2[0,7])   ; ws_m=(req_data_2[0,2]) ; ws_mi=(req_data_2[0,4]) ; ws_kn=(req_data_2[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;


wd=(req_data_2[1,6]) ; wd_shrt=(req_data_2[1,7]) ; ws_m=(req_data_2[1,2]) ; ws_mi=(req_data_2[1,4]) ; 
ws_kn=(req_data_2[1,5]) ; vis_km=(req_data_2[1,8]) ; vis_ml=(req_data_2[1,9])
cldcdn=(req_data_2[1,10]) ; cil_feet=(req_data_2[1,11]) ; wcdn=(req_data_2[1,12])

taf_block_2="""
WRF CESAM LAB TAF Data  
Data at: {}
TAF for:OMAA (Abu Dhabi Intl, --, ER)  issued at {}

Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  """.format(d_2,d_3,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn)

outFle=output+'wrf_TAF_'+date+'_'+req_data_2[0,1]+'.txt'
file1=open(outFle,'w') ; file1.write(taf_block_2) ; file1.close()


#############################################################################################################################################
req_data_2=fin_mat[7:11,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')

d_2=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y') 
d_3=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H%M') + 'Z'

d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data_2[0,6]) ; wd_shrt=(req_data_2[0,7])   ; ws_m=(req_data_2[0,2]) ; ws_mi=(req_data_2[0,4]) ; ws_kn=(req_data_2[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;


wd=(req_data_2[1,6]) ; wd_shrt=(req_data_2[1,7]) ; ws_m=(req_data_2[1,2]) ; ws_mi=(req_data_2[1,4]) ; 
ws_kn=(req_data_2[1,5]) ; vis_km=(req_data_2[1,8]) ; vis_ml=(req_data_2[1,9])
cldcdn=(req_data_2[1,10]) ; cil_feet=(req_data_2[1,11]) ; wcdn=(req_data_2[1,12])

taf_block_3="""
WRF CESAM LAB TAF Data  
Data at: {}
TAF for:OMAA (Abu Dhabi Intl, --, ER)  issued at {}

Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  """.format(d_2,d_3,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn)

outFle=output+'wrf_TAF_'+date+'_'+req_data_2[0,1]+'.txt'
file1=open(outFle,'w') ; file1.write(taf_block_3) ; file1.close()

################################################################################################################################################
req_data_2=fin_mat[11:15,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')

d_2=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y') 
d_3=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H%M') + 'Z'

d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data_2[0,6]) ; wd_shrt=(req_data_2[0,7])   ; ws_m=(req_data_2[0,2]) ; ws_mi=(req_data_2[0,4]) ; ws_kn=(req_data_2[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;


wd=(req_data_2[1,6]) ; wd_shrt=(req_data_2[1,7]) ; ws_m=(req_data_2[1,2]) ; ws_mi=(req_data_2[1,4]) ; 
ws_kn=(req_data_2[1,5]) ; vis_km=(req_data_2[1,8]) ; vis_ml=(req_data_2[1,9])
cldcdn=(req_data_2[1,10]) ; cil_feet=(req_data_2[1,11]) ; wcdn=(req_data_2[1,12])

taf_block_4="""
WRF CESAM LAB TAF Data  
Data at: {}
TAF for:OMAA (Abu Dhabi Intl, --, ER)  issued at {}
 
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  """.format(d_2,d_3,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn)

outFle=output+'wrf_TAF_'+date+'_'+req_data_2[0,1]+'.txt'
file1=open(outFle,'w') ; file1.write(taf_block_4) ; file1.close()

##############################################################################################################################################
req_data_2=fin_mat[15:19,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')

d_2=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y') 
d_3=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H%M') + 'Z'

d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data_2[0,6]) ; wd_shrt=(req_data_2[0,7])   ; ws_m=(req_data_2[0,2]) ; ws_mi=(req_data_2[0,4]) ; ws_kn=(req_data_2[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;


wd=(req_data_2[1,6]) ; wd_shrt=(req_data_2[1,7]) ; ws_m=(req_data_2[1,2]) ; ws_mi=(req_data_2[1,4]) ; 
ws_kn=(req_data_2[1,5]) ; vis_km=(req_data_2[1,8]) ; vis_ml=(req_data_2[1,9])
cldcdn=(req_data_2[1,10]) ; cil_feet=(req_data_2[1,11]) ; wcdn=(req_data_2[1,12])

taf_block_5="""
WRF CESAM LAB TAF Data  
Data at: {}
TAF for:OMAA (Abu Dhabi Intl, --, ER)  issued at {}
 
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  """.format(d_2,d_3,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn)

outFle=output+'wrf_TAF_'+date+'_'+req_data_2[0,1]+'.txt'
file1=open(outFle,'w') ; file1.write(taf_block_5) ; file1.close()


#################################################################################################################################################
req_data_2=fin_mat[19:23,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')

d_2=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y') 
d_3=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H%M') + 'Z'

d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data_2[0,6]) ; wd_shrt=(req_data_2[0,7])   ; ws_m=(req_data_2[0,2]) ; ws_mi=(req_data_2[0,4]) ; ws_kn=(req_data_2[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;


wd=(req_data_2[1,6]) ; wd_shrt=(req_data_2[1,7]) ; ws_m=(req_data_2[1,2]) ; ws_mi=(req_data_2[1,4]) ; 
ws_kn=(req_data_2[1,5]) ; vis_km=(req_data_2[1,8]) ; vis_ml=(req_data_2[1,9])
cldcdn=(req_data_2[1,10]) ; cil_feet=(req_data_2[1,11]) ; wcdn=(req_data_2[1,12])

taf_block_6="""
WRF CESAM LAB TAF Data  
Data at: {}
TAF for:OMAA (Abu Dhabi Intl, --, ER)  issued at {}
 
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  """.format(d_2,d_3,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn)

outFle=output+'wrf_TAF_'+date+'_'+req_data_2[0,1]+'.txt'
file1=open(outFle,'w') ; file1.write(taf_block_6) ; file1.close()

#####################################################################################################################################################
req_data_2=fin_mat[23:27,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')

d_2=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y') 
d_3=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H%M') + 'Z'

d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data_2[0,6]) ; wd_shrt=(req_data_2[0,7])   ; ws_m=(req_data_2[0,2]) ; ws_mi=(req_data_2[0,4]) ; ws_kn=(req_data_2[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;


wd=(req_data_2[1,6]) ; wd_shrt=(req_data_2[1,7]) ; ws_m=(req_data_2[1,2]) ; ws_mi=(req_data_2[1,4]) ; 
ws_kn=(req_data_2[1,5]) ; vis_km=(req_data_2[1,8]) ; vis_ml=(req_data_2[1,9])
cldcdn=(req_data_2[1,10]) ; cil_feet=(req_data_2[1,11]) ; wcdn=(req_data_2[1,12])

taf_block_7="""
WRF CESAM LAB TAF Data  
Data at: {}
TAF for:OMAA (Abu Dhabi Intl, --, ER)  issued at {}
  
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  """.format(d_2,d_3,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn)

outFle=output+'wrf_TAF_'+date+'_'+req_data_2[0,1]+'.txt'
file1=open(outFle,'w') ; file1.write(taf_block_7) ; file1.close()

#################################################Save TAF and Send as mail ###############################################################


#sendmail(outFle,email_id)
quit()









