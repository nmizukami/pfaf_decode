#!/usr/bin/env python

import numpy as np

'''
https://en.wikipedia.org/wiki/Pfafstetter_Coding_System
pfafstetter coding system

Given a point with code A on the river system, a point with code B is downstream if

The first exactly n digits of each code match, where n >= 0

AND

The remaining digits of B are:

    less than the remaining digits of A

    AND

    all odd.
'''


def check_upstream(pfaf_a, pfaf_b, verbose=False):
  '''
  check if "pfaf_a" is an upstream segment of "pfaf_b"

  Input
    pfaf_a:  scalar, string
    pfaf_b:  scalar, string

  Return
    isUpstream: :scalar, logical

  '''

  if len(pfaf_a) < len(pfaf_b):
    ndigit = len(pfaf_a)
  else:
    ndigit = len(pfaf_b)

  # Find first nth digits that match
  nth = 0
  for dd in np.arange(ndigit):
    if pfaf_a[dd] == pfaf_b[dd]:
      nth += 1
    else:
      break

  isUpstream = True

  # if none of digit matches, A and B are not the same river system
  if nth == 0:
    if verbose:
      print('criteria 1: seg-%s is not upstream of %s' % (pfaf_a, pfaf_b))
    isUpstream = False
  else:
    if pfaf_b[nth:] > pfaf_a[nth:]:
      if verbose:
        print('criteria 2: seg-%s is not upstream of %s' % (pfaf_a, pfaf_b))
      isUpstream = False
    else:
      for dd in np.arange(nth,ndigit):
        if int(pfaf_b[dd]) % 2 == 0:
          if verbose:
            print('criteria 3: seg-%s is not upstream of %s' % (pfaf_a, pfaf_b))
          isUpstream = False
          break

  return isUpstream


def get_outlet(pfafs, verbose=False):
  '''
  Given a list of pfafs of river network, identify outlets

  Input
    pfafs: vector, string, list of pfaf codes

  Return
    pfaf_out: :scalar or vectors, string, pfaf code at outlet
  '''

  pfaf_outlet = [];

  while True :

    pfaf_outlet_tmp = ''

    pfaf_list1 = []

    for pfaf in pfafs:

      if pfaf == '-9999' or pfaf == '0':
        continue

      if not pfaf_outlet_tmp:
        # Initialize guessing outlet
        pfaf_outlet_tmp = pfaf
      else:
        # if current guessing outlet ("pfaf_outlet_tmp") is upstream of "pfaf"
        # Update guessing outlet as "pfaf"
        if check_upstream(pfaf_outlet_tmp, pfaf):
          pfaf_outlet_tmp = pfaf
        else:
          # blacklist if "pfaf_outlet_tmp" is no upstream of "pfaf", could be downstream or outside the network
          pfaf_list1.append(pfaf)

    pfaf_outlet.append(pfaf_outlet_tmp)

    if not pfaf_list1:
      # if blacklist is empty, done
      break
    # Check if blacklisted pfaf codes are actually upstream of "pfaf_outlet_tmp"
    # and update blacklist
    else:
      pfaf_list2 = []
      for pfaf in pfaf_list1:
        if not check_upstream(pfaf, pfaf_outlet_tmp):
          pfaf_list2.append(pfaf)

    # if blacklist is empty, done
    if not pfaf_list2:
      break
    # otherwise find outlet from blacklisted pfaf code
    pfafs = pfaf_list2

  if len(pfaf_outlet) == 1:
    pfaf_outlet = pfaf_outlet[0]

  return pfaf_outlet


def get_tributary(pfaf, pfaf_out):
  '''
  Give a outlet "pfaf_out" and pfaf code, return network category for pfaf (0:outside network, -999:mainstem, tributary code)

  Input
    pfaf:     scalar, string
    pfaf_out: scalar, string

  Return
    tributary: :scalar, string: "-999"=mainstem, "0"=outside river network
  '''

  ndigit = len(pfaf_out)
  ndigit_a = len(pfaf)

  # Find first nth digits that match
  nth = 0
  for dd in np.arange(ndigit):
    if pfaf[dd] == pfaf_out[dd]:
      nth += 1
    else:
      break

  if nth != 0:
    tributary = '-999'            # initialize as mainstem
    for dd in np.arange(nth, ndigit_a):
      if int(pfaf[dd]) % 2 == 0:  # pfaf is tributary
        tributary = pfaf[:dd+1]
        break
  else:
    tributary = '0'   # outside river network

  return tributary

