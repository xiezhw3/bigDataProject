#! /usr/bin/python

import sys, heapq

oldKeyWord = None
keyWordList = []
tags = {}

for line in sys.stdin:
    keyWord, location = line.strip().split(" ")
    if oldKeyWord and oldKeyWord != keyWord:
        lineOut = oldKeyWord
        num = 0
        keyWordList = sorted(keyWordList)
        for item in keyWordList:
            lineOut = lineOut + ' ' + item
            num += 1
        keyWordList = []
        tags[lineOut] = num
    oldKeyWord = keyWord
    keyWordList.append(location)

if oldKeyWord:
    num = 0
    lineOut = oldKeyWord
    keyWordList = sorted(keyWordList)
    for item in keyWordList:
        lineOut = lineOut + ' ' + item
        num += 1
    tags[lineOut] = num

top100 = heapq.nlargest(100, tags, key = lambda x: (tags[x], x))
 
for item in top100:
    print item + '\t' + str(tags[item])