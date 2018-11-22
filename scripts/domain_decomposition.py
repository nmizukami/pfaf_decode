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
inshp = '../test_data/nhdPlus_SHPs_pfaf/Flowline_CO_14.shp' # to get seg-id, pfaf
network = '../test_data/NHDPlus2_updated-CONUS.nc'  # to get seg-id, seg-index and downstream-index
#output
outasc = './my_csv.csv'

fieldname_pfaf = 'PFAF_CODE'
fieldname_segid = 'ComID'

nThresh = 10000

#open shp
shp = gpd.read_file(inshp)
# list of pfaf_code
pfafs = shp[fieldname_pfaf].astype(str).values
seg_ids = shp[fieldname_segid].astype(int).values

# #open netcdf
# netopo = xr.open_dataset(network)
# segID = netopo['link'].values
# downSegIndex = netopo['downSegIndex'].values

# Outlet pfafstetter code
pfaf_outlet = '965311'
#pfaf_outlet = pfaf.get_outlet(pfafs)
# '965311', '9602111', '96021101', '96020021', u'9602006', u'96020041', u'9653011', u'96521111'
pfafCode = '96'


def decomposition(seg_ids, pfafs, pfafCode):

  for iPfaf0 in range(1,10):
    pfafCode = '%s%d'%(pfafCode,iPfaf0)               # Append new digit
    pfafs_sub = [x[:len(pfafCode)] for x in pfafs]    # get pfaf code at the "pfafCode" level
    ixMatch = [i for i, str_elem in enumerate(pfafs_sub) if pfafCode in str_elem]  # find match with "pfafCode"
    nMatch = len(ixMatch)
    print('pfafCode, number of matches = %s, %d'%(pfafCode, nMatch))

    if (nMatch == 0):
      pfafCode = pfafCode[0:len(pfafCode)-1]
      continue

    if(nMatch < nThresh):
      print('nMatch less than nThrehold = %d - aggregate' % (nThresh))
      # assign pfaf_code for mainstem and tributaries for "pfafCode" basin
      b = np.array(ixMatch)
      idAggregate, numAggregate = aggregate(pfafCode, pfafs[b])
      # write out in ascii (append) using panda dataframe
      df = pd.DataFrame({'seg_id':seg_ids[b],
                         'pfaf_code':pfafs[b],
                         'idAggre'  :idAggregate,
                         'numAggre' :numAggregate},
                         columns=['seg_id','pfaf_code','idAggre','numAggre'])
      with open(outasc, 'a') as f:
        df.to_csv(f, header=False, index = False)

    else:
      print('nMatch more than nThrehold = %d - disaggregate' % (nThresh))
      decomposition(seg_ids, pfafs, pfafCode)

    # decrement
    pfafCode = pfafCode[0:len(pfafCode)-1]


def aggregate(pfafCode, subset_pfafs):
  # Initialization
  idAggregate = np.full(len(subset_pfafs),'-999')
  numAggregate = np.full(len(subset_pfafs),'-999',dtype=int)

  # get pfaf old and pfaf new
  pfaf_old = int(pfafCode[-2:-1])
  pfaf_new = int(pfafCode[-1:])

  # check if an interbasin
  isInterbasin = ((pfaf_new % 2)==1)
  isHeadwater  = ((pfaf_old % 2)==0 and pfaf_new==9)

  # get closed basin segments
  ixClosed = find_closed_basin(pfafCode, subset_pfafs)

  if (isInterbasin and not isHeadwater):   # if a river reach is in inter-basin and not headwater
    # populate mainstem segments
    ixMainstem = find_mainstems(pfafCode, subset_pfafs)
    nMainstem = np.sum(ixMainstem)
    print('nMainstem = %d'%nMainstem)
    idAggregate[ixMainstem]  = '-%s'%(pfafCode)
    numAggregate[ixMainstem] = nMainstem

    # populate tributary segments
    tribs_pfafs = subset_pfafs[np.invert(ixMainstem)]
    trib_outlet_pfafs = pfaf.get_outlet(tribs_pfafs)
    nTrib = len(trib_outlet_pfafs)
    print('nTrib = %d'%nTrib)
    for pfaf_out in trib_outlet_pfafs:             # loop through each tributary
      mainstem_code = pfaf.get_mainstem(pfaf_out)  # get mainstem code in current tributary
      subset_code = [x[:len(mainstem_code)] for x in subset_pfafs]                         # get sbuset code at the tributary mainstem level
      ixTrib = [i for i, str_elem in enumerate(subset_code) if mainstem_code in str_elem]  # find match with "mainstem_code"
      idAggregate[ixTrib] = mainstem_code
      numAggregate[ixTrib] = len(ixTrib)

  else:    # a river reach is in tributary basin or headwater
    idAggregate[:] = pfafCode
    numAggregate[:] = len(subset_pfafs)

  idAggregate[ixClosed] = '-777'
  numAggregate[ixClosed] = '-777'

  return idAggregate, numAggregate


def find_mainstems(pfafCode, pfafs):
  # initialize output
  nStream = len(pfafs)
  isMainstem = np.full(nStream, False)

  # get the length of the basin ID (=pfafCode)
  uniqLen = len(pfafCode)

  if nStream == 1: # simple case of one stream segment
    isMainstem[0] = True
  else:            # standard case: find odd-numbered segments
    for iStream, pfaf in enumerate(pfafs):
      # disaggregate pfafsttter code ** REMAINDER** into a vector of digits
      # check if all of the remainder is odd
      count = 0
      for digit in pfaf[uniqLen:]:
        if int(digit)%2 == 0:
          break
        count += 1
      if count == len(pfaf[uniqLen:]):
        isMainstem[iStream] = True

  return isMainstem


def find_closed_basin(pfafCode, pfafs):
  # initialize output
  nStream = len(pfafs)
  isClosed = np.full(nStream, False)

  # get the length of the basin ID (=pfafCode)
  uniqLen = len(pfafCode)

  for iStream, pfaf in enumerate(pfafs):
    for digit in pfaf[uniqLen:]:
      if int(digit) == 0:
        isClosed[iStream] = True
        break

  return isClosed


def get_common_code(pfafs):


  return common_code


if __name__ == '__main__':
  decomposition(seg_ids, pfafs, pfafCode)

