#!/usr/bin/env python
'''

'''

import geopandas as gpd
import pfafstetter as pfaf

inshp = '../test_data/Flowline_CO_14_cameo_tributary.shp'

threshold = 100

#open shp
shp = gpd.read_file(inshp)

# get unique tributary ID
tributaries = set(shp['tributary'])

# Number of tributaries
num_trib = len(tributaries)

print('Number of tributaries flowing to the mainstem: %d '%num_trib)

counter = 0

group = {}

for tr in tributaries:

  print('tributary: %s'%tr)
  shp_sub = shp.loc[shp['tributary']==tr]

  if len(shp_sub)< threshold:
    continue

  pfaf_outlet = ''

  for idx, feature in shp_sub.iterrows():

    pfaf1 = feature['PFAF_CODE']

    if not pfaf_outlet:
      pfaf_outlet = pfaf1
      continue
    else:
      if pfaf.check_upstream(pfaf_outlet,pfaf1):
        pfaf_outlet = pfaf1

  group[counter] = tr

  counter += 1

print(group)
