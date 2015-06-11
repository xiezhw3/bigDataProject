#! /usr/bin/env/python
# coding: utf-8

# from pyspark import SparkConf, SparkContext

# sconf = SparkConf().setMaster("local").setAppName("Correlated Pages")
# sc = SparkContext(conf = sconf)

# lines = sc.textFile("readme")

def mapper(line):
	result = []
	elements = line.strip().split(" ")
	if len(elements) == 5:
		key = elements[1] + ' ' + elements[2]
		val = int(elements[3])
		result.append((key, val))
	return result

def mapTo(x):
	return (x, abs(x[0][1] - x[1][1]))

def main(RDDS):
	print 'project_code1 page_title1 visit_count1 project_code2 page_title2 visit_count1'
	if len(RDDS) > 0:
		lines = RDDS[0]
		if len(RDDS) > 1:
			for i in range(1, len(RDDS)):
				lines = lines.union(RDDS[i])

	keyVal = lines.flatMap(mapper).reduceByKey(lambda x, y: x + y).filter(lambda x: x[1] >= 0).sortByKey()
	keyValMap = keyVal.cartesian(keyVal).filter(lambda x: str(x[0][0]) < str(x[1][0])).map(mapTo).sortBy(lambda x: x[1], True).take(20)
	
	for item in keyValMap:
		if item[0][0][1] < item[0][1][1] or (item[0][0][1] == item[0][1][1] and item[0][0][0] < item[0][1][0]):
			print item[0][1][0] + ' ' + str(item[0][1][1]) + ' ' + item[0][0][0] + ' ' + str(item[0][0][1])
		else:
			print item[0][0][0] + ' ' + str(item[0][0][1]) + ' ' + item[0][1][0] + ' ' + str(item[0][1][1])