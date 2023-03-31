# AWS EC2 Describe Instances to CSV

This Python script uses the AWS SDK for Python (boto3) to describe EC2 instances in a specified AWS region and output the results in CSV format to a file.

## Requirements

- Python 3.x
- boto3 library
- argparse library (for parsing command-line arguments)

To install the required libraries, run the following command in the terminal:
```
pip install -r requirements.txt
```
## Usage

To run the script, use the following command in the terminal:

```
python aws_ec2_describe_to_csv.py [--output FILENAME]
```
The `--output` option is used to specify the output filename. If not specified, the default filename `output.csv` will be used.

The output CSV file will have the following columns:

- Instance ID
- Tag Name
- Availability Zone
- Platform Details
- Instance Type
- State
- VPC ID
- Private IP Address
- Public IP Address

## Example
To run the script and output to a file named `my_output.csv`, use the following command:

```
python aws_ec2_describe_to_csv.py --output my_output.csv
```
The output will be written to the `my_output.csv` file in the same directory as the script.
