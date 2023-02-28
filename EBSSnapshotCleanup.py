import boto3
import botocore
import datetime

regions = ['us-east-1','us-west-2','ca-central-1','eu-west-1']


for region in regions:
    client = boto3.client('ec2',region_name=region)
    snapshots = client.describe_snapshots(OwnerIds=['self'])
    print ("\nListing Snapshots in region :: " +region)

    for snapshot in snapshots['Snapshots']:
            snapshot_start_time=snapshot['StartTime'] #a
            #print(a)
            snapshot_creation_date=snapshot_start_time.date()  #b
            current_date=datetime.datetime.now().date()  #c
            snapshot_age=current_date-snapshot_creation_date #d

            try:
                 if snapshot_age.days >= 365 :
                   id = snapshot['SnapshotId']
                   #des = snapshot['Description']
                   print ("\nListing SnapshotId =====>>>>" +id)
                   client.delete_snapshot(SnapshotId=id)

            except botocore.exceptions.ClientError as e:
                    error_code = e.response['Error']['Code']

                    if error_code != "None":
                      print ("Response :" +error_code)
                      #print(id)
                      #print(des)
                      continue