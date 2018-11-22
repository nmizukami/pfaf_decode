#!/usr/bin/env python
'''
Append fields in ascii to shapefile attribute
'''
import sys
import pandas as pd
import geopandas as gpd

inshp = '../test_data/HDMA/eu_streams_1.shp'
outshp = '../test_data/HDMA/eu_streams_outlet.shp'

df = pd.read_csv('pfaf_outlet.csv')
print df['pfaf_outlet'].astype('int64').values.tolist()

#open shp
shp = gpd.read_file(inshp)

shp1 = shp[shp.PFAF.astype('int64').isin(df['pfaf_outlet'].values)]
print shp1
shp1.to_file(outshp)
