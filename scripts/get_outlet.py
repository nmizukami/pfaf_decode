#!/usr/bin/env python
'''
Get outlet pfafstetter code given a river network
'''

import fiona
import pfafstetter as pfaf

inshp = '../test_data/Flowline_CO_14_cameo.shp'

# Pfafstetter code
_pfaf = '9685333'

#open shp
shp = fiona.open(inshp)

# print out shapefile attributes
print(shp.schema)

pfaf_outlet = '';

for idx, feature in enumerate(shp):

  pfaf1 = feature['properties']['PFAF_CODE']

  if pfaf1 == '-9999':
    continue

  if not pfaf_outlet:
    pfaf_outlet = pfaf1
    continue
  else:
    if pfaf.check_upstream(pfaf_outlet,pfaf1):
      pfaf_outlet = pfaf1

print(_pfaf)
print(pfaf_outlet)


