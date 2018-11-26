#!/usr/bin/env python
'''
subset shapefile based on selected attributes values in csv
'''
import pandas as pd
import geopandas as gpd

inshp = '../test_data/HDMA/eu_streams_1.shp'
outshp = '../test_data/HDMA/eu_streams_outlet.shp'

#read  csv
df = pd.read_csv('pfaf_outlet.csv')
print df['pfaf_outlet'].astype('int64').values.tolist()

#read shp
shp = gpd.read_file(inshp)

# subset shapefile
shp1 = shp[shp.PFAF.astype('int64').isin(df['pfaf_outlet'].values)]
print shp1
# write subset shapefile
shp1.to_file(outshp)
