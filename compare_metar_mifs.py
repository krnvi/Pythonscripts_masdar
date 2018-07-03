
import pandas as pd ;  import pytz ; import numpy as np 
import matplotlib.pyplot as plt; from pylab import savefig ;   
met_file='/home/vkvalappil/Data/masdar_station_data/wyoming/201803/metar.csv'

fs_file='/home/vkvalappil/Data/masdar_station_data/metStation/mifs_201803.csv'

mifs_data=pd.read_csv(fs_file)
mifs_data['TimeStamp']=mifs_data['TimeStamp'].apply(pd.to_datetime, errors='ignore') ; 

mifs_data.iloc[:,1:]=mifs_data.iloc[:,1:].apply(pd.to_numeric,errors='coerce')
mifs_data.index=pd.to_datetime(mifs_data.TimeStamp) ;          

mifs_data.index =mifs_data.index.tz_localize(pytz.timezone('Asia/Dubai'))    
mifs_data['TimeStamp']=mifs_data.index
mifs_data_hour=mifs_data.iloc[:,:].resample('1H').mean()  ; mifs_data_hour.insert(0,'TimeStamp', mifs_data_hour.index) ; 


met_data=pd.read_csv(met_file)
met_data['TIME']=met_data['TIME'].apply(pd.to_datetime,format='%d/%H%M',errors='ignore') ; x = pd.Timedelta(days=43158)
met_data.TIME+= x 
met_data[['ALTM','TMP','DEW','RH','DIR','SPD','VIS']]=met_data[['ALTM','TMP','DEW','RH','DIR','SPD','VIS']].apply(pd.to_numeric,errors='coerce') 
#met_data=met_data.drop(0) ;# met_data=met_data.drop(columns=9)
met_data.index=pd.to_datetime(met_data.TIME)
met_data.index=(met_data.index.tz_localize(pytz.utc)).tz_convert(pytz.timezone('Asia/Dubai'))    
met_data['TIME']=met_data.index


idx = pd.date_range('2018-03-10 04:00:00+04:00', '2018-03-20 03:00:00+04:00',freq='H') #Missing data filled with Nan
mifs_data_2=mifs_data_hour.reindex(idx, fill_value=np.nan)


tdep_mifs=mifs_data_2['Temperature@10m'] - mifs_data_2['Dew_Point_Temperature@10m']
tdep_met=met_data['TMP'] - met_data['DEW']

fig, ax1= plt.subplots(1, sharex=False, sharey=False,figsize=(12,12),dpi=50)

ax1 = met_data['DEW'].plot.line(ax=ax1,marker='o',grid=True, legend=True, style=None,linewidth=3,color='r',label='Metar')              

#ax1 = mifs_data_2['Dew_Point_Temperature@2m'].plot.line(ax=ax1,marker='o', grid=True, legend=True, style=None,linewidth=3,color='b',label='Mifs: Weather Station 2m')              
ax1 = mifs_data_2['Dew_Point_Temperature@10m'].plot.line(ax=ax1,marker='o', grid=True, legend=True, style=None,linewidth=3,color='g',label='Mifs: Weather Station')              
                                      
leg1=ax1.legend(loc='upper center',fontsize=14)
plt.tight_layout(h_pad=3) ; 
plt.legend(loc=1,fontsize=14)
plt.title('Dew Point',fontsize=16)         
outFile='/home/vkvalappil/Data/masdar_station_data/metStation/mifs_metar_dewtemp_10_19.png'
savefig(outFile);
plt.close(fig) ; fig.clf(fig)


fig, ax1= plt.subplots(1, sharex=False, sharey=False,figsize=(12,12),dpi=50)

ax1 = met_data['TMP'].plot.line(ax=ax1,marker='o',grid=True, legend=True, style=None,linewidth=3,color='r',label='Metar')              

#ax1 = mifs_data_2['Temperature@2m'].plot.line(ax=ax1,marker='o', grid=True, legend=True, style=None,linewidth=3,color='b',label='Mifs: Weather Station 2m')              
ax1 = mifs_data_2['Temperature@10m'].plot.line(ax=ax1,marker='o', grid=True, legend=True, style=None,linewidth=3,color='g',label='Mifs: Weather Station')              
                                      
leg1=ax1.legend(loc='upper center',fontsize=14)
plt.tight_layout(h_pad=3) ; 
plt.legend(loc=1,fontsize=14)
plt.title('Temperature',fontsize=16)
outFile='/home/vkvalappil/Data/masdar_station_data/metStation/mifs_metar_temp_10_19.png'
savefig(outFile);
plt.close(fig) ; fig.clf(fig)
#######################################
fig, ax1= plt.subplots(1, sharex=False, sharey=False,figsize=(12,12),dpi=50)

ax1 = tdep_met.plot.line(ax=ax1,marker='o',grid=True, legend=True, style=None,linewidth=3,color='r',label='Metar')              

#ax1 = mifs_data_2['Temperature@2m'].plot.line(ax=ax1,marker='o', grid=True, legend=True, style=None,linewidth=3,color='b',label='Mifs: Weather Station 2m')              
ax1 = tdep_mifs.plot.line(ax=ax1,marker='o', grid=True, legend=True, style=None,linewidth=3,color='g',label='Mifs: Weather Station')              


#ax1.set_yticks(np.arange(0,tdep_mifs.shape[0],1)) ; 
#yTickMarks=np.arange(0,tdep_met.max()+2,1)
#ytickNames = ax1.set_yticklabels(yTickMarks,fontsize=18)
#                                    
leg1=ax1.legend(loc='upper center',fontsize=14)
plt.tight_layout(pad=4) ; 
plt.legend(loc=1,fontsize=14)
plt.title('Tdep',fontsize=16)
outFile='/home/vkvalappil/Data/masdar_station_data/metStation/mifs_metar_tdep_10_19.png'
savefig(outFile);
plt.close(fig) ; fig.clf(fig)



















