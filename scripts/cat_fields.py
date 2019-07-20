#!/usr/bin/env python
'''
Append fields in ascii to shapefile attribute
ascii should include common field to shapefile attribute
'''

import geopandas as gpd
import pandas as pd

#Mississippi
#inshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_MS_10U.shp'
#outshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_MS_10U_mainstem.shp'
#asc = 'ms100_1'

#Cameo
#inshp = '../test_data/Flowline_CO_14_cameo.shp'
#outshp = '../test_data/Flowline_CO_14_cameo_trib500_2.shp'
#asc = 'cameo500_2'

#upper colorado
#inshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_CO_14_LeesFerry.shp'
#outshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_CO_14_LeesFerry_parallel_fortran1.shp'
#asc = 'seginfo1'

inshp = '../test_data/nhdPlus_SHPs_class250/Flowline_CO_14.shp'
outshp = '../test_data/nhdPlus_SHPs_class250/Flowline_CO_14_ntopo.shp'
asc = 'streamOrder'

# attributes in csv
common_field = 'ComID'
#field_in_ascii =  ['level','trib_id','numseg']   # ['level','dangle']
#field_in_ascii = ['pfaf_code','pfaf_common','numseg','core'] # ['level','trib_id','numseg']   # ['level','dangle']
field_in_ascii = ['streamOrder'] # ['level','trib_id','numseg']   # ['level','dangle']
field_in_ascii.insert(0,common_field)

# read csv
df = pd.read_csv(asc,
                 skiprows=1,
                 delim_whitespace=True,
                 names=field_in_ascii)
print(df)

#read shp
shp = gpd.read_file(inshp)
print shp

# append csv attributes to shp
new = pd.merge(shp, df, on=common_field, how='left', validate="one_to_one")
print new

# write new shapefile with new attributes
new.to_file(outshp, driver='ESRI Shapefile')
