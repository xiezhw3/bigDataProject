import sys
from pyspark import SparkContext
from main import main
 
input_file_names = [
    "part-00096",
]
 
if __name__ == "__main__":
    sc = SparkContext(appName="wiki-top10")
    RDDs = []
    for input_file_name in input_file_names:
        rdd = sc.textFile(input_file_name)
        RDDs.append(rdd)
    main(RDDs)