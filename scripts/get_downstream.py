#!/usr/bin/env python
'''
 Given a pfafstetter code as an outlet, decompose a catchment or flowline shapefile.
'''
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
import xarray as xr
import pfafstetter as pfaf

#input
#inshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_CO_14.shp' # to get seg-id, pfaf
inshp = '../test_data/Flowline_CO_14_cameo.shp' # to get seg-id, pfaf
#output
outasc = './downstream1.csv'

fieldname_pfaf = 'PFAF_CODE'
fieldname_segid = 'ComID'

#open shp
shp = gpd.read_file(inshp)
# list of pfaf_code
pfafs = shp[fieldname_pfaf].astype(str).values
seg_ids = shp[fieldname_segid].astype(int).values


def downstream(seg_ids, pfafs, verbose=False):
  # Initialize
  down_id = np.full(len(pfafs),-999)
  down_pfaf = np.full(len(pfafs),'-999',dtype='S32')

  for idx,pfaf in enumerate(pfafs):

    if pfaf =='-999': continue

    # Get slicing position of prefix (all digits minus suffix) and suffix (=last digit) of pfaf code
    # typically n-1 where n is digits of pfaf code if tailing integer(s) is 1, neglect it
    # e.g., 685111 pos=2,  685331 pos=4, 685342 pos=5
    for pos in range(len(pfaf),0,-1):
      digit = int(pfaf[pos-1:pos])
      if digit == 1: continue
      else: break
    prefix = pfaf[:pos-1]
    suffix = pfaf[pos-1:pos]

    # if suffix is even, subtract 1 from last digit of suffix and append it to prefix
    # if suffix is odd, subtract 2 from last digit of suffix and append it to prefix
    if int(suffix)%2 == 0:
      share_code = '%s%d'%(prefix,int(suffix)-1)
    else:
      share_code = '%s%d'%(prefix,int(suffix)-2)

    # get digits of share_code and select indices of pfaf codes that match share_code from pfafs array
    pos = len(share_code)
    arr_index = [i for i, v in enumerate(pfafs) if share_code in v[:pos]]

    # Select downstream code from candidate pfaf codes
    # if there are more than one candidates, find a pfaf code with max digit in tailing codes after codes matching with share_code,
    if len(arr_index)>1:
      for jdx, sub_idx in enumerate(arr_index):
        pfaf1 = pfafs[sub_idx]
        if jdx==0:
          kdx = sub_idx
          last = pfaf1[pos:]
        else:
          current = pfaf1[pos:]
          for ldx, digit in enumerate(current):
            if ldx+1 > len(last):
              break
            if int(digit) > int(last[ldx:ldx+1]):
              kdx = sub_idx
              last = pfaf1[pos:]
              break
            elif int(digit) < int(last[ldx:ldx+1]):
              break
            elif int(digit) == int(last[ldx:ldx+1]):
              continue
      down_pfaf[idx] = pfafs[kdx]
      down_id[idx] = seg_ids[kdx]
    elif len(arr_index) == 1: # if candidate is only one
      if len(pfafs[arr_index[0]]) == pos:
        down_id[idx] = seg_ids[arr_index[0]]
        down_pfaf[idx] = pfafs[arr_index[0]]
      else:
        print('error')
        sys.exit()

    if verbose:
      print('-------------')
      print('%s = %s, %s'%(pfaf, prefix,suffix))
      print('%s'%share_code)
      print(pfafs[arr_index])
      print('%s -> %s'%(pfaf,down_pfaf[idx]))

  return down_id, down_pfaf


if __name__ == '__main__':

  down_id, down_pfaf = downstream(seg_ids, pfafs)

  # write out in ascii (append) using panda dataframe
  df = pd.DataFrame({'seg_id'    :seg_ids,
                     'pfaf_code' :pfafs,
                     'down_id'   :down_id,
                     'down_pfaf' :down_pfaf},
                     columns=['seg_id','pfaf_code','down_id','down_pfaf'])
  with open(outasc, 'w') as f:
    df.to_csv(f, header=True, index = False)

