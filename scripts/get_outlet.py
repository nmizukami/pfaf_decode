#!/usr/bin/env python
'''
Get outlet pfafstetter code given a river network
'''
import pandas as pd
import geopandas as gpd
import pfafstetter as pfaf

inshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_MS_08.shp'

fieldname = 'PFAF'

_output = True

#open shp
shp = gpd.read_file(inshp)

# list of pfaf_code
pfafs = shp[fieldname].tolist()

pfaf_outlet = pfaf.get_outlet(pfafs)

print(pfaf_outlet)

if _output:
  df = pd.DataFrame(pfaf_outlet, columns=["pfaf_outlet"])
  df.to_csv('pfaf_outlet.csv', index=False)
