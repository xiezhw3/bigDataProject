#!/usr/bin/python
import sys

for line in sys.stdin:        
    items = line.strip().split("\t")
    if len(items) != 2:
        continue
    key, tag = items
    print "{0}\t{1}\t{2}".format(0, items[0], items[1])