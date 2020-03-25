#This function is to delete (stop & terminate) EC2 instances
#Pre-requisites -- all EC2 intances to be covered under this function should have a tag as follows
#Tag_Name = target_date
#Tag_value = date (in MM-DD-YYYY format)
import boto3
import collections
import datetime

ec = boto3.client('ec2', 'us-east-1')
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag:AppCluster', 'Values': ['sync-prod-us-east-1']},
            { 'Name': 'instance-state-name','Values': ['running'] }
        ]
        ).get(
        'Reservations', []
    )
    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])
    #print(instances)
    date = datetime.datetime.now()
    date_fmt = date.strftime('%m-%d-%Y')
    print("Present date and time:", date.strftime('%m-%d-%Y:%H.%m.%s'))
    for instance in instances:
        instance_id = instance['InstanceId']
        ids = []
        ids.append(instance_id)
        instance_tags = instance['Tags']
        print(instance_tags)
        try:
            if instance_tags is not None:
                for tag in instance['Tags']:
                    if tag['Key'] == "target_date":
                        deletion_date = tag['Value']
                        delete_date = time.strptime(deletion_date, "%m-%d-%Y")
        except:
            deletion_date = False
            delete_date = False
        print("Deletion date is", delete_date)
        today_time = datetime.datetime.now().strftime('%m-%d-%Y')
        today_date = time.strptime(today_time, '%m-%d-%Y')
        print("today's date is", today_date)
        
        print("Instance Name is", instance['InstanceId'])
        if delete_date < today_date:
            print("stopping instance", instance['InstanceId'])
            ec2.instances.filter(InstanceIds=ids).stop()
            print("terminating instance", instance['InstanceId'])
            ec2.instances.filter(InstanceIds=ids).terminate()

