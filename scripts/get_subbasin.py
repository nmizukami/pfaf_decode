#!/usr/bin/env python
'''
 Given a pfafstetter code as an outlet, subset a catchment of flowline shapefile.
'''

import fiona
import pfafstetter as pfaf


check_closed = True    # check closed basin

#inshp = '../test_data/Flowline_CO_14_cameo.shp'
#outshp = '../test_data/Flowline_CO_14_eagle.shp'
inshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_CO_14.shp'
outshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_CO_14_LeesFerry.shp'

# Pfafstetter code
#pfaf_b = '9688111'    #9688111: Eagle river outlet into Colorado River
pfaf_b = '96531'    #9688111: Eagle river outlet into Colorado River

fieldname = 'PFAF_CODE'

#open shp
shp = fiona.open(inshp)

# print out shapefile attributes
print(shp.schema)

meta = shp.meta
with fiona.open(outshp, 'w', **meta) as output:

  for feature in shp:
    pfaf_a = feature['properties'][fieldname]

    if pfaf_a == '-9999' or pfaf_a == 0:
      continue

    check = pfaf.check_upstream(pfaf_a, pfaf_b)

    if check:

      isClose = False
      if check_closed:
        for dd in range(len(pfaf_b)-1, len(pfaf_a)):
          if (pfaf_a[dd] == '0'):
            isClosed = True
            break

      if not isClosed:
        print('write seg-%s' % (pfaf_a))
        output.write(feature)

