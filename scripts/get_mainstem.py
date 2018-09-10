#!/usr/bin/env python
'''
 Given a pfafstetter code as an outlet, subset a catchment of flowline shapefile.
'''

import fiona
import pfafstetter as pfaf

inshp = '../Flowline_CO_14_cameo.shp'
outshp = '../Flowline_CO_14_cameo_mainstem.shp'

# Pfafstetter code
pfaf_out = '9685333'
ndigit = len(pfaf_out)

#open shp
shp = fiona.open(inshp)

# print out shapefile attributes
print(shp.schema)

meta = shp.meta
with fiona.open(outshp, 'w', **meta) as output:

  for feature in shp:
    pfaf_a = feature['properties']['PFAF_CODE']

    if pfaf_a == '-9999':
      continue

    check = pfaf.check_mainstem(pfaf_a, pfaf_out)

    if check:
      print('write seg-%s' % (pfaf_a))
      output.write(feature)

