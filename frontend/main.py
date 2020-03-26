from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import *
import re
import boto3
import nltk
from warcio.archiveiterator import ArchiveIterator
from io import BytesIO
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from nltk.stem.wordnet import WordNetLemmatizer
Lem = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('words')


def html_to_text(page):
    try:
        encoding = EncodingDetector.find_declared_encoding(page, is_html=True)
        soup = BeautifulSoup(page, "lxml", from_encoding=encoding)
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(" ", strip=True)
    except:
        return ""

def fetch_process_warc_records(rows):
    s3client = boto3.client('s3')
    for row in rows:
        url = row['url']
        warc_path = row['warc_filename']
        offset = int(row['warc_record_offset'])
        length = int(row['warc_record_length'])
        rangereq = 'bytes={}-{}'.format(offset, (offset+length-1))
        response = s3client.get_object(Bucket='commoncrawl', Key=warc_path, Range=rangereq)
        record_stream = BytesIO(response["Body"].read())
        for record in ArchiveIterator(record_stream):
            page = record.content_stream().read()
            text = html_to_text(page)
            words = map(lambda w: w, word_pattern.findall(text))
            for word in words:
                yield word, 1


session = SparkSession.builder.getOrCreate()
sqldf = session.read.format("csv").option("header", True).option("inferSchema", True).load("s3://athena-tedyu/bball/2020/03/24/99b65ef8-d73f-444e-8685-dd1d1261dd46.csv")
warc_recs = sqldf.select("url", "warc_filename", "warc_record_offset", "warc_record_length").rdd

word_pattern = re.compile('\w+', re.UNICODE)
word_counts = warc_recs.mapPartitions(fetch_process_warc_records).filter((lambda a: re.search(r'^[A-Z][a-z]', a[0]))).reduceByKey(lambda a, b: a + b).sortBy(lambda a: a[1], ascending=False)

list= word_counts.take(1000)
new_list=[]
for i in list:
    if i[0].lower() not in nltk.corpus.wordnet.words():
        lower_case = Lem.lemmatize(i[0].lower())
        if lower_case not in nltk.corpus.words.words():
            new_list.append(i)

print(new_list)
