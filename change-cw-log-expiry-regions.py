#This funciton will set a retention period for all loggroups
#retention value is passed via lambda environment variable "retention"
#Make sure the lambda function is having enough permissions to execute this
#Please note, this will change expiry for all log groups
import boto3
import os

session = boto3.Session()
client = session.client('ec2')

def lambda_handler(event, context):
  #default_region = os.environ.get('AWS_REGION', 'us-east-1')
  #retain_days = int(os.environ.get('RETAIN_DAYS', '30'))
  log_retention = int(os.environ['retention'])
  for region_dict in client.describe_regions()['Regions']:
    region = region_dict['RegionName']
    print('Region:', region)
    logs = boto3.client('logs', region_name=region)
    #adding paginator incase there are more than 50 log groups
    paginator = logs.get_paginator('describe_log_groups')
    itenator = paginator.paginate()
    #counter for number of log groups
    log_group_count = 0
    for page in itenator:
      print("**** page****")
      for log_group in page['logGroups']:
        log_group_name = log_group['logGroupName']
        log_group_count = log_group_count + 1
        if 'retentionInDays' in log_group:
          print(region, log_group_name, log_group['retentionInDays'], 'days') 
          print("retention already exists for the log group:", log_group_name)
        else:
          print("there is not retention exists for the log group", log_group_name)        
          response = logs.put_retention_policy(
              logGroupName=log_group_name,
              retentionInDays=log_retention
          )
          print("changed the log group retention for the log group", log_group_name)
    print("total no of groups evaluated -- ", log_group_count)
  return 'CloudWatchLogRetention.Success'