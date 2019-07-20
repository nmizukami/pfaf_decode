#!/usr/bin/env python
'''
Assign m domains into n groups based on number of segments within domains
'''

import sys
import pandas as pd
import numpy as np

nProc = 11 # 10 used for tributary segments and 1 is used for mainstem + small tributaries
in_asc = 'junk.csv'
outasc = 'my_csv_1core.csv'

# read csv (number of rows are number of all the segments)
df = pd.read_csv(in_asc, names=['seg_id','pfaf_code','basin_pfaf','nseg'])
print('Total number of segments = %d'%len(df))
# Group based on basin_pfaf code
df1 = df.groupby('basin_pfaf')['nseg'].mean()
df2 = df1.reset_index()
# sort based on number of tributary or mainstem segments
df3 = df2.sort_values(by=['nseg'], ascending=False)

# Split mainstem and tributaries
df_main = df3.loc[df3['basin_pfaf']<0]
df_trib = df3.loc[df3['basin_pfaf']>0]

nTrib = len(df_trib)
print('Number of unique tributaries = %d'%nTrib)

nMainstems = df_main['nseg'].sum()
nTrib_segs = df_trib['nseg'].sum()

print('Total number of tributary segments = %d'%nTrib_segs)

nEven = nTrib_segs/nProc
print('Approx. number of segments processed per core = %d'%nEven)

# Mainstem cores is used to process mainstem and small tributaries (off course, tributaries processed prior to mainstems)
# Going through tributaries from the smallest, and accumulate number of tributary segments up to "nEven", which is nAgg
# count a number of tributaries that are processed in mainstem cores
core = {}
nAgg=0
nReserved=0
for _, row in df_trib.iloc[::-1].iterrows():
  nAgg = nAgg + row['nseg']
  nReserved = nReserved+1
  core[row['basin_pfaf']]=nProc
  if(nAgg > nEven):
     break

# number of tributaries to be distributed to nProc-1 cores
nDistrib = nTrib - nReserved

print('Total number of mainstem segments processed in mainstem core = %d'%nMainstems)
print('Total number of tributary segments processed in mainstem core = %d'%nAgg)
print('Number of tributaries processed in mainstem core = %d'%nReserved)
print('Number of tributaries processed in distributed core = %d'%nDistrib)

# Distribute larger tributary to distributed cores
iWork = np.full(nProc-1, 0, dtype='int')
nComm = np.full(nProc-1, 0, dtype='int')
for _, row in df_trib.iloc[:nDistrib].iterrows():
  idx = np.argmin(iWork)
  iWork[idx] = iWork[idx] + row['nseg']
  nComm[idx] = nComm[idx] + 1
  core[row['basin_pfaf']]=idx
  print('%s,%d,%d,%d'%(row['basin_pfaf'],idx,row['nseg'],iWork[idx]))
print('iWork = '),
for idx in range(nProc-1):
  print('%4d '%iWork[idx]),

print('\nnComm = '),
for idx in range(nProc-1):
  print('%4d '%nComm[idx]),
print('\n'),

seg_core = np.full(len(df), -999, dtype='int')
for idx,row in df.iterrows():
  if row['basin_pfaf'] < 0:
    seg_core[idx] = nProc
  else:
    seg_core[idx] = core[row['basin_pfaf']]

df['core'] = seg_core
with open(outasc, 'w') as f:
  df.to_csv(f, header=True, index = False)
