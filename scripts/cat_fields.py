#!/usr/bin/env python

import sys
import argparse
import geopandas as gpd
import pandas as pd

FIELD_TYPE = 'str'

def process_command_line():
    '''Parse the commandline'''
    parser = argparse.ArgumentParser(description='Script to append fields in ascii to shapefile attribute')
    parser.add_argument('inshp',
                        help='input shapefile')
    parser.add_argument('inasc',
                        help='input ascii attributes')
    parser.add_argument('ascfield',
                        help='common field name in ascii')
    parser.add_argument('shpfield',
                        help='common field name in shapefile')
    parser.add_argument('outshp',
                        help='output shapefile')

    args = parser.parse_args()

    return(args)


# main
if __name__ == '__main__':

  # process command line
  args = process_command_line()

  #read shp
  shp = gpd.read_file(args.inshp)
  shp[args.shpfield] = shp[args.shpfield].astype(FIELD_TYPE)
  print(shp)

  # read csv
  df = pd.read_csv(args.inasc,
                   header=0,
                   delim_whitespace=True)

  df.rename(columns={args.ascfield:args.shpfield},
            inplace=True)
  print(df)

  df[args.shpfield] = df[args.shpfield].astype(FIELD_TYPE)

  print(df)

  # append csv attributes to shp
  new = pd.merge(shp, df, on=args.shpfield, how='left', validate="one_to_one")
  print(new)

  # write new shapefile with new attributes
  new.to_file(args.outshp, driver='ESRI Shapefile')
