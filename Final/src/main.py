#! /usr/bin/env/python
# coding: utf-8

import hashlib

def similarity_between(setA, setB):
    return len(setA.intersection(setB)) / float(len(setA.union(setB)))

def mapper(line):
    url_start_idx = line.find("\"")
    url_end_idx = line.rfind("\"")
    if url_start_idx == -1 or url_end_idx == -1:
        return []
    url = line[url_start_idx + 1 : url_end_idx].split(' ')[1]
    tuples = line.split()
    ip = tuples[0]
    return [(ip, url)]
 
def reduce(x, y):
    return x + '\t' + y

def mapToSet(x):
    linkList = x[1].strip().split('\t')
    s = set(linkList)
    return (len(s), (x[0], s))

def mapNum(x):
    return (len(x[1]), (x[0], x[1]))

def mapper3(x):
    k = []
    if x[0] >= 80:
        length = int(x[0] / 10.0) + 1
        for i in range(0, length):
            k.append(([x[0] - i, x[1]]))
    return k

def filterFun(x):
    return x[1][0][0] !=  x[1][1][0]

def mapper4(x):
    return (similarity_between(x[1][0][1], x[1][1][1]), (x[1][0][0], x[1][1][0]))

def main_func(sc, rdd, url_dict):
    global shared_dict
    shared_dict = sc.broadcast(url_dict)
    result = rdd.flatMap(mapper).flatMap(lambda x: [(x[0], str(shared_dict.value[x[1]]))] if (x[1] in shared_dict.value) else []).\
    reduceByKey(reduce).map(mapToSet).filter(lambda x: x[0] >= 80)
    diff_rdd = result.flatMap(mapper3)
    items = diff_rdd.join(result).filter(filterFun).map(mapper4).filter(lambda x: x[0] > 0.989 and x[0] != 1.0).takeOrdered(1000, key = lambda x: -x[0])
    for item in items:
        if int(item[1][0]) < int(item[1][1]):
            print '%.5f\t%s\t%s' % (item[0], item[1][0], item[1][1])
        else:
            print '%.5f\t%s\t%s' % (item[0], item[1][1], item[1][0])




