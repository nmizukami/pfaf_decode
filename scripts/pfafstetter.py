#!/usr/bin/env python

import sys
from collections import defaultdict


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
  for dd in range(ndigit):
    if pfaf_a[dd] == pfaf_b[dd]:
      nth += 1
    else:
      break

  isUpstream = True

  # if none of digit matches, A and B are not the same river system
  if nth == 0:
    if verbose:
      print('prafs %s and %s are not the same system' % (pfaf_a, pfaf_b))
    isUpstream = False
  else:
    if len(pfaf_b) != nth and len(pfaf_a) != nth:
      #if pfaf_b[nth:] > pfaf_a[nth:]:
      if int(pfaf_b[nth]) > int(pfaf_a[nth]):
        if verbose:
          print('pfaf-%s is greater than pfaf %s after match' % (pfaf_b, pfaf_a))
        isUpstream = False
      else:
        for dd in range(nth,len(pfaf_b)):
          if int(pfaf_b[dd]) % 2 == 0:
            if verbose:
              print('pfaf-%s include even number after match - %s ' % (pfaf_b, pfaf_b[nth:]))
            isUpstream = False
            break

    elif len(pfaf_b) != nth and len(pfaf_a) == nth:
      isUpstream = False

  return isUpstream


def get_subbasin(pfafs, pfaf_outlet):
  '''
  Given a list of pfaf codes and pfaf code for desired segment in network, obtain list of upstream pfaf codes
  Input

    pfafs:       list of pfaf codes,            vector, string
    pfaf_outlet: pfaf code at desired segment,  scalar, string

  Return

    sub_pfafs: list of pfaf codes upstream of outlet pfaf, vector, str

  '''
  sub_pfafs = []
  for pfaf in pfafs:

    if pfaf == '-9999' or pfaf == 0:
      continue

    check = check_upstream(pfaf, pfaf_outlet)

    if check:
     sub_pfafs.append(pfaf)

  return sub_pfafs


def get_outlet(pfafs, verbose=False):
  '''
  Given a list of pfafs of river network, identify outlets

  Input
    pfafs: vector, string, list of pfaf codes

  Return
    pfaf_out: list of pfaf codes at oulets, vector, string
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
  for dd in range(ndigit):
    if pfaf[dd] == pfaf_out[dd]:
      nth += 1
    else:
      break

  if nth != 0:
    tributary = '-999'            # initialize as mainstem
    for dd in range(nth, ndigit_a):
      if int(pfaf[dd]) % 2 == 0:  # pfaf is tributary
        tributary = pfaf[:dd+1]
        break
  else:
    tributary = '0'   # outside river network

  return tributary


def get_tributaries(pfafs, lwr_threshold, pfaf_outlet=[]):
  '''
  Give a list of pfaf codes, threshold of number of segments, and list of outlet pfaf codes in tributary, return groups of tributaries

  Input

    pfafs:         list of pfaf_codes,                             vector, string
    lwr_threshold: lower threshold of number of tributary segment, scaler, integer
    pfafs_outlet:  list of mainstem outlet pfaf_codes,             vector, string, optional

    a number of tributary segments has to be greater than lwr_threshold

  Return

    tributary: dictionary, key:   mainstem outlet pfaf
                           items: key:   tributary code
                                  value: list of pfafs, vector, string
  '''

  if not pfaf_outlet:
    pfaf_outlet = get_outlet(pfafs)

  tributary = {}

  for pfaf_out in pfaf_outlet:

    tributary_tmp = defaultdict(list)

    for pfaf in pfafs:

      if pfaf == '-9999' or pfaf == 0:
        continue

      tributary_code = get_tributary(pfaf, pfaf_out)

      if tributary_code != '-999' and tributary_code != '0':

        tributary_tmp[tributary_code].append(pfaf)

    for key, values in tributary_tmp.items():

      if (len(values) < lwr_threshold):
        del tributary_tmp[key]

    tributary[pfaf_out] = tributary_tmp

  return tributary


def get_mainstem(pfaf, verbose=False):
  '''
  Input


  Return

    mainstem: mainstem code relative to outlet, scalar, integer
  '''

  # look for consecutive odd digit from last level

  ndigits = len(pfaf)

  pfaf_head = '-999'

  for dd in range(ndigits-1, -1, -1):
    if int(pfaf[dd]) % 2 == 0:
      break

  pfaf_head = pfaf[:dd+1]

  return pfaf_head


def get_tributary_v1(pfafs, lwr_threshold):
  '''
  Give a list of pfaf codes, threshold of number of segments, and list of outlet pfaf codes in tributary, return groups of tributaries

  Input

    pfafs:         list of pfaf_codes,                             vector, string
    lwr_threshold: lower threshold of number of tributary segment, scaler, integer
    pfafs_outlet:  list of mainstem outlet pfaf_codes,             vector, string, optional

    a number of tributary segments has to be greater than lwr_threshold

  Return

    tributary: dictionary, key:   mainstem outlet pfaf
                           items: key:   tributary code
                                  value: list of pfafs, vector, string
  '''

  mainstem_tmp = defaultdict(list)

  for pfaf in pfafs:

    if pfaf == '-9999' or pfaf == 0:
      continue

    mainstem_code = get_mainstem(pfaf)

    mainstem_tmp[mainstem_code].append(pfaf)

  mainstem = {}

  for _, mainstem_pfafs in mainstem_tmp.items():

    mainstem_outlet = get_outlet(mainstem_pfafs)

    trib_pfafs = get_subbasin(pfafs, mainstem_outlet[0])

    if len(trib_pfafs) > lwr_threshold:

      mainstem[mainstem_outlet[0]] = trib_pfafs

  return mainstem

