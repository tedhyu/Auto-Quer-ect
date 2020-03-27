import boto3
"""
This script takes every 100 lines of the AWS file and outputs into local drive.
"""

s3 = boto3.resource('s3')
obj = s3.Object("athena-tedyu", "Unsaved/2020/03/26/14596464-5556-493f-8f8e-e1378e2ef9b1.csv")
lines = obj.get()['Body'].read().split()
spacing=100


with open('new.csv', 'w') as file:
    count=0
    for row in lines:
        if count%100 == 0:
            file.write(str(row)+"\n")
        count += 1
~                   