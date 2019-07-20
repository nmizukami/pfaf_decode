#!/usr/bin/env python
'''
subset shapefile based on selected attributes values in csv
'''
import sys
import pandas as pd
import geopandas as gpd

#inshp = '../test_data/HDMA/eu_streams_1.shp'
#outshp = '../test_data/HDMA/eu_streams_outlet.shp'
#asc = 'pfaf_outlet.csv'

inshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_CO_14_LeesFerry.shp'
outshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_CO_14_LeesFerry_parallel_node5.shp'
asc = 'node5'
field1 ='reach_ID'
field2 ='ComID'

#read  csv
df = pd.read_csv(asc)
print df[field1].astype('int64').values.tolist()

#read shp
shp = gpd.read_file(inshp)

# subset shapefile
#shp1 = shp[shp.PFAF.astype('int64').isin(df[field1].values)]
shp1 = shp[shp[field2].astype('int64').isin(df[field1].values)]
print(shp1)
# write subset shapefile
shp1.to_file(outshp)
