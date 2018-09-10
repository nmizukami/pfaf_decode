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
  check "pfaf_a" is an upstream segment of "pfaf_b"

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


def check_mainstem(pfaf, pfaf_out, verbose=False):
  '''
  check "pfaf" is a mainstem of river network with "pfaf_out" outlet

  Input
    pfaf:     scalar, string
    pfaf_out: scalar, string

  Return
    isMainstem: :scalar, logical

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

  isMainstem=True

  for dd in np.arange(nth,ndigit_a):
    if int(pfaf[dd]) % 2 == 0:
      isMainstem=False
      break

  return isMainstem


