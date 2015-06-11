#! /usr/bin/env/python
#encoding: utf-8

from pyspark import SparkConf, SparkContext

sconf = SparkConf().setMaster("local").setAppName("Access_log")
sc = SparkContext(conf = sconf)

lines = sc.textFile("access_log")

def mapper(line):
	result = []
	urlStartIndex = line.find("\"GET ")
	if urlStartIndex == -1:
		urlStartIndex = line.find("\"POST ")
		urlStartIndex += 1
	if urlStartIndex == 0:
		urlStartIndex = line.find("\"HEAD ")
		urlStartIndex += 1
	if urlStartIndex == 0:
		return result
	urlEndIndex = line.find(" HTTP/")
	if urlEndIndex == -1:
		return result
	pageLink = line[urlStartIndex + 5 : urlEndIndex]

	state = line[urlEndIndex + 11 : urlEndIndex + 14] + "\t" + "-1"
	result.append((pageLink, state))
	return result

def reducer(x, y):
	xItems = x.strip().split("\t")
	yItems = y.strip().split("\t")

	if xItems[1] == "-1":
		total = 1
		if int(xItems[0]) >= 400 and int(xItems[0]) < 600:
			fail = 1
		else:
			fail = 0
	else:
		total = int(xItems[0])
		fail = int(xItems[1])

	if yItems[1] == "-1":
		total += 1
		if int(yItems[0]) >= 400 and int(yItems[0]) < 600:
			fail += 1
	else:
		total += int(yItems[0])
		fail += int(yItems[1])

	return str(str(total) + "\t" + str(fail))

f = open("result", "w")

for result in lines.flatMap(mapper).reduceByKey(reducer).collect():
	items = result[1].strip().split("\t")
	if items[1] == "-1":
		items[0] = "1"
		items[1] = "0"
	rate = float(items[1]) / float(items[0])
	f.write(result[0].encode('utf8') + " " + str(rate) + "\n")
f.close()