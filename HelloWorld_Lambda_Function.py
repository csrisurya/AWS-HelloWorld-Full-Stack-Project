# This is the lambda function that returns text to the client using AWS Amplify and puts text into the Dyamo Database in AWS 

# import the json utility package since we will be working with a JSON object
import json
# import the AWS SDK (for Python the package name is boto3)
import boto3
# import two packages to help us with dates and date formatting
from time import gmtime, strftime

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('HelloWorldDatabase')
# store the current time in a human readable format in a variable
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())


# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):

# extract values from the event object we got from the Lambda service and store in a variable
    name = event['firstName'] +' '+ event['lastName']
    response = table.get_item(
        Key={
            'ID': name
            })  

    if 'Item' not in response:
         count = 1
    else:     
        count = response['Item']['SubmissionFrequency'] + 1     

# write name and time to the DynamoDB table using the object we instantiated and save response in a variable
    response = table.put_item(
        Item={
            'ID': name,
            'LatestGreetingTime':now,
            'SubmissionFrequency': count
            })              
    # return a properly formatted JSON object
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Surya, ' + name)
    }