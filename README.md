# Auto-Querect

Personalized Auto-Correct for Mobile Devices
<br>Presentation:  https://docs.google.com/presentation/d/15lw0YoCaAgi6aS3IDdqB2xxnaMgcg-fHXuMsZ4Jo9qw/edit?usp=sharing

<hr/>

## How to install and get it up and running

Requirements:  Amazon Web Services

1)  S3:  Set up and S3 bucket.  In this case:  s3://athena-tedyu/
2)  Athena:  Open Athena on AWS.  Follow the instructions to set up "Running SQL Queries with Athena" here:  https://commoncrawl.org/2018/03/index-to-warc-files-and-urls-in-columnar-format/
3)  Run Athena with the example in https://github.com/tedhyu/Auto-Querect/blob/master/athena/athena_instructions.txt
4)  Start EMR in Amazon with Spark and Hadoop.  SSH in.
5)  Add the following to ~/.bashrc and type "source ~/.bashrc"<br>
export SPARK_HOME=/usr/lib/spark<br>
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH  <br>
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH
6)  Install the following on EMR (both master and workers) with "pip install --user": warcio, boto3, bs4, nltk
7)  Execute main.py in master node.

## Introduction
Basketball fans, are you tired that your phone's auto-correct changes Celtics to Clerics, even though your phone should "know" that you text about the NBA with your friends all the time?  This app finds proper nouns of the individual's most often-used subject matter (e.g. NBA, cricket, music) and includes it to an auto-correct dictionary.  The proper nouns are the most often-used words related to a subject as queried through the common crawl data lake.  Using very little processing power, the most common words that are not in an English dictionary are found that is related to a subject.  For example when doing a short query for NBA, the app returns the following top 10 words:  Lakers, Celtics, Knicks, Timberwolves, Skyforce, Stats, Grande, Facebook, Antonio, Chris.

When an individual is found to text a lot of NBA words, the top words in the query will be added to their auto-correct dictionary.  This app updates the auto-correct dictionary so that the newest trending terms, for example new NBA rookies, are constantly updated.

The key to making a great auto-correct dictionary is to strike a balance between a short and long dictionary.  A short dictionary will not contain enough words, while the long dictionary will incorrectly change words to little used words that were probably not the author's intention.  The ideal dictionary is a customized one, catering to the writing habit of the author.  Most auto-correct already does this...kind of...  When one forces the auto-correct to accept a word, that word is added to the dictionary.  Yet, the goal of Auto-Querect is to make it so that the dictionary "knows" rare words you are likely to type.

## Architecture
Data Pipeline:  
![Pipeline](https://imgur.com/cJtaUBu.png)

##Environment Setup
Install and configure AWS and the open-source tool and setup an AWS EMR cluster. At launch time, emr-5.30.0 version was used. It comes with Python version 3.7.6, pyspark version 2.4.5-amzn-0 and Zeppelin 0.8.2.

## Dataset
Common Crawl Dataset, WARC data:  https://commoncrawl.org/the-data/

##Repository Structure and Run Instructions
./athena/ contains instructions on how to query common crawl data with AWS Athena .
./frontend/ contains the main.py spark script to launch spark jobs using the output from athena query

## Engineering challenges
Common Crawl Dataset contains 50 PetaBytes of data.  The navigation of thie data lake with metadata is a challenge.  Optimizing Spark so that there is efficient scaling with increased cluster size.

## References:
Very useful poster about getting started with Athena and Common Crawl:  http://netpreserve.org/ga2019/wp-content/uploads/2019/07/IIPCWAC2019-SEBASTIAN_NAGEL-Accessing_WARC_files_via_SQL-poster.pdf