# Created by Samuel Chalvet at 3/22/21
# Email: SamuelChalvet@gmail.com
from os import getenv
import boto3
import json


def handler(event, context):

    if event.get("body"):   # check if the API call has a body
        data = json.loads(event.get('body'))      # load the body as a json
        return {
            'body': json.dumps(add_user(data))   # return the results from our dynamo transaction
        }
    else:
        return {
            'body': "Missing body!"
        }


def add_user(data):
    table_name = getenv('tableName')
    client_dynamo_db = boto3.client('dynamodb')
    try:
        return client_dynamo_db.put_item(
            TableName=table_name,
            Item={
                    "userEmail": {'S': data.get("email")},
                    "name": {'S': data.get("name")},
                    "age": {'S':  str(data.get("age"))},
                    "phone": {'S': data.get("phone")}
                }
            )
    except Exception as e:
        return {'error': str(e)}

