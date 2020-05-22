#This funtion is to enable unlimited CPU mode on instances filtered based on tags
#example: t2 normal t2 unlimited
#1.Filter instances based a unique tag -- unlimitedcpu:on
#2.Fetch cpucredit status and change to unlimited if the status is standard

import boto3
import os

ec2 = boto3.resource('ec2')
ec = boto3.client('ec2')

def lambda_handler(event, context):
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag:unlimitedcpu', 'Values': ['on']},
            { 'Name': 'instance-state-name','Values': ['running'] }
        ]
        ).get(
        'Reservations', []
    )
    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], []
    )
    instance_ids = []
    for instance in instances:
        #print(instance)
        #print(instance['InstanceId'])
        instance_ids.append(instance['InstanceId'])
    print(instance_ids)
    
    cpucreditstaus = ec.describe_instance_credit_specifications(InstanceIds=instance_ids)
    cpu_specs = cpucreditstaus['InstanceCreditSpecifications']
    for cpu_spec in cpu_specs:
        inst_id = cpu_spec['InstanceId']
        cpu_cred = cpu_spec['CpuCredits']
        #print(inst_id)
        #print(cpu_cred)
        if cpu_cred is 'unlimited':
            continue
        else:
            response = ec.modify_instance_credit_specification(
            InstanceCreditSpecifications=[
                {
                    'InstanceId': inst_id,
                    'CpuCredits': 'unlimited'
                },
            ]
            )
            print(response)
    
    #cpucreditstaus = ec.describe_instance_credit_specifications(InstanceIds=instance_ids)
    #print(cpucreditstaus)
