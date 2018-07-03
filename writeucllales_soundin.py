import numpy as np ; import pandas as pd ; import metpy.calc as mpcalc ; from metpy.units import units 


data=pd.read_csv('~/Data/masdar_station_data/wyoming/metar+rs/201712/AbuDhabi_upperair_2017122112.csv')
data=data.apply(pd.to_numeric,errors='coerce')  
#pd.set_option('display.float_format', '{:.2E}'.format) 
#new_data=pd.concat([data['PRES'][1::][::-1],data['TEMP'][1::][::-1]+273.15,data['MIXR'][1::][::-1]/1000,data['MIXR'][1::][::-1]*0,(data['MIXR'][1::][::-1]*0).astype(int) ],axis=1 )
#new_data.to_csv('/home/vkvalappil/Data/modelWRF/LES/UCLALES-SALSA/bin/datafiles/dsrt.lay',sep=',',index=False,float_format='%.3E')  

wind_speed = (data['SKNT'] *0.514).values * units('m/s')
wind_dir = data['DRCT'].values * units.deg 

#data['u_wind'], data['v_wind'] = mpcalc.get_wind_components(data['SKNT'][1::]*0.51,np.deg2rad(data['DRCT'][1::]))
data['u_wind'], data['v_wind']  = mpcalc.get_wind_components(wind_speed,wind_dir)

#u, v = mpcalc.get_wind_components(data['SKNT'][1::], data['DRCT'][1::])
                                                       
new_data=pd.concat([data['HGHT'][1::],data['TEMP'][1::]+273.15,data['MIXR'][1::],data['u_wind'][1::],data['v_wind'][1::] ],axis=1 )
new_data.to_csv('/home/vkvalappil/Data/modelWRF/LES/UCLALES-SALSA/bin/sound_in_2017122112',sep=',',index=False) ; #float_format='%.3E'  

