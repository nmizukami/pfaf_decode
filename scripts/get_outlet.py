#!/usr/bin/env python
'''
Get outlet pfafstetter code given a river network
'''

import geopandas as gpd
import pfafstetter as pfaf

inshp = '../test_data/Flowline_CO_14.shp'

#open shp
shp = gpd.read_file(inshp)

# list of pfaf_code
pfafs = shp['PFAF_CODE'].tolist()

pfaf_outlet = pfaf.get_outlet(pfafs)

print(pfaf_outlet)
