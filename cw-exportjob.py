#This function is to export CWlogs to a specified s3 bucket with custom prefix
#Prefix here is the loggroup name itself but replacing / with - Ex: /aws/lambda/test will have a prefix as aws-lambda-test
#Mention all the required loggroups in the array at line 18
#Provide the s3 bukcet name in line 29
#Make sure you choose the lambda timout value basedon the number of loggroups to be included
import boto3
import json
import collections
from datetime import datetime, timedelta
import math
import time

cw_logs = boto3.client('logs')
def lambda_handler(event, context):
    export_log_duration = 1
    export_log_date = datetime.now() - timedelta(days=export_log_duration)
    print (deletionDate)
    startofday = export_log_date.replace(hour=0, minute=0, second=0, microsecond=0)
    endofday = export_log_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    log_groups = ['']  #mention all loggroups to be exported
    for log_group in log_groups:
        prefix = log_group.replace("/", "-")
        prefix = prefix[1:]
        print(prefix)
        response = cw_logs.create_export_task(
            taskName='export_task',
            logGroupName=x,
            fromTime=math.floor(startofday.timestamp() * 1000), 
            to=math.floor(endofday.timestamp() * 1000), 
            destination='your-bucket-name',
            destinationPrefix=prefix
        )
        time.sleep(10)  #this is needed as to not force the exports to exceed the limit
