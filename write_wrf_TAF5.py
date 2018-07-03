#/usr/bin/python
# script for extracting data frpm WRF UPP output and write TAF for Abu Dhabi airport.
# sends TAF as a mail .
# date:24/05/17
#####################################################################################################################################

import sys ; import numpy as np ; import datetime as dt ; from scipy.interpolate import interp2d
import netCDF4 as nf ; from pytz import timezone ; import shapefile ; 

############################################### Defining location, files ############################################################

main='/home/vkvalappil/Data/' ; scripts=main+'modelWRF/scripts/' ; output='/home/oceanColor/Fog/WRFmodel_forecast/TAF/'
inp='/home/oceanColor/Fog/WRFmodel_forecast/wrfouput_weatherforcast/Archivewrffogmaskwithbackground/' ; 
#date=dt.datetime.now().strftime('%Y%m%d')+'06' ; outFle=output+'wrf_TAF_'+date+'.txt' ; lstFle=scripts+'master_uae.csv'
shp_100='/home/vkvalappil/Data/alert/alert/abudhabi_100km.shp' 

date=str(sys.argv[1]) ; outFle=output+'wrf_TAF_'+date+'.txt'; lstFle=scripts+'master_uae.csv'
wrfFile=inp+'wrfpost_'+date+'.nc'

#email_id=["mtemimi@masdar.ac.ae","mjweston@masdar.ac.ae","jzhao@masdar.ac.ae","nchaouch@masdar.ac.ae","vkvalappil@masdar.ac.ae"] 
#email_id=["vkvalappil@masdar.ac.ae"]
email_id=sys.argv[2].split(',') ; #print email_id

#', '.join('"{0}"'.format(w) for w in email_id.split(','))
#print email_id


##############################################Send mail as text ########################################################################
def sendmail(file_taf,email_list) :
           from smtplib import SMTP ; from smtplib import SMTPException ; 
           from email.mime.multipart import MIMEMultipart ; from email.mime.text import MIMEText      

           _from         =   "fog@masdar.ac.ae" ;
           _to           =   email_list  ;  
           _sub          =   "TAF (WRF CESAM LAB)  "
           _attach       =   file_taf
           #_content      =   "WRF TAF DATA"
           _username     =   'fog' ;
           _password     =   'P@ssword321'
           _smtp         =   "mail.masdar.ac.ae:587" ;
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
               print "Using Gmail : Error: unable to send email :  {err}".format(err=error)   
               try:
                   _from         =   "fog.masdar@gmail.com" ;
                   _to           =   email_list;
                   _sub          =   "TAF (WRF CESAM LAB)  "
                   _attach       =   file_taf
                   #_content      =   "WRF TAF DATA"
                   _username     =   'fog.masdar' ;
                   _password     =   'fog@masdar123'
                   _smtp         =   "smtp.gmail.com:587" ;
                   #_text_subtype = "plain"
                   
                   mail=MIMEMultipart()
                   mail["Subject"]  =  _sub
                   mail["From"]     =  _from
                   mail["To"]       =  ','.join(_to) 
                   mail.attach(MIMEText(file(_attach).read()))
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

               except:
				  print 'error'
				  return "Error";

##########################################################################################################################################
def pixelsInsidePolygon(points,lattitude,longitude) :
           from matplotlib.path import Path ;
           mpath = Path( points ) ;  XY = np.dstack((longitude, lattitude)) ; XY_flat = XY.reshape((-1, 2))
           mask_flat = mpath.contains_points(XY_flat) ; mask = mask_flat.reshape(lattitude.shape) 
           return mask 

################################################# Reads Data from WRF UPP outputs ######################################################

ncfile=nf.Dataset(wrfFile,'r') ; 
lat1=ncfile.variables['lat'][:] ; lon1=ncfile.variables['lon'][:] ; 
wspd=ncfile.variables['ws_10m'][:] ; 
wdir=ncfile.variables['wd_10m'][:]
tim=ncfile.variables['time'][:] ;tim_unit=ncfile.variables['time'].units
uwnd=ncfile.variables['u_10m_tr'][:] 
vwnd=ncfile.variables['v_10m_tr'][:] ;
temp=ncfile.variables['T_2m'][:] 
fmsk=ncfile.variables['fog_mask'][:]
fprb=ncfile.variables['fog_prob'][:]
rhum=ncfile.variables['rh_2m'][:]
ncfile.close()

