#!usr/bin/python

import numpy as np ; import os ; import sys ; from metar import Metar ; import pandas as pd ; 


path='/home/vkvalappil/Data/metarData/'
date=str(sys.argv[1]) ; 

lstFile='/home/vkvalappil/Data/workspace/pythonScripts/metar_surf.csv'
points=np.genfromtxt(lstFile,delimiter=',',dtype='S')

for code, loc in points:

    fil = '%s%s/%s/%s_%s.csv' % (path,date[0:4],date[0:6],loc, date)

    print fil 

    #data=np.genfromtxt(fil,delimiter=',',dtype='S') 
    data=pd.read_csv(fil)
    data.tmpf=data.tmpf.apply(pd.to_numeric,errors='coerce')
    data.tmpf=(data.tmpf-32)/1.8 #(5.0/9.0)
    data[' dwpf']=data[' dwpf'].apply(pd.to_numeric,errors='coerce')  
    data[' dwpf']=(data[' dwpf']-32)/1.8 #(5.0/9.0)
#met.station_id met.time met.temp.value() met.dewpt.value(),met.vis.value(),met.wind(), met.present_weather()

#    for ii in range(1,data.shape[0]):
#    
#        met=Metar.Metar(data[ii,-1]) ; 
#        if met.press:
#             data[ii,11]=met.press.value(units='MB') ; 
#        if met.temp:
#            data[ii,4]=met.temp.value(units='C')   ;
#        #else:
#        #    data[ii,4]=(data[ii,4].astype(float)-32)/1.8
#        if met.dewpt:
#            data[ii,5]=met.dewpt.value(units='C')   ;
#        #else:
#        #    data[ii,5]=(data[ii,5].astype(float)-32)/1.8    
            
       
    if not os.path.exists(path+'_data/'+date[0:4]+'/'+date[0:6]) :
        os.makedirs(path+'_data/'+date[0:4]+'/'+date[0:6])
    
    file1 = '%s%s%s/%s/%s_%s.csv' % (path,'_data/',date[0:4],date[0:6],loc, date)
    data.to_csv(file1)
    #np.savetxt(file1,data,delimiter=',',fmt='%s')

quit()

