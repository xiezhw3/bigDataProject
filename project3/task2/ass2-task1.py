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
		continue
	urlEndIndex = line.find(" HTTP/")
	if urlEndIndex == -1:
		continue
	pageLink = line[urlStartIndex + 5 : urlEndIndex]
	result.append((pageLink, 1))
	return result

def reducer(x, y):
	return x + y

f = open("result", "w")

for result in lines.flatMap(mapper).reduceByKey(reducer).collect():
	f.write(result[0].encode('utf8') + " " + str(result[1]) + "\n")
f.close()