#/usr/bin/python
################################ National Data Extraction ######################################################################################
#importing necessary modules
import sys ; import numpy as np ; import scipy as sp ; from scipy.interpolate import interp2d ; import datetime as dt
from scipy.interpolate import griddata ; import datetime ; import time ; import pygrib as pg ;from dateutil import rrule

start_time = time.time()
#define paths
main='/home/OldData/modelWRF/NMMV3.7' ; scripts=main+'/scripts/' ; output=main+'/output/'
date=str(sys.argv[1]) ;  fcs_leaddays=3 ; #provide date as argument, forecast start and end date defined
fcs_st_date=dt.datetime.strptime(date,'%Y%m%d') ; fcs_ed_date=(dt.datetime.strptime(date,'%Y%m%d')+dt.timedelta(days=fcs_leaddays-1));  
date_list=[x.strftime('%d%m%y') for x in rrule.rrule(rrule.DAILY,dtstart=fcs_st_date,until=fcs_ed_date)] ; #forecast start and end datelist 
day_list=np.array(range(0,fcs_leaddays)) # define forecast day sequence 
#define input and output file names files 
lstFle=main+'/scripts/master_uae.csv'
modFile=main+'/UPPV3.0/run/poutpost/' + date +'00_NODA/wrfpost_d01.'+date+'00'
outFile=output+'24hourly'+date+'00.csv' ; 

# Reading data from lst file and model output files
lst_f=np.genfromtxt(lstFle,delimiter=',', dtype="S") ; lst_f=lst_f[lst_f[:,0].argsort(kind='mergesort')]  
points=lst_f[:,1:3].astype(float) ; noloc=points.shape[0] 

grb_f=pg.open(modFile) ; 
tmp=(np.array(grb_f.select(name="2 metre temperature"))) 
ugrd=(np.array(grb_f.select(name="10 metre U wind component"))) 
vgrd=(np.array(grb_f.select(name="10 metre V wind component"))) 
LCDClcl=(np.array(grb_f.select(name="Low cloud cover"))) 
MCDCmcl=(np.array(grb_f.select(name="Medium cloud cover"))) 
HCDChcl=(np.array(grb_f.select(name="High cloud cover"))) 
RH=(np.array(grb_f.select(name="Relative humidity"))) 
DPT=(np.array(grb_f.select(name="2 metre dewpoint temperature"))) 
TSOIL=(np.array(grb_f.select(name="Soil Temperature"))) 
#SOILW=(np.array(grb_f.select(name="Soil Moisture")))  
#snowcsfc=(np.array(grb_f.select(name="Snow Cover"))) 
APCPsfc=(np.array(grb_f.select(name="Total Precipitation"))) 
grb_f.close()

#lat, lon=tmp[1].latlons()
lat=tmp[0].data()[1] ; lon=tmp[0].data()[2] ; 
#time intervel, start time and end time defined. 
tint=24 ; stim=0 ; etim=72 ; #tmp.shape[0]-1 

#date,tehsil id abd day seq arranged according to required format.
f_date=np.vstack(np.tile(date_list,noloc)) ; c_date=np.vstack(np.repeat(fcs_st_date.strftime('%Y-%m-%d'),noloc*fcs_leaddays))
tid=np.vstack(np.repeat(lst_f[:,0],fcs_leaddays)) ; pre_mat=np.concatenate([tid,c_date,f_date],axis=1)
day_seq=np.vstack(np.tile(day_list,noloc))
lat=np.vstack(lat[:,0]) ; #lat=lat[::-1] 
lon=np.vstack(lon[0,:])
#defined empty arrays. 
temp=np.empty((0,noloc)) ; uwnd=np.empty((0,noloc)) ; vwnd=np.empty((0,noloc))
lcdc=np.empty((0,noloc)) ; mcdc=np.empty((0,noloc)) ; hcdc=np.empty((0,noloc))
rhum=np.empty((0,noloc)) ; dtemp=np.empty((0,noloc)); stemp=np.empty((0,noloc))
rain=np.empty((0,noloc)) ; cldfrn=np.empty((0,noloc)) ; 

