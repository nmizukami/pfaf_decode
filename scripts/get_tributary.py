#!/usr/bin/env python
'''
 Given a pfafstetter code as an outlet, subset a catchment of flowline shapefile.
'''

import fiona
import pfafstetter as pfaf
import sys

inshp = '../test_data/Flowline_CO_14_cameo.shp'
outshp = '../test_data/Flowline_CO_14_cameo_tributary.shp'

# Pfafstetter code
pfaf_out = '9685333'
ndigit = len(pfaf_out)

#open shp
shp = fiona.open(inshp,'r')

# print out shapefile attributes
shp.schema['properties']['tributary'] = 'str:30'
print(shp.schema)

meta = shp.meta
with fiona.open(outshp, 'w', **meta) as output:

  for feature in shp:
    pfaf_a = feature['properties']['PFAF_CODE']

    if pfaf_a == '-9999':
      continue

    tributary = pfaf.get_tributary(pfaf_a, pfaf_out)

    print('seg-%s, tributary-%s' % (pfaf_a, tributary))

    feature['properties']['tributary'] = tributary
    output.write(feature)

