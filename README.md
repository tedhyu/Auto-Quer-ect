# Auto-Querect

Personalized Auto-Correct for Mobile Devices

Slides:  https://docs.google.com/presentation/d/1ETRXEolbi1zsujgT4A_xpSHWsWtPfVPXFJIyV4LPVas/edit#slide=id.p
<br>Video:  https://www.youtube.com/watch?v=HJ6JcFWGJCs

<hr/>

## How to install and get it up and running

Requirements:  Amazon Web Services

1)  S3:  Set up and S3 bucket.  In this case:  s3://athena-tedyu/
2)  Athena:  Open Athena on AWS.  Follow the instructions to set up "Running SQL Queries with Athena" here:  https://commoncrawl.org/2018/03/index-to-warc-files-and-urls-in-columnar-format/
3)  Run Athena with the example in https://github.com/tedhyu/Auto-Querect/blob/master/athena/athena_instructions.txt
4)  Start EMR in Amazon with Spark and ssh in.
5)  Add the following to ~/.bashrc and source ~/.bashrc
export SPARK_HOME=/usr/lib/spark
export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH  
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/build:$PYTHONPATH
6)  Install the following on EMR with "sudo pip install":  warcio, boto3, bs4, nltk 
7)  Execute main.py in master node.

## Introduction
This app establishes a connection between venue and salesforce data, which were previously not linked.  It enters into two new tables:  attendees and events.

## Architecture
Data Pipeline:  
![Pipeline](https://imgur.com/PIiQevq.png)

## Dataset
CSV file that contains minimum three headers:  email, first name, and last name.  
Two salesforce table in BigQuery:
<br>Attendees:  Email, First_name, Last_name, Guests, Is_salesforce, Datestamp, Eventname, Venue, Eventdate
<br>Events:  Eventname, Venue, Eventdate, Datestamp, Attendance

## Engineering challenges
Multiple schemas of CSV files.  Organizing BigQuery tables in a format that is easily readable and logical.  Error handling algorithm:  
![Error](https://imgur.com/fWY7Drk.png)
