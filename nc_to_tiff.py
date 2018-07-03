

from osgeo import gdal, osr, gdal_array

import xarray as xr ; import numpy as np ;


sub_data='NETCDF:"' +'/home/oceanColor/Fog/WRFmodel_forecast/wrfouput_weatherforcast/Archivewrffogmaskwithbackground/wrfpost_2017060500.nc'+'":'+'fog_mask'
nc_file=gdal.Open(sub_data)

NDV=nc_file.GetRasterBand(1).GetNoDataValue()
xsize=nc_file.RasterXSize ; ysize=nc_file.RasterYSize
geoT=nc_file.GetGeoTransform()
projection=osr.SpatialReference() ; projection.ImportFromEPSG(3857)  #ImportFromWkt(nc_file.GetProjectionRef()) ;
nc_file=None ; 

xr_ensemble=xr.open_dataset('/home/oceanColor/Fog/WRFmodel_forecast/wrfouput_weatherforcast/Archivewrffogmaskwithbackground/wrfpost_2017060500.nc') 
data=xr_ensemble['fog_mask']
data=np.ma.masked_array(data,mask=data==NDV,fill_value=NDV)

data_type=gdal_array.NumericTypeCodeToGDALTypeCode(data.dtype)

if type(data_type)==np.int:
    if data_type.startswith('gdal_GDT_')=='FALSE' :
        data_type=eval('gdal.GDT_'+data_type)
        
tif_file='/home/vkvalappil/Data/wrf_fog_mask.tiff'        
zsize=data.shape[0]
driver=gdal.GetDriverByName('GTiff') ; data[np.isnan(data)]=NDV
Dataset=driver.Create(tif_file,xsize,ysize,zsize,data_type)
Dataset.SetGeoTransform(geoT) ; 
Dataset.setProjection(projection.ExportToWkt())
for i in xrange(0,zsize):
    Dataset.GetRasterBand(i+1).WriteArray(data[i])
    Dataset.GetRasterBand(i+1).SetNoDataValue(NDV)
Dataset.FlushCache()   