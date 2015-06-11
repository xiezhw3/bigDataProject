#! /usr/bin/python

import sys, heapq
from operator import *
 
oldKey = None
tags = {}
 
for line in sys.stdin:
    data_mapped = line.strip().split('\t')
    if len(data_mapped) != 3:
        continue
    zero, tag, num = data_mapped
    if not tag in tags.keys():
        tags[tag] = 0
    tags[tag] += int(num)
 
top100 = heapq.nlargest(100, tags, key = lambda x: (tags[x], x))

for item in top100:
    print item