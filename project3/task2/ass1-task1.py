#! /usr/bin/env/python
# coding: utf-8

from pyspark import SparkConf, SparkContext

sconf = SparkConf().setMaster('local').setAppName('Purchase')
sc = SparkContext(conf = sconf)

lines = sc.textFile('purchases.txt')

def mapper(line):
	result = []
	items = line.strip().split("\t")
	if len(items) == 6:
		result.append((items[2], float(items[4])))
	return result

def reducer(x, y):
	return x + y

f = open("result", "w")

for result in lines.flatMap(mapper).reduceByKey(reducer).collect():
	f.write(result[0].encode('utf8') + "\t" + str(result[1]) + "\n")
f.close()



