##########################################################################################################################################
vis_ruc=np.empty((rhum.shape)) ; 
indx1=np.where(rhum<50) ;  indx2=np.where((rhum >=50) & (rhum <=88)) ; 
indx3=np.where((rhum >88) & (rhum <=100))

#indx1=rh.where(rh<50) ; indx2=rh.where((rh>=50) & (rh <=85)) ; indx3=rh.where((rh>85) & (rh <=100))
vis_ruc[indx1]=60*np.exp(-2.5*((rhum[indx1]-15)/80))  
vis_ruc[indx2]=50*np.exp(-2.5*((rhum[indx2]-10)/85))  
vis_ruc[indx3]=(50*np.exp(-2.75*((rhum[indx3]-5)/60))) +(((-0.36)*rhum[indx3])+36)
#vis_ruc[indx3]=((-0.36)*rhum[indx3])+36

vis_ruc[vis_ruc>10]=10

##############################################################################################################################
r=shapefile.Reader(shp_100) ; shapes = r.shapes() ;
#fields=r.fields ; records = np.array(r.records())
shp_mask=pixelsInsidePolygon(shapes[0].points,lat1[:,:],lon1[:,:])
###############################################################################################################################
lat_pt=24.45  ; lon_pt=54.65 ; 
stim=0 ; etim=72 ; tint=1

ws=np.empty((etim,1)) ; wd=np.empty((etim,1)) ;  tmp=np.empty((etim,1)) ; visib=np.empty((etim,1)) ; 

for ii in xrange(stim,etim):               
    lat=lat1[:,0] ; lon=lon1[0,:]
    data_f=fprb[ii,:,:].data ; fprb_shp1=data_f[shp_mask] ; 
    thld_cnt=len(np.where(fprb_shp1>0.95)[0])
    
    if thld_cnt > 3 :  
            
            thld_indx=np.where(fprb_shp1>0.95)[0]
            fprb_shp=fprb_shp1[thld_indx].max()
            wspd_shp1=wspd[ii,shp_mask] ; wspd_shp=round((wspd_shp1[thld_indx]).min(),1) ;  
            wdir_shp1=wdir[ii,shp_mask] ; wdir_shp=round((wdir_shp1[thld_indx]).mean())
            rhum_shp1=rhum[ii,shp_mask] ; rhum_shp=round((rhum_shp1[thld_indx]).max()) 
            vis_ruc_shp1=vis_ruc[ii,shp_mask] ; vis_ruc_shp=round((vis_ruc_shp1[thld_indx]).min(),1) 
            temp_shp1=temp[ii,shp_mask] ; temp_shp=round((temp_shp1[thld_indx]).mean())                         
            ws[ii]=wspd_shp ; wd[ii]=wdir_shp ; visib[ii]=vis_ruc_shp ; tmp[ii]=temp_shp
             
    else:
            
            wspd_f=interp2d(lon,lat, wspd[ii,:,:],kind='linear',copy=False,bounds_error=True ) ; 
            wdir_f=interp2d(lon,lat, wdir[ii,:,:],kind='linear',copy=False,bounds_error=True ) ; 
            vis_ruc_f=interp2d(lon,lat, vis_ruc[ii,:,:],kind='linear',copy=False,bounds_error=True ) ; 
            temp_f=interp2d(lon,lat, temp[ii,:,:],kind='linear',copy=False,bounds_error=True ) ;         
                        
            ws_pt=np.round(wspd_f(lon_pt,lat_pt)) ; tmp_pt=np.round(temp_f(lon_pt,lat_pt)) ; 
            vis_pt=np.round(vis_ruc_f(lon_pt,lat_pt)) ; wd_pt=np.round(wdir_f(lon_pt,lat_pt))
            ws[ii]=ws_pt ; wd[ii]=wd_pt ; visib[ii]=vis_pt ; tmp[ii]=tmp_pt
            
