from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *

session = SparkSession.builder.getOrCreate()
sc = SparkContext.getOrCreate()
spark = SparkSession(sc)
df = spark.read.load('s3://commoncrawl/cc-index/table/cc-main/warc/')
df.createOrReplaceTempView('ccindex')
