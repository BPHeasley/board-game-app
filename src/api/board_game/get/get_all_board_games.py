import boto3
import json
import os

# from aws_lambda_powertools import Logger

# logger = Logger()

dynamodb = boto3.resource('dynamodb')
board_games_table = os.getenv('TABLE_NAME')
ddbTable = dynamodb.Table(board_games_table)


def lambda_handler(event, context):
    status_code = 400  # default response
    try:
        ddb_response = ddbTable.scan(Select='ALL_ATTRIBUTES')

        if 'Items' in ddb_response:
            response_body = ddb_response['Items']
            status_code = 200
        else:
            response_body = {}
    except Exception as err:
        response_body = {'Error:': str(err)}
        status_code = 400

    return {
        'statusCode': status_code,
        'headers': {},
        'body': json.dumps(response_body)
    }
