#! /usr/bin/python

import sys

totalVal = 0
totalNum = 0
oldAuthor = None

for line in sys.stdin:
	autoId, bodyLen = line.strip().split("\t")

	if oldAuthor and oldAuthor != autoId:
		print "{0}\t{1}".format(oldAuthor, float(totalVal) / float(totalNum))
		totalVal = 0
		totalNum = 0


	oldAuthor = autoId
	totalVal += int(bodyLen)
	totalNum += 1

if oldAuthor:
	print "{0}\t{1}".format(oldAuthor, float(totalVal) / float(totalNum))
