#! /usr/bin/env/python
# coding: utf-8

def mapper(line):
    result = []
    elements = line.strip().split(" ")
    key = elements[1] + '\t' + elements[2]
    val = int(elements[3])
    result.append((key, val))
    return result
    
def mapTo(x):
    return (abs(x[0][1] - x[1][1]), x)

def main(RDDS):
    if len(RDDS) > 0:
        lines = RDDS[0]
        if len(RDDS) > 1:
            for i in range(1, len(RDDS)):
                lines = lines.union(RDDS[i])
                
        sc = lines.context
        keyVal = lines.flatMap(mapper).reduceByKey(lambda x, y: x + y).filter(lambda x: x[1] >= 10000).sortBy(lambda x: x[1]).collect()
        count_ = len(keyVal)
        left = []
        right = []
        for i in range(count_):
            left.append((i, keyVal[i]))
            right.append((i + 1, keyVal[i]))
            
        joinLeft = sc.parallelize(left)
        joinRight = sc.parallelize(right)
        for item in joinLeft.join(joinRight).map(lambda x: (x[1], abs(x[1][0][1] - x[1][1][1]))).takeOrdered(20, key = lambda x: x[1]):
            if (item[0][0][1] < item[0][1][1]) or (item[0][0][1] == item[0][1][1] and item[0][0][0] < item[0][1][0]):
                print item[0][1][0], '\t', item[0][1][1], '\t', item[0][0][0], '\t', item[0][0][1]
            else:
                print item[0][0][0], '\t', item[0][0][1], '\t', item[0][1][0], '\t', item[0][1][1]