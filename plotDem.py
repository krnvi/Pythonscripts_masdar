#!usr/bin/python

from osgeo import gdal
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

#filename = "/home/vkvalappil/OldData/WRFDomainWizard/asterdem/aster_dem/ASTGTM2_N21E049_dem.tif"
filename ="/home/vkvalappil/OldData/WRFDomainWizard/srtm_dem/old/uae-90m-DEM_N21E050.tif"
gdal_data = gdal.Open(filename)
gdal_band = gdal_data.GetRasterBand(1)
nodataval = gdal_band.GetNoDataValue()

# convert to a numpy array
data_array = gdal_data.ReadAsArray().astype(np.float)

# replace missing values if necessary
if np.any(data_array == nodataval):
    data_array[data_array == nodataval] = np.nan


#Plot out data with Matplotlib's 'contour'
fig = plt.figure(figsize = (12, 8))
ax = fig.add_subplot(111)
plt.contourf(data_array, cmap = "viridis") #,levels = list(range(0, 5000, 100)))
plt.title("Elevation")
cbar = plt.colorbar()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()


xoff, a, b, yoff, d, e = gdal_data.GetGeoTransform()

def pixel2coord(x, y):
 """Returns global coordinates from pixel x, y coords"""
 xp = a * x + b * y + xoff
 yp = d * x + e * y + yoff
 return(xp, yp)

# get columns and rows of your image from gdalinfo
rows = 3600+1
colms = 3400+1

if __name__ == "__main__":
 for row in  range(0,rows):
  for col in  range(0,colms): 
   print pixel2coord(col,row)