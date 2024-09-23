import os

import boto3

import json

dynamodb = boto3.resource('dynamodb')
board_games_table = os.getenv('TABLE_NAME')
ddbTable = dynamodb.Table(board_games_table)


def lambda_handler(event, context):
    status_code = 400  # default response
    try:
        ddb_response = ddbTable.delete_item(
            Key={
                'title': event['pathParameters']['title']
            }
        )

        if 'Item' in ddb_response:
            response_body = ddb_response['Item']
            status_code = 200
        else:
            response_body = "Item not found"
    except Exception as e:
        response_body = str(e)

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response_body)
    }
