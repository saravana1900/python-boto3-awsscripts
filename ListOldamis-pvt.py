import boto3
import botocore
from datetime import datetime
import time

amis_in_use = []
unique_amis = []
regions = ['us-east-1','us-west-2','ca-central-1','eu-west-1']

for region in regions:
    client = boto3.client('ec2',region_name=region)
    instances = client.describe_instances()
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            amis_in_use.append(instance['ImageId'])
    


    unique_amis = set(amis_in_use)
    
    
    custom_images=client.describe_images(

                                        Filters=[
                                            {
                                            'Name': 'state',
                                            'Values': ['available',]
                                            },
                                            ],
                                        Owners=['self',],

                                        )

    custom_amis_list = []

    for image in custom_images['Images']:

        ami_creation_date_str = image['CreationDate']
        ami_creation_date = datetime.strptime(ami_creation_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        current_date=datetime.now().date()
        ami_age=current_date-ami_creation_date.date()

        if ami_age.days > 123 :
            custom_amis_list.append(image['ImageId'] +' ' + image['Name'])

        print ("REGION == > " +region)
        
        for custom_ami in custom_amis_list:
            if custom_ami not in amis_in_use:
                print ("To be Deregistered == >> {}".format(custom_ami))