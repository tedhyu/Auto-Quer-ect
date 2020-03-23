from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *

session = SparkSession.builder.getOrCreate()
sqldf = session.read.format("csv").option("header", True).option("inferSchema", True).load("s3://athena-tedyu/bball/2020/03/23/9315090e-a014-4a7b-9560-d92d99f6cce6.csv")
warc_recs = sqldf.select("url", "warc_filename", "warc_record_offset", "warc_record_length").rdd
print warc_recs.collect()
