#!/usr/bin/env python
'''
Append fields in ascii to shapefile attribute
ascii should include common field to shapefile attribute
'''

import sys
import fiona
import geopandas as gpd
import pandas as pd

#Mississippi
#inshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_MS_10U.shp'
#outshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_MS_10U_mainstem.shp'
#asc = 'ms100_1'

#Cameo
inshp = '../test_data/Flowline_CO_14_cameo.shp'
outshp = '../test_data/Flowline_CO_14_cameo_trib500_2.shp'
asc = 'cameo500_2'

common_field = 'ComID'
field_in_ascii = ['level','numseg']   # ['level','dangle']


field_in_ascii.insert(0,common_field)
df = pd.read_csv(asc,
                 delim_whitespace=True,
                 names=field_in_ascii)
print(df)

#open shp
shp = gpd.read_file(inshp)
print shp

new = pd.merge(shp, df, on=common_field, how='left', validate="one_to_one")
print new

new.to_file(outshp, driver='ESRI Shapefile')
