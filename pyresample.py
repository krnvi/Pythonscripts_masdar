# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 13:26:55 2017

@author: vkvalappil
"""

import pyresample as pr
from pyresample import kd_tree, geometry
from pyresample import utils

swath_def = geometry.SwathDefinition(lons=lon1, lats=lat1)
area_def = utils.parse_area_file('/home/vkvalappil/Data/modelWRF/input/region_config.cfg', 'scan2')[0]
result = kd_tree.resample_nearest(swath_def, brt,area_def, radius_of_influence=12000, epsilon=100, fill_value=None)
pr.plot.save_quicklook('/home/vkvalappil/Data/modelWRF/input/iasi_ctp_quick.png',area_def, result, label='AMSUA Brightness Temp', coast_res = 'h')
                   
                   
                   
area_id = 'uae'                   
description = 'uae wrf domain'                  
proj_id = 'uae'
x_size = 425
y_size = 425
area_extent = (186073.68,2214294.03,210590.35,3322575.90)
proj_dict = {'a': '6371228.0', 'units': 'm', 'lon_0': '0','proj': 'laea', 'lat_0': '-90'}
area_def = geometry.AreaDefinition(area_id, description, proj_id,proj_dict, x_size, y_size, area_extent)




swath_def =geometry.SwathDefinition(lon1, lat1)


result = pr.kd_tree.resample_nearest(swath_def, brt1, area_def,radius_of_influence=20000, fill_value=None)


pr.plot.save_quicklook('/home/vkvalappil/Data/modelWRF/input/tb_amsua.png', area_def, result, label='Tb 37v (K)')