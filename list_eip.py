#This function will list all EIPs from all region for this account, please note this will list only EIPs owned/assigned to this account
#but not any dynamic public IPs attached to instances
#Note--- Please change the default timout period for the lambda function to atleast 3 mins

import json
import json
import boto3

session = boto3.Session()
client = session.client('ec2')

def lambda_handler(event, context):
    for region_dict in client.describe_regions()['Regions']:
        region = region_dict['RegionName']
        print('Region', region)
        client_region = session.client('ec2', region)
        addresses_dict = client_region.describe_addresses()
        for eip_dict in addresses_dict['Addresses']:
            print(eip_dict['PublicIp'])
