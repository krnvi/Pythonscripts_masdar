#!/usr/bin/python

import os ; import sys ; import numpy as np ; 

########################################################################################################################
main='/home/vkvalappil/Data/' ; output=main+'metarData/' ; scripts=main+'/workspace/pythonScripts/'

date=str(sys.argv[1]) ; 


lstFile=scripts+'metar_surf.csv' ; points=np.genfromtxt(lstFile,delimiter=',',dtype='S')

for code, loc in points:
    
    fil = '%s%s/%s/%s/%s_%s.csv' % (output,'_data',date[0:4],date[0:6],loc, date) ;     print fil 

    data=np.genfromtxt(fil,delimiter=',',dtype='S') 
    
    indx=np.where(data[:,4]=='M')[0]   ; data[indx,4]=data[indx-1,4] 

    indx=np.where(data[:,5]=='M')[0]   ; data[indx,5]=data[indx-1,5] 

    indx=np.where(data[:,6]=='M')[0]   ; data[indx,6]=data[indx-1,6] 

    indx=np.where(data[:,11]=='M')[0]   ; data[indx,11]=data[indx-1,11] 

    e_0=0.611 ; b=17.2694 ; t_1=273.16 ; t_2=35.86 ; eps=0.622
    
    es=(e_0*np.exp(b*((data[1:,4].astype(float)+273.16-t_1)/(data[1:,4].astype(float)+273.16-t_2)))) 
    e= (es*data[1:,6].astype(float))/100 ;
    mr=(eps*e)/((data[1:,11].astype(float)/10)-e) ; 
    mr_1=np.empty(data.shape[0]).astype(str)  ; mr_1[0]='MixRatio(g/g)' ; mr_1[1:]=mr.astype(str)
    
    data_1=np.concatenate([data[:,0:11],np.vstack(mr_1),data[:,12:]],axis=1)
    
    if not os.path.exists(output+'_data_mr/'+date[0:6]) :
        os.mkdir(output+'_data_mr/'+date[0:6])
    
    file1 = '%s%s%s/%s_%s.csv' % (output,'_data_mr/',date[0:6],loc, date)
    np.savetxt(file1,data_1,delimiter=',',fmt='%s')

quit()

