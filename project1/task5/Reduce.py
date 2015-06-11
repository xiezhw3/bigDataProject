#! /usr/bin/python

import sys

oldNodeId = None
authorList = []

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) != 2:
    	continue
    nodeId, authorId = data
    if oldNodeId and nodeId != oldNodeId:
        print oldNodeId, sorted(authorList)
        authorList = []
    oldNodeId = nodeId
    authorList.append(int(authorId))

if oldNodeId:
    print oldNodeId, sorted(authorList)