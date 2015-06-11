#! /usr/bin/python

import sys

oldNodeId = None
authorList = []

for line in sys.stdin:
    nodeId, authorId = line.strip().split("\t")
    
    if oldNodeId and nodeId != oldNodeId:
        print oldNodeId, authorList
        authorList = []
    oldNodeId = nodeId
    authorList.append(int(authorId))

if oldNodeId:
    print oldNodeId, authorList