ws=np.vstack(ws) ; wd=np.vstack(wd) ; tmp=np.vstack(tmp) ; visib=np.vstack(visib)



##############################################   Extracting Data and interpolating to locations ###########################################
noloc=1 
date_list=[d.strftime('%Y%m%d%H') for d in nf.num2date(tim,units = tim_unit)] ; 
date_list=np.delete(date_list,-1)
date_list=np.vstack(np.tile(date_list,noloc))

tid=np.vstack(np.repeat(1,72))  ; pre_mat=np.concatenate([tid,date_list],axis=1)

##############################################################################################################################

rem_data=np.genfromtxt(main+'/oppModel/output/visibility_'+date+'.csv',delimiter=',',dtype='S')
cil=rem_data[1:73,11] ; cfr=rem_data[1:73,10].astype(float)  ; #visib=rem_data[1:,6] ; 
meancld=np.vstack(cfr) ; 
#################################### adjusting CIl, removing un realistic data, check later ##################################
# only for abu Dhabi location
cil_72=cil[0:72]
u1, indices = np.unique(cil_72, return_inverse=True) ; cil_cd=u1[np.argmax(np.bincount(indices))]
cil_72[np.where(cil_72.astype(float)>1000)]=cil_cd
cil[0:72]=cil_72
cil=np.vstack((np.round(cil.astype(float)*3.28/100).astype(int)).astype(str))

##############################################################################################################################
wd[wd>360]=wd[wd>360]-360 ; tmpp=np.vstack(tmp) ; wispd=np.vstack(ws) ; wd=np.vstack(wd)

vis1=np.vstack(visib)  ; vis2=np.round((vis1.astype(float)/1.60),2).astype(str)

wispd_km=np.round(ws*3.6).astype(int) ; wispd_mi=np.round(ws*2.25).astype(int) ; wispd_kn=np.round(wispd*1.94).astype(int)

#wind short and long 
wndshrt=np.empty((wd.shape[0],wd.shape[1])).astype("S") ; wndlong=np.empty((wd.shape[0],wd.shape[1])).astype("S")
wndshrt[(wd >25)  & (wd <=70)]="NE"   ; wndlong[(wd >25)  & (wd <=70)]="NorthEast"
wndshrt[(wd >70)  & (wd <=110)]="E"   ; wndlong[(wd >70)  & (wd <=110)]="East"
wndshrt[(wd >110) & (wd <=160)]="SE"  ; wndlong[(wd >110) & (wd <=160)]="SouthEast"
wndshrt[(wd >160) & (wd <=200)]="S"   ; wndlong[(wd >160) & (wd <=200)]="South"
wndshrt[(wd >200) & (wd <=250)]="SW"  ; wndlong[(wd >200) & (wd <=250)]="SouthWest"
wndshrt[(wd >250) & (wd <=290)]="W"   ; wndlong[(wd >250) & (wd <=290)]="West"
wndshrt[(wd >290) & (wd <=340)]="NW"  ; wndlong[(wd >290) & (wd <=340)]="NorthWest"
wndshrt[((wd >340) & (wd <=360)) |((wd >0) & (wd <=25))]="N"  ;
wndlong[((wd >340) & (wd <=360)) |((wd >0) & (wd <=25))]="North"


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

wcnd[vis1.astype(float)<=1]='FG'                                      ;
wcnd[(vis1.astype(float) >1) & (vis1.astype(float)<=2)]='BR'                  ;  
wcnd[(vis1.astype(float) >2) & (vis1.astype(float) <=4)]='HZ'                  ;
wcnd[(vis1.astype(float) >4) & (vis1.astype(float) <=10)]='NSW(no significant weather)'                 


fin_mat=np.concatenate([pre_mat,wispd,wispd_km,wispd_mi,wispd_kn,wd,wndshrt,vis1,vis2,skycnd,cil,wcnd,tmpp],axis=1)


################################################# Writing TAF ####################################################################
req_mat=fin_mat[7:31,:] ; # choosing data for AbuDhabi  for required time ; need to change later , location wise 
                                                         # seperation has to be done 

req_data_1=req_mat[0:3,:] ;   

