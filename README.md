# AWS EC2 Find Instances

## Description
List all EC2 instances from  regions in an AWS account. Filter for instance_state and Tag  

## Runtime
Python 3.6  

## Inputs
None  

## Outputs  
Result object list of all regions with instances matching filters  

## AWS Dependencies  
IAM Permissions Required:  
  - ec2:DescribeInstances
  - ec2:DescribeRegions
