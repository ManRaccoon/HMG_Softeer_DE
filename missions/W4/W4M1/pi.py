import sys
from random import random
from operator import add
import datetime

from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("SparkPi") \
        .getOrCreate()

    slices = int(sys.argv[1]) if len(sys.argv) > 1 else 2

    n = 100000 * slices

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x**2 + y**2 <= 1 else 0

    startTime = datetime.datetime.now()
    count = spark.sparkContext.parallelize(range(1, n + 1), slices).map(f).reduce(add)
    endTime = datetime.datetime.now()

    pi_estimate = 4.0 * count / n
    print(f"Pi is roughly {pi_estimate}")

    time = endTime - startTime
    outputPath = sys.argv[2]
    spark.sparkContext.parallelize([pi_estimate], 1).saveAsTextFile(outputPath)

    spark.stop()