d_1=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')
d_2=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H%M')+'Z'
d_3=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_4=((dt.datetime.strptime(req_data_1[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')

d_5=((dt.datetime.strptime(req_data_1[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H')

req_data_1_1=req_mat[23:,:] ;
d_6=((dt.datetime.strptime(req_data_1_1[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%d%H')

windcnd=np.vstack(req_data_1[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_1[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_1[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_1[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data[0,6]) ; wd_shrt=(req_data[0,7])   ; ws_m=(req_data[0,2]) ; ws_mi=(req_data[0,4]) ; ws_kn=(req_data[0,5]) ;

req_data=np.vstack(req_data_1[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_1[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;

meantmp=(np.round(req_data_1[:,13].astype(float).mean()).astype(int).astype(str) +u" \u2103" ).encode('utf-8') 

taf_block_1="""  
This TAF is automatically generated by Masdar's fog detection and forecast system.
  
Data at: {}
TAF for:OMAA (Abu Dhabi Intl, --, ER)  issued at {}
Text:TAF OMAA {} {}/{} {}0{}KT 8000 NSC
Forecast period:{} to {}
Forecast type:BECOMING: standard forecast or significant change
Winds:from the {} ({} degrees) at   {} MPH ({} knots;  {} m/s)
Visibility: {} sm  (  {} km)
Clouds:{}  
Weather:{}       
Mean Temperature: {} """.format(d_1,d_2,d_2,d_5,d_6,wd,ws_kn,d_3,d_4,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn,meantmp)

####################################################################################################################################
req_data_2=req_mat[3:6,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')
d_2=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M') 
d_3=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data[0,6]) ; wd_shrt=(req_data[0,7])   ; ws_m=(req_data[0,2]) ; ws_mi=(req_data[0,4]) ; ws_kn=(req_data[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;

meantmp=(np.round(req_data_2[:,13].astype(float).mean()).astype(int).astype(str) +u" \u2103" ).encode('utf-8') 

taf_block_2="""
Text:BECMG {}/{} {}0{}KT
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  
Mean Temperature: {} """.format(d_3,d_2,wd,ws_kn,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn,meantmp)

#############################################################################################################################################
req_data_2=req_mat[6:9,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')
d_2=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M') 
d_3=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data[0,6]) ; wd_shrt=(req_data[0,7])   ; ws_m=(req_data[0,2]) ; ws_mi=(req_data[0,4]) ; ws_kn=(req_data[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;
meantmp=(np.round(req_data_2[:,13].astype(float).mean()).astype(int).astype(str) +u" \u2103" ).encode('utf-8') 

taf_block_3="""
Text:BECMG {}/{} {}0{}KT
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  
Mean Temperature: {} """.format(d_3,d_2,wd,ws_kn,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn,meantmp)

################################################################################################################################################
req_data_2=req_mat[9:12,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')
d_2=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_3=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data[0,6]) ; wd_shrt=(req_data[0,7])   ; ws_m=(req_data[0,2]) ; ws_mi=(req_data[0,4]) ; ws_kn=(req_data[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;

meantmp=(np.round(req_data_2[:,13].astype(float).mean()).astype(int).astype(str) +u" \u2103" ).encode('utf-8') 

taf_block_4="""
Text:BECMG {}/{} {}0{}KT
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  
Mean Temperature: {} """.format(d_3,d_2,wd,ws_kn,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn,meantmp)

##############################################################################################################################################
req_data_2=req_mat[12:15,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')
d_2=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_3=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data[0,6]) ; wd_shrt=(req_data[0,7])   ; ws_m=(req_data[0,2]) ; ws_mi=(req_data[0,4]) ; ws_kn=(req_data[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;
meantmp=(np.round(req_data_2[:,13].astype(float).mean()).astype(int).astype(str) +u" \u2103" ).encode('utf-8') 


taf_block_5="""
Text:BECMG {}/{} {}0{}KT
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  
Mean Temperature: {} """.format(d_3,d_2,wd,ws_kn,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn,meantmp)

#################################################################################################################################################
req_data_2=req_mat[15:18,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')
d_2=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_3=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data[0,6]) ; wd_shrt=(req_data[0,7])   ; ws_m=(req_data[0,2]) ; ws_mi=(req_data[0,4]) ; ws_kn=(req_data[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;
meantmp=(np.round(req_data_2[:,13].astype(float).mean()).astype(int).astype(str) +u" \u2103" ).encode('utf-8') 

taf_block_6="""
Text:BECMG {}/{} {}0{}KT
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  
Mean Temperature: {} """.format(d_3,d_2,wd,ws_kn,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn,meantmp)

#####################################################################################################################################################
req_data_2=req_mat[18:21,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')
d_2=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_3=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data[0,6]) ; wd_shrt=(req_data[0,7])   ; ws_m=(req_data[0,2]) ; ws_mi=(req_data[0,4]) ; ws_kn=(req_data[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;
meantmp=(np.round(req_data_2[:,13].astype(float).mean()).astype(int).astype(str) +u" \u2103" ).encode('utf-8') 

taf_block_7="""
Text:BECMG {}/{} {}0{}KT
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  
Mean Temperature: {} """.format(d_3,d_2,wd,ws_kn,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn,meantmp)


################################################################################################################################################
req_data_2=req_mat[21:24,:] ;
d_1=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')
d_2=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_3=((dt.datetime.strptime(req_data_2[0,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M')
d_4=((dt.datetime.strptime(req_data_2[-1,1],'%Y%m%d%H')).replace(tzinfo=timezone('UTC'))).strftime('%H%M %Z %d %b %Y')


windcnd=np.vstack(req_data_2[:,7]) ; u, indices = np.unique(windcnd, return_inverse=True) ; wd_shrt=u[np.argmax(np.bincount(indices))] 

viscnd=np.vstack(req_data_2[:,8]) ; u, indices = np.unique(viscnd, return_inverse=True) ; vis_cd=u[np.argmax(np.bincount(indices))] 

cldcnd=np.vstack(req_data_2[:,10]) ; u, indices = np.unique(cldcnd, return_inverse=True) ; cld_cd=u[np.argmax(np.bincount(indices))]

req_data=np.vstack(req_data_2[np.where(wd_shrt==windcnd)[0][0],:]).T
wd=(req_data[0,6]) ; wd_shrt=(req_data[0,7])   ; ws_m=(req_data[0,2]) ; ws_mi=(req_data[0,4]) ; ws_kn=(req_data[0,5]) ;

req_data=np.vstack(req_data_2[np.where(vis_cd==viscnd)[0][0],:]).T
vis_km=(req_data[0,8]) ; vis_ml=(req_data[0,9]) ;  wcdn=(req_data[0,12])

req_data=np.vstack(req_data_2[np.where(cld_cd==cldcnd)[0][0],:]).T
cldcdn=(req_data[0,10]) ; cil_feet=(req_data[0,11]) ;
meantmp=(np.round(req_data_2[:,13].astype(float).mean()).astype(int).astype(str) +u" \u2103" ).encode('utf-8') 

taf_block_8="""
Text:BECMG {}/{} {}0{}KT
Forecast period:{} to {}
Forecast type:BECOMING: Conditions expected to become as follows by {}
Winds:from the {} ({} degrees) at  {} MPH ({} knots;  {} m/s)
Visibility: {} sm   (  {} km)
Clouds:{} 
Weather:{}  
Mean Temperature: {} """.format(d_3,d_2,wd,ws_kn,d_1,d_4,d_1,wd_shrt,wd,ws_mi,ws_kn,ws_m,vis_ml,vis_km,cldcdn,wcdn,meantmp)


e_sig="""
For comments and/or questions; please contact:
Dr. Marouane Temimi, Ph.D.,
Associate Professor
Masdar Institute of Science and Technology 
Email: mtemimi@masdar.ac.ae """
#################################################Save TAF and Send as mail ###############################################################

taf_block=taf_block_1+'\n'+taf_block_2+'\n'+taf_block_3+'\n'+taf_block_4+'\n'+taf_block_5+'\n'+taf_block_6+'\n'+taf_block_7+'\n\n'+taf_block_8+'\n\n'+e_sig 

file1=open(outFle,'w') ; file1.write(taf_block) ; file1.close()
sendmail(outFle,email_id)
quit()









