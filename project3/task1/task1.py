#! /usr/bin/env/python
# coding: utf-8

def mapper(line):
	result = []
	elements = line.strip().split(" ")
	if len(elements) == 5:
		key = elements[1] + ' ' + elements[2]
		val = int(elements[3])
		result.append((key, val))
	return result

def main(RDDS):
	if len(RDDS) > 0:
		lines = RDDS[0]
		if len(RDDS) > 1:
			for i in range(1, len(RDDS)):
				lines = lines.union(RDDS[i])

		for i in lines.flatMap(mapper).reduceByKey(lambda x, y: x + y).takeOrdered(10, key = lambda x: -x[1]):
			print i[0] + " " + str(i[1])