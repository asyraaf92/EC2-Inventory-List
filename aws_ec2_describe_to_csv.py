#!/usr/bin/env python3
import argparse
import boto3
import csv

def describe_instances_to_csv(output_file):
    region_name = 'ap-southeast-1'
    ec2 = boto3.client('ec2', region_name=region_name)
    response = ec2.describe_instances()

    # Open the output file for writing in CSV format
    with open(output_file, mode='w', newline='') as csv_file:
        fieldnames = ['Instance ID', 'Tag Name', 'Availability Zone', 'Platform Details', 'Instance Type', 'State', 'VPC ID', 'Private IP Address', 'Public IP Address']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Extract the fields for each instance object in the response and write to the CSV file
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                tags = instance.get('Tags', [])
                tag_name = None
                for tag in tags:
                    if tag['Key'] == 'Name':
                        tag_name = tag['Value']
                        break
                availability_zone = instance['Placement']['AvailabilityZone']
                platform_details = instance['PlatformDetails']
                instance_type = instance['InstanceType']
                state = instance['State']['Name']
                vpc_id = instance['VpcId']
                private_ip_address = instance['PrivateIpAddress']
                public_ip_address = instance.get('PublicIpAddress', 'N/A')
                
                # Write the extracted values to the CSV file
                writer.writerow({
                    'Instance ID': instance_id,
                    'Tag Name': tag_name,
                    'Availability Zone': availability_zone,
                    'Platform Details': platform_details,
                    'Instance Type': instance_type,
                    'State': state,
                    'VPC ID': vpc_id,
                    'Private IP Address': private_ip_address,
                    'Public IP Address': public_ip_address
                })

if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Script to describe EC2 instances and output to CSV.')
    parser.add_argument('--output', dest='output_file', default='output.csv', help='Output CSV filename')
    args = parser.parse_args()

    # Call the function to describe instances and output to CSV
    describe_instances_to_csv(args.output_file)
