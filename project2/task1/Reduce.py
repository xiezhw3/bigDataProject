#! /usr/bin/python

import sys

totalVal = 0
totalNum = 0

for line in sys.stdin:
    bodyLen = int(line.strip())
    totalVal += bodyLen
    totalNum += 1
    
print float(totalVal) / float(totalNum)