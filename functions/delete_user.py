# Created by Samuel Chalvet at 4/3/21
# Email: SamuelChalvet@gmail.com
from os import getenv
import boto3
import json
from botocore.exceptions import ClientError


def handler(event, context):

    if event.get('pathParameters') and event['pathParameters'].get('email'):
        email = event['pathParameters'].get('email')     # get the user email from the path
        return {
            'body': json.dumps(delete_user(email))   # return the results from our dynamo transaction
        }
    else:
        return {
            'body': "User email is a required PATH parameter ex: delete_user/foo@bar.com"
        }


def delete_user(email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(getenv('tableName'))
    try:
        response = table.delete_item(Key={'userEmail': email}, ReturnValues='ALL_OLD')
    except ClientError as e:
        return {'error': str(e)}
    else:
        if response.get('Attributes') is None:
            return {'error': "No item found"}
        else:
            return response

