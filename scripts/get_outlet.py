#!/usr/bin/env python

import sys
import argparse
import pandas as pd
import geopandas as gpd
import pfaf.pfafstetter as pfaf

fieldname = 'PFAF'

_output = True

def process_command_line():
    '''Parse the commandline'''
    parser = argparse.ArgumentParser(description='Script to list outlet segment pfaf code')
    parser.add_argument('inshp',
                        help='input shapefile')
    parser.add_argument('fieldname',
                        help='pfaf field name')
    parser.add_argument('outasc',
                        help='ascii output')
#    # Optional arguments
#    parser.add_argument('--outasc', action='store_true', default=False,
#                        help='ascii output' )

    args = parser.parse_args()

    return(args)


# main
if __name__ == '__main__':

  # process command line
  args = process_command_line()

  #open shp
  shp = gpd.read_file(args.inshp)

  # list of pfaf_code
  pfafs = shp[args.fieldname].tolist()

  # Get outlelt list
  pfaf_outlet = pfaf.get_outlet(pfafs)

  print(pfaf_outlet)

  if _output:
    df = pd.DataFrame(pfaf_outlet, columns=["pfaf_outlet"])
    df.to_csv(args.outasc, index=False)

