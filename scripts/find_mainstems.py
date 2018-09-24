#!/usr/bin/env python
'''
 Given a pfafstetter code as an outlet, subset a catchment of flowline shapefile.
 Add field "tributary"
'''

import fiona
import pfafstetter as pfaf

inshp = '../test_data/Flowline_CO_14_cameo.shp'
outshp = '../test_data/Flowline_CO_14_cameo_mainstem.shp'

# Pfafstetter code
pfaf_out = '9685333'

#open shp
shp = fiona.open(inshp,'r')

# print out shapefile attributes
shp.schema['properties']['mstem_level'] = 'int'
shp.schema['properties']['mstem_code'] = 'str:30'
print(shp.schema)

meta = shp.meta
with fiona.open(outshp, 'w', **meta) as output:

  for feature in shp:

    pfaf_a = feature['properties']['PFAF_CODE']

    if pfaf_a == '-9999' or pfaf_a == '0':
      continue

    code = pfaf.get_mainstems(pfaf_a)

    feature['properties']['mstem_level'] = len(code)
    feature['properties']['mstem_code'] = code

    output.write(feature)