#start_time = time.time()
#below loop will do the interpolation to the required location
for i in range(stim,etim):
    tmp1=tmp[i].data()
    tmp_f=interp2d(lon,lat, tmp1[0]-273.15,kind='linear',copy=False,bounds_error=True ) ; 
    #temp=np.concatenate([temp,(np.array([tmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)

    ugrd1=ugrd[i].data()    
    ugrd_f=interp2d(lon,lat, ugrd1[0],kind='linear',copy=False,bounds_error=True ) ; 
    
    vgrd1=vgrd[i].data()    
    vgrd_f=interp2d(lon,lat, vgrd1[0],kind='linear',copy=False,bounds_error=True ) ; 
    
    lcdc1=LCDClcl[i].data() ; mcdc1=MCDCmcl[i].data() ; hcdc1=HCDChcl[i].data()
    cldfrn1=((lcdc1[0]+mcdc1[0]+hcdc1[0])*8)/300
    cldfrn_f=interp2d(lon,lat, cldfrn1,kind='linear',copy=False,bounds_error=True ) ; 
    
    rhum1=RH[i].data() ;
    rhum_f=interp2d(lon,lat, rhum1[0],kind='linear',copy=False,bounds_error=True ) ;
    
    dtemp1=DPT[i].data()
    dtemp_f=interp2d(lon,lat, dtemp1[0]-273.15,kind='linear',copy=False,bounds_error=True ) ;  
    
    stemp1=TSOIL[i].data()
    stemp_f=interp2d(lon,lat, stemp1[0]-273.15,kind='linear',copy=False,bounds_error=True ) ;
    
    rain1=APCPsfc[i].data()
    rain_f=interp2d(lon,lat,rain1[0],kind='linear',copy=False,bounds_error=True ) ;
    
    temp=np.concatenate([temp,(np.array([tmp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    uwnd=np.concatenate([uwnd,(np.array([ugrd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)
    vwnd=np.concatenate([vwnd,(np.array([vgrd_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  
    cldfrn=np.concatenate([cldfrn,(np.array([cldfrn_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  
    rhum=np.concatenate([rhum,(np.array([rhum_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  
    dtemp=np.concatenate([dtemp,(np.array([dtemp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  
    stemp=np.concatenate([stemp,(np.array([stemp_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)  
    rain=np.concatenate([rain,(np.array([rain_f(ii[1],ii[0]) for ii in points[:]])).T],axis=0)      

rain[rain<=0.5]=0 # Making rain less than 0.9 to 0
#below two lines will calculate wind direction and speed (km/h)
wdir=np.round(270-(np.arctan2(vwnd,uwnd))*(180/3.14)).astype(int)   ; wdir[wdir>360]=wdir[wdir>360]-360 
wspd=np.round(np.sqrt(np.square(uwnd)+np.square(vwnd))*3.6).astype(int) ;   

#maximum and minium of different variables are calculated in below lines. 
#All arrays are reshaped into 3 dimensional (forecast lead days,time intervel, no: of locations)
temp=np.round(temp.reshape(fcs_leaddays,tint,noloc)).astype(int) ;
maxt=np.vstack((np.round(temp.max(axis=1)).astype(int)).flatten('F')) ;  
mint=np.vstack(np.round(temp.min(axis=1)).astype(int).flatten('F')) ; 

rhum=np.round(rhum.reshape(fcs_leaddays,tint,noloc)).astype(int) ;
maxrh=np.vstack(np.round(rhum.max(axis=1)).astype(int).flatten('F'));  
minrh=np.vstack(np.round(rhum.min(axis=1)).astype(int).flatten('F'))

stemp=np.round(stemp.reshape(fcs_leaddays,tint,noloc)).astype(int) ;  
maxst=np.vstack(np.round(stemp.max(axis=1)).astype(int).flatten('F')) ;  
minst=np.vstack(np.round(stemp.min(axis=1)).astype(int).flatten('F'))

dtemp=np.round(dtemp.reshape(fcs_leaddays,tint,noloc)).astype(int) ;  
meandpt=np.vstack(np.round(dtemp.mean(axis=1)).astype(int).flatten('F')) ;

cldfrn=np.round(cldfrn.reshape(fcs_leaddays,tint,noloc)).astype(int) ; 
meancld=np.vstack(np.round(cldfrn.mean(axis=1)).astype(int).flatten('F')) ; meancld[meancld>8]=8 ; 

rain=np.round(rain.reshape(fcs_leaddays,tint,noloc)).astype(int) ;  
sumrf=np.vstack(np.round(rain.sum(axis=1)).astype(int).flatten('F')) ; 
raincnt=np.vstack((rain[:,:,:]>0.1).sum(axis=1).flatten('F')) 

wdir=wdir.reshape(fcs_leaddays,tint,noloc) ; meandir=np.vstack(np.round(wdir.mean(axis=1)).astype(int).flatten('F')) 
wspd=wspd.reshape(fcs_leaddays,tint,noloc) ; maxws=np.vstack(np.round(wspd.max(axis=1)).astype(int).flatten('F'))

msoil=np.vstack(np.round(np.zeros((fcs_leaddays,noloc))).astype(int).flatten('F')); 
snowc=np.vstack(np.round(np.zeros((fcs_leaddays,noloc))).astype(int).flatten('F')); 

#calculating different conditions ; 
#sky condition, skyno, iconname
skycnd=np.empty((meancld.shape[0],meancld.shape[1])).astype("S") ;
skyno=np.empty((meancld.shape[0],meancld.shape[1])).astype("S") ;
skycnd[meancld<0.5]='SUNNY'                              ; skyno[meancld<0.5]='1'
skycnd[(meancld >=0.5) & (meancld <4.0)]='PARTLY CLOUDY' ; skyno[(meancld >=0.5)  & (meancld <4.0)]='10'
skycnd[(meancld >=4.0) & (meancld <6.9)]='CLOUDY'        ; skyno[(meancld >=4.0) & (meancld <6.9)]='17'
skycnd[(meancld >=6.9)]='OVERCAST'                       ; skyno[(meancld >=6.9)]='18'
iconname=skycnd                                          ; icon=skyno 

#heat index 
tempcnd=np.empty((temp.shape[0],temp.shape[1],temp.shape[2])).astype("S")
tempcnd[temp[:,:,:]<13.0]='COLD'       ;  tempcnd[(temp[:,:,:] >=13) &(temp[:,:,:] <=19)]='COOL'
tempcnd[(temp[:,:,:] >=20) &(temp[:,:,:] <=23)]='PLEASANT' ; 
tempcnd[((temp[:,:,:] >=24) &(temp[:,:,:] <=34)) & (rhum[:,:,:] <=60) ]='WARM'
tempcnd[((temp[:,:,:] >=24) &(temp[:,:,:] <=34)) & (rhum[:,:,:] >60) ]='WARMHUMID' 
tempcnd[((temp[:,:,:] >=35)) & (rhum[:,:,:] <=60) ]='HOT' 
tempcnd[((temp[:,:,:] >=35)) & (rhum[:,:,:] >60) ]='HOTHUMID' 

u, indices = np.unique(tempcnd[:], return_inverse=True) 
tempcndcnt=u[np.argmax(np.apply_along_axis(np.bincount, 1, indices.reshape(tempcnd.shape), None, np.max(indices) + 1), axis=1)]
tempcndcnt=np.vstack(tempcndcnt.flatten('F'))

#wind short and long 
wndshrt=np.empty((meandir.shape[0],meandir.shape[1])).astype("S") ;
wndlong=np.empty((meandir.shape[0],meandir.shape[1])).astype("S")
wndshrt[(meandir >25)  & (meandir <=70)]="NE"   ; wndlong[(meandir >25)  & (meandir <=70)]="North East" 
wndshrt[(meandir >70)  & (meandir <=110)]="E"   ; wndlong[(meandir >70)  & (meandir <=110)]="East" 
wndshrt[(meandir >110) & (meandir <=160)]="SE"  ; wndlong[(meandir >110) & (meandir <=160)]="South East" 
wndshrt[(meandir >160) & (meandir <=200)]="S"   ; wndlong[(meandir >160) & (meandir <=200)]="South" 
wndshrt[(meandir >200) & (meandir <=250)]="SW"  ; wndlong[(meandir >200) & (meandir <=250)]="South West" 
wndshrt[(meandir >250) & (meandir <=290)]="W"   ; wndlong[(meandir >250) & (meandir <=290)]="West" 
wndshrt[(meandir >290) & (meandir <=340)]="NW"  ; wndlong[(meandir >290) & (meandir <=340)]="North West" 
wndshrt[((meandir >340) & (meandir <=360)) |((meandir >0) & (meandir <=25))]="N"  ; 
wndlong[((meandir >340) & (meandir <=360)) |((meandir >0) & (meandir <=25))]="North" 

#Rain percentage and conditions
prain=np.empty((raincnt.shape[0],raincnt.shape[1])).astype("S") ;
crain=np.empty((raincnt.shape[0],raincnt.shape[1])).astype("S") ;
prain[raincnt==0]=0                      ; crain[raincnt==0]='Negligible'
prain[(raincnt >0) & (raincnt<=6)]=30    ; crain[(raincnt >0) & (raincnt<=6)]='Low'
prain[(raincnt >6) & (raincnt<=12)]=60   ; crain[(raincnt >6) & (raincnt<=12)]='Moderate'
prain[(raincnt >12) & (raincnt<=18)]=80  ; crain[(raincnt >12) & (raincnt<=18)]='High'
prain[raincnt >18]=85                    ; crain[raincnt  >18]='High'

#Rain descriptions
precipdesc=np.empty((sumrf.shape[0],sumrf.shape[1])).astype("S") ;
precp=np.empty((sumrf.shape[0],sumrf.shape[1])).astype("S") ;
precipdesc[sumrf <0.01]='0'                      ; precp[sumrf <0.01]='*'
precipdesc[(sumrf >0.01) & (sumrf <=1.0)]='1'    ; precp[(sumrf >0.01) & (sumrf <=1.0)]='DRIZZLE'
precipdesc[(sumrf >1.0) & (sumrf <=2.0)]='5'     ; precp[(sumrf >1.0) & (sumrf <=2.0)]='LIGHT SHOWERS'
precipdesc[(sumrf >2.0) & (sumrf <=3.0)]='6'     ; precp[(sumrf >2.0) & (sumrf <=3.0)]='PASSING SHOWERS'
precipdesc[(sumrf >3.0) & (sumrf <=4.0)]='7'     ; precp[(sumrf >3.0) & (sumrf <=4.0)]='LIGHT RAIN'
precipdesc[(sumrf >4.0) & (sumrf <=5.0)]='8'     ; precp[(sumrf >4.0) & (sumrf <=5.0)]='RAIN SHOWERS'
precipdesc[(sumrf >5.0) & (sumrf <=7.5)]='9'     ; precp[(sumrf >5.0) & (sumrf <=7.5)]='RAIN'
precipdesc[(sumrf >7.5) & (sumrf <=25.0)]='10'   ; precp[(sumrf >7.5) & (sumrf <=25.0)]='NUMEROUS SHOWERS'
precipdesc[(sumrf >25.0) & (sumrf <=35.0)]='11'  ; precp[(sumrf >25.0)  & (sumrf <=35.0)]='SHOWERY'
precipdesc[(sumrf >35.0) & (sumrf <=65.0)]='12'  ; precp[(sumrf >35.0)  & (sumrf <=65.0)]='HEAVY RAIN'
precipdesc[(sumrf >65.0) & (sumrf <=128.0)]='13' ; precp[(sumrf >65.0)  & (sumrf <=128.0)]='LOTS OF RAIN'
precipdesc[(sumrf >128.0) & (sumrf <=265.0)]='14'; precp[(sumrf >128.0)  & (sumrf <=265.0)]='TONS OF RAIN'
precipdesc[sumrf >265.0]='15'                    ; precp[sumrf >265.0]='FLASH FLOODS'

#temperature descriptions
tempdesc=np.empty((maxt.shape[0],maxt.shape[1])).astype("S")
tempd=np.empty((maxt.shape[0],maxt.shape[1])).astype("S")
tempdesc[(maxt <0.0)]='1'                    ; tempd[maxt <0.0]='BRUTALLY COLD'
tempdesc[(maxt >0.0) & (maxt <5.0)]='2'      ; tempd[(maxt >0.0) & (maxt <5.0)]='FRIGID'
tempdesc[(maxt >5.0) & (maxt <=9.0)]='3'     ; tempd[(maxt >5.0) & (maxt <=9.0)]='COLD'
tempdesc[(maxt >=10.0) & (maxt <=14.0)]='4'  ; tempd[(maxt >=10.0) & (maxt <=14.0)]='CHILLY'
tempdesc[(maxt >=15.0) & (maxt <=19.0)]='5'  ; tempd[(maxt >=15.0) & (maxt <=19.0)]='NIPPY'
tempdesc[(maxt >=20.0) & (maxt <=23.0)]='6'  ; tempd[(maxt >=20.0) & (maxt <=23.0)]='COOL'
tempdesc[(maxt >=24.0) & (maxt <=25.0)]='7'  ; tempd[(maxt >=24.0) & (maxt <=25.0)]='REFRESHINGLY COOL'
tempdesc[(maxt >=26.0) & (maxt <=27.0)]='8'  ; tempd[(maxt >=26.0) & (maxt <=27.0)]='MILD'
tempdesc[(maxt >=28.0) & (maxt <=30.0)]='9'  ; tempd[(maxt >=28.0) & (maxt <=30.0)]='PLEASENTLY WARM'
tempdesc[(maxt >=31.0) & (maxt <=34.0)]='10' ; tempd[(maxt >=31.0) & (maxt <=34.0)]='WARM'
tempdesc[(maxt >=35.0) & (maxt <=45.0)]='11' ; tempd[(maxt >=35.0) & (maxt <=45.0)]='HOT'
tempdesc[(maxt >45.0)]='12'                  ; tempd[maxt >45.0]='EXREMELY HOT'

#frost parameter not required, so filled with empty arrays
frost=np.empty((mint.shape[0],mint.shape[1])).astype("S") ; frost[:]='No'
#heat index and skycond added together.
descrip1=np.core.defchararray.add(skycnd,' ') ; descrip=np.core.defchararray.add(descrip1,tempd)
#file header defined
header="TEHSILID,T_DATE,F_DATE,TEMPMAX,TEMPMIN,RHMAX,RHMIN,WINDDIR,WINDSPD,RAIN,CLOUD,DEWPOINT,MAXSOILTEMP,MINSOILTEMP,MAXSOILMOIS,MINSOILMOIS,RAINP,PRECPDESC,PRECP,RAINCHANCE,SKY,SKYCOND,TEMPDESC,TEMPERATURE,WINDSHRT,WINDLONG,FROST,ICON,ICONNAME,DAYSEQUENCE,DESCRIP,HEATINDEX,SNOW"
header=np.vstack(np.array(header.split(","))).T
#data aranged in required format and saved as a csv file
fin_mat1=np.concatenate([pre_mat,maxt,mint,maxrh,minrh,meandir,maxws,sumrf,meancld,meandpt,maxst,minst,msoil,msoil, \
       prain,precipdesc,precp,crain,skyno,skycnd,tempdesc,tempd,wndshrt,wndlong,frost,icon,iconname,day_seq,descrip,tempcndcnt,snowc],axis=1)
fin_mat=np.concatenate([header,fin_mat1],axis=0)

np.savetxt(outFile,fin_mat,fmt="%s",delimiter=',')

print("--- %s seconds ---" % (time.time() - start_time)) 
quit()
