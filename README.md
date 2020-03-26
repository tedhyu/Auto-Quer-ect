# Auto-Querect

Personalized Auto-Correct for Mobile Devices

Slides:  https://docs.google.com/presentation/d/1ETRXEolbi1zsujgT4A_xpSHWsWtPfVPXFJIyV4LPVas/edit#slide=id.p
<br>Video:  https://www.youtube.com/watch?v=HJ6JcFWGJCs

<hr/>

## How to install and get it up and running

Requirements:  Amazon Web Services

1)  S3:  Set up and S3 bucket.  In this case:  s3://athena-tedyu/
2)  Athena:  Open Athena on AWS.  Follow the instructions to set up "Running SQL Queries with Athena" here:  https://commoncrawl.org/2018/03/index-to-warc-files-and-urls-in-columnar-format/
3)  Run Athena with the example in the 
5)  Input CSV File:  The event file must contain the headers:  "Email", "Last Name", "First Name".  If there are multiple columns containing these words, priority will be given to the headers "Buyer Email", "Buyer Last Name", and "Buyer First Name".
6)  BigQuery:  Set up Three BigQuery Tables:
<br>a)  customertable.salesforce - This is a BigQuery table imported from Salesforce.  It has one column needed which is Email_address.
<br>b)  customertable.attendees - Email(String), First_name(string), Last_name(string), Guests(integer), Is_salesforce(boolean), Datestamp(timestamp), Eventname(string), Venue(String), Eventdate(string)
<br>c)  customertable.events - Eventname(string), Venue(string), Eventdate(string), Datestamp(timestamp), Attendance(integer)
<hr/>

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
