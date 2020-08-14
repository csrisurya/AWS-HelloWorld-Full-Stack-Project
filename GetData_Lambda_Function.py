# This is the lambda function that returns text to the client using AWS Amplify and puts text into the Dyamo Database in AWS 

# import the json utility package since we will be working with a JSON object
import json
# import the AWS SDK (for Python the package name is boto3)
import boto3

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
table = dynamodb.Table('HelloWorldDatabase')



# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
# extract values from the event object we got from the Lambda service and store in a variable and check if the database has values
    message = ""
    code = 200
    name = event['firstName']+' '+event['lastName']
    response = table.get_item(
        Key={
            'ID': name
            })  

    if 'Item' not in response:
        message = "This name does not exist in the database"
        code = 404
        raise Exception("Nope")

    else:  
        count = response['Item']['SubmissionFrequency']   
        message = "This name has been submitted " + str(count) + " time(s)"
            
    # return a properly formatted JSON object
    return {    
        'statusCode': code,
        'body': json.dumps(message)
    }