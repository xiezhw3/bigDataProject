import sys
from pyspark import SparkContext
from main import *
 
if __name__ == "__main__":
    sc = SparkContext(appName="Co-occurrence")
    global shared_dict
    url_dict = {}      
    f = open("object_mappings.sort", "r")
    for line in f:
        line = line.strip()
        idx = line.find(" ")
        url_id = int(line[:idx])
        url = line[idx + 1:].rstrip()
        url_dict[url] = url_id
    f.close()
    rdd = sc.textFile("readme")
    main_func(sc, rdd, url_dict)