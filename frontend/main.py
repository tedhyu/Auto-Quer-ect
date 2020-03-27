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
    """Converts html page to text
    Args:
        page:  html
    Returns:
        soup.get_text(" ", strip=True):  string
    """
    try:
        encoding = EncodingDetector.find_declared_encoding(page, is_html=True)
        soup = BeautifulSoup(page, "lxml", from_encoding=encoding)
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(" ", strip=True)
    except:
        return ""

def fetch_process_warc_records(rows):
    """Retrieves document from S3 Data Lake.  The argument is a row of warc_filename, warc_record_offset, warc_record_length.  
       The html to be retrieved are pulled from the file using the offset and length.  
    Args:
        rows: list[string, int, int]
    Returns:
        fetch_process_warc_records
    """
    s3client = boto3.client('s3')
    for row in rows:
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
                yield word, 1   #create key as word and index as 1


session = SparkSession.builder.getOrCreate()  #Create Spark Session

#Read csv from athena output.  Take rows
sqldf = session.read.format("csv").option("header", True).option("inferSchema", True).load("s3://athena-tedyu/Unsaved/2020/03/26/14596464-5556-493f-8f8e-e1378e2ef9b1.csv")

#Create rdd of the 1000 rows selected
warc_recs = sqldf.select("warc_filename", "warc_record_offset", "warc_record_length").rdd

#convert to unicode
word_pattern = re.compile('\w+', re.UNICODE)

#mapPartition gets a list of words and 1's.  Filter removes all words that don't start with capital.  reduceByKey combines all a's and gets word count.  sortBy sorts by largest count to smallest. 
word_counts = warc_recs.mapPartitions(fetch_process_warc_records).filter((lambda a: re.search(r'^[A-Z][a-z]', a[0]))).reduceByKey(lambda a, b: a + b).sortBy(lambda a: a[1], ascending=False)

list= word_counts.take(1000)
new_list=[]
for i in list:
    if i[0].lower() not in nltk.corpus.wordnet.words():  #filters by wordnet library
        lower_case = Lem.lemmatize(i[0].lower())         #converts any plurals to singular
        if lower_case not in nltk.corpus.words.words():  #filter by words library
            new_list.append(i)                           #adds to list.

print(new_list)
