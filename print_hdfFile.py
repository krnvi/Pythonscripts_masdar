#!/usr/bin/python 

import pyhdf as hdf ; from pyhdf.SD import SD 
modFile='/home/Data/workspace/AIRS.2016.09.24.001.L2.RetStd.v6.0.31.0.G16268163917.hdf'

hdf_f=hdf.SD.SD(modFile,hdf.SD.SDC.READ)
print hdf_f.datasets()
#print hdf_f.attributes()

quit()
