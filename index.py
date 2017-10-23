# index.py
#
# Author: Ryan Russell
# Purpose: List all EC2 instances from  regions in an AWS account.
#          Filter for instance_state and Tag
# Runtime: Python 3.6
# Input: None
# Output: Result object list of all regions with instances matching filters
# Other Dependencies: IAM Permissions for:
#                        - ec2:DescribeInstances
#                        - ec2:DescribeRegions
#                  

import time, os, boto3

# Define instance states to filter by
INSTANCE_STATE = ['stopped']

# Define tag environment variable
TAG_ENV_VAR = 'EC2_TAG'

# For use with AWS Lambda
def lambda_handler(event, context):

    start = time.time() # Begin execution timer

    client = boto3.client('ec2')
    
    result = { } # Search Result Object
    response = { } # JSON object response
    response['filters'] = { } # Filter object (JSON response)
    
    # Get the region list from AWS
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    
    # Build the filter object
    ec2_filter = [{
        'Name': 'instance-state-name',
        'Values': INSTANCE_STATE
    }]
    response['filters']['instance-state-name'] = ec2_filter[0]['Values']
                
    # Look for the tag filter from the environment variables. 
    try:
        tag = os.environ[TAG_ENV_VAR]
        response['filters']['ec2_tag'] = tag
        ec2_filter.append({
            'Name': 'tag-key',
            'Values':[tag]
        })
        print('EC2_TAG: ' + tag)
    except:
        response['filters']['ec2_tag'] = None
        print('No EC2 Tag Defined. Listing all.')
    
    print('Looking for instances in all regions...')
    
    # Start search against AWS
    for i in range(0,len(regions)):
        result[regions[i]] = [ ]
        client = boto3.client('ec2',region_name=regions[i])
        instances = client.describe_instances(Filters=ec2_filter)
        
        # If instances are present in the describe_instances response
        if len(instances['Reservations']) > 0 :
            print(regions[i] + ':')
            for j in range(0,len(instances['Reservations'])):
                for k in range(0,len(instances['Reservations'][j]['Instances'])):
                    result[regions[i]].append(instances['Reservations'][j]['Instances'][k]['InstanceId'])
                    print('  ' + instances['Reservations'][j]['Instances'][k]['InstanceId'])
                    
        # If no instances found
        else:
            print(regions[i] + ': No Instances Found')
            
    print('Instance Search Complete')
    
    print('Filters: ' + str(response['filters']))
    
    #Build JSON response object
    response['instances'] = result
    response['version'] = "0.2.0"
    response['timestampGMT'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    print('Timestamp: ' + response['timestampGMT'])
    
    end = time.time() # End execution timer
    response['executionTimeSec'] = end - start
    print('Execution Time: ' + str(response['executionTimeSec']) + 's')
    
    return response # Return JSON response object
   
# For use with command line
# $ python3 <filname.py>
if __name__ == '__main__':
    lambda_handler(None,None)