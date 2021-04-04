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
            'body': json.dumps(get_user(email))   # return the results from our dynamo transaction
        }
    else:
        return {
            'body': "User email is a required PATH parameter ex: get_user/foo@bar.com"
        }


def get_user(email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(getenv('tableName'))
    try:
        response = table.get_item(Key={'userEmail': email})

        if response.get('Item') is None:
            return {'error': "No item found matching that key"}
        else:
            return response.get('Item')

    except ClientError as e:
        return {'error': str(e.response['Error']['Message'])}


