#!/usr/bin/env python

import sys
import argparse
import fiona
import pfaf.pfafstetter as pfaf

include_closed = True    # check closed basin

def process_command_line():
    '''Parse the commandline'''
    parser = argparse.ArgumentParser(description='Script to subset a catchment based on outlet pfaf')
    parser.add_argument('inshp',
                        help='input shapefile')
    parser.add_argument('outshp',
                        help='output shapefile')
    parser.add_argument('fieldname',
                        help='pfaf field name')
    parser.add_argument('outpfaf',
                        help='pfaf code for outlet seg')

    args = parser.parse_args()

    return(args)

# main
if __name__ == '__main__':

  # process command line
  args = process_command_line()

  shp = fiona.open(args.inshp)

  meta = shp.meta

  print(meta)

  with fiona.open(args.outshp, 'w', **meta) as output:

    for feature in shp:
      pfaf_a = feature['properties'][args.fieldname]

      if pfaf_a == '-9999' or pfaf_a == 0 or pfaf_a is None:
        continue

      if pfaf_a == args.outpfaf:
        check = True
      else:
        check = pfaf.check_upstream(pfaf_a, args.outpfaf, includeClose=include_closed)

      if check:

        print('write seg-%s' % (pfaf_a))
        output.write(feature)
