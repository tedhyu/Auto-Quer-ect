# Auto-Querect

Personalized Auto-Correct for Mobile Devices
Presentation:  https://docs.google.com/presentation/d/15lw0YoCaAgi6aS3IDdqB2xxnaMgcg-fHXuMsZ4Jo9qw/edit?usp=sharing

<hr/>

## How to install and get it up and running

Requirements:  Amazon Web Services

1)  S3:  Set up and S3 bucket.  In this case:  s3://athena-tedyu/
2)  Athena:  Open Athena on AWS.  Follow the instructions to set up "Running SQL Queries with Athena" here:  https://commoncrawl.org/2018/03/index-to-warc-files-and-urls-in-columnar-format/
3)  Run Athena with the example in https://github.com/tedhyu/Auto-Querect/blob/master/athena/athena_instructions.txt
4)  Start EMR in Amazon with Spark and Hadoop.  SSH in.
5)  Add the following to ~/.bashrc and source ~/.bashrc:
export SPARK_HOME=/usr/lib/spark
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH  
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH
6)  Install the following on EMR with "sudo pip install":  warcio, boto3, bs4, nltk 
7)  Execute main.py in master node.

## Introduction
This app finds proper nouns of the individual's most often-used subject matter (e.g. NBA, cricket, music) and includes it to an auto-correct dictionary.  The proper nouns are the most often-used
words related to a subject as queried through the common crawl data lake.  Using very little processing power, the most common words that are not in an English dictionary are found that is 
related to a subject.  For example when doing a short query for NBA, the app returns the following top 10 words:  Lakers, Celtics, Knicks, Timberwolves, Skyforce, Stats, Grande, Facebook, Antonio, Chris.

When an individual is found to text a lot of NBA words, the top words in the query will be added to their auto-correct dictionary.

## Architecture
Data Pipeline:  
![Pipeline](https://imgur.com/PIiQevq.png)

## Dataset
Common Crawl Dataset, WARC data:  https://commoncrawl.org/the-data/

## Engineering challenges
Common Crawl Dataset contains 50 PetaBytes of data.  The navigation of thie data lake with metadata is a challenge.  Optimizing Spark so that there is efficient scaling with increased cluster size.