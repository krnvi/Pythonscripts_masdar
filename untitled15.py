

import gdal

ds1=gdal.Open('/home/oceanColor/Fog/maps_codes/maps/mask_geo/mask_20180304_2230.tiff')
band1 = ds1.GetRasterBand(1)
arr1 = band1.ReadAsArray()
[cols1, rows1] = arr1.shape


ds = gdal.Open(fileName)
band = ds.GetRasterBand(1)
arr = band.ReadAsArray()
[cols, rows] = arr.shape



