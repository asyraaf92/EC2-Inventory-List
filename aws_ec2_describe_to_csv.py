import argparse
import boto3
import csv
from datetime import datetime, timedelta

def get_cpu_utilization(instance_id, region):
    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch', region_name=region)

    # Set the metric dimensions and period
    dimensions = [
        {
            'Name': 'InstanceId',
            'Value': instance_id
        },
    ]
    period = 300

    # Set the start and end times for the metric data
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)

    # Retrieve the CPU utilization metric data
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'cpu',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': 'CPUUtilization',
                        'Dimensions': dimensions
                    },
                    'Period': period,
                    'Stat': 'Average'
                },
                'ReturnData': True
            },
        ],
        StartTime=start_time,
        EndTime=end_time
    )

    # Calculate the average CPU utilization and return the result
    values = response['MetricDataResults'][0]['Values']
    if len(values) > 0:
        average = sum(values) / len(values)
        return '{:.2f}%'.format(round(average, 2))
    else:
        return 'N/A'


def describe_instances_to_csv(output_file):
    region_name = 'ap-southeast-1'
    ec2 = boto3.client('ec2', region_name=region_name)
    response = ec2.describe_instances()

    # Open the output file for writing in CSV format
    with open(output_file, mode='w', newline='') as csv_file:
        fieldnames = ['Instance ID', 'Instance Name', 'Availability Zone', 'Platform Details', 'Instance Type', 'State', 'VPC ID', 'Private IP Address', 'Public IP Address', 'CPU Utilization']
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
                cpu_utilization = get_cpu_utilization(instance_id, region_name)
                
                # Write the extracted values to the CSV file
                writer.writerow({
                    'Instance ID': instance_id,
                    'Instance Name': tag_name,
                    'Availability Zone': availability_zone,
                    'Platform Details': platform_details,
                    'Instance Type': instance_type,
                    'State': state,
                    'VPC ID': vpc_id,
                    'Private IP Address': private_ip_address,
                    'Public IP Address': public_ip_address,
                    'CPU Utilization': cpu_utilization
                })
                
def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Describe EC2 instances and write to a CSV file.')
    parser.add_argument('--output', metavar='output_file', type=str, default='output.csv', help='the output file name in CSV format')
    args = parser.parse_args()

    # Run the EC2 describe instances command and write to the output file
    describe_instances_to_csv(args.output)

if __name__ == '__main__':
    main()

