import os
import boto3

import json

dynamodb = boto3.resource('dynamodb')
board_games_table = os.getenv('TABLE_NAME')
ddbTable = dynamodb.Table(board_games_table)


def lambda_handler(event, context):
    status_code = 400  # default response
    try:
        title = event['pathParameters']['title']
        ddb_response = ddbTable.get_item(
            Key={
                'title': title
            }
        )

        if 'Item' in ddb_response:
            delete_ddb_response = ddbTable.delete_item(
                Key={
                    'title': title
                }
            )
            response_body = f"{title} was removed from db"
        else:
            response_body = f"{title} was not in db"

    except Exception as e:
        response_body = str(e)

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response_body)
    }
