#This function will list all EIPs owned/assigned to this account + any dynamic public IPs attached to instances
#Note--- Please change the default timout period for the lambda function to atleast 3 mins

import json
import boto3

session = boto3.Session()
client = session.client('ec2')

def lambda_handler(event, context):
    eip_list = []
    ec2_pubip = []
    for region_dict in client.describe_regions()['Regions']:
        region = region_dict['RegionName']
        print('Region', region)
        client_region = session.client('ec2', region)
        reservations = client_region.describe_instances().get('Reservations', [])
        for reservation in reservations:
            for instance in reservation['Instances']:
                if instance[u'State'][u'Name'] == 'running' and instance.get(u'PublicIpAddress') is not None:
                    ipaddress = instance.get(u'PublicIpAddress')
                    #print(ipaddress)
                    ec2_pubip.append(ipaddress)
        addresses_dict = client_region.describe_addresses()
        for eip_dict in addresses_dict['Addresses']:
            #print(eip_dict['PublicIp'])
            eip_list.append(eip_dict['PublicIp'])
    #print(eip_list)
    #print("Ips from EC2")
    #print(ec2_pubip)
    public_ipaddresses = eip_list + ec2_pubip
    print(public_ipaddresses)
    public_ipaddresses = list(dict.fromkeys(public_ipaddresses))
    print(public_ipaddresses)