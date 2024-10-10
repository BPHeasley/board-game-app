import boto3
import json
import os

from python.boto3.dynamodb.conditions import Key

from aws_lambda_powertools import Logger

logger = Logger()

dynamodb = boto3.resource('dynamodb',  region_name='us-east-1')
board_games_table = os.getenv('TABLE_NAME')
ddbTable = dynamodb.Table(board_games_table)


def lambda_handler(event, context):
    status_code = 400  # default response
    try:
        title = event['pathParameters']['title']
        logger.info(title)
        ddb_response = ddbTable.query(
            KeyConditionExpression=Key('title').eq(title)
        )

        logger.info(ddb_response)

        if 'Items' in ddb_response:
            response_body = ddb_response['Items']
            status_code = 200
        else:
            status_code = 404
            response_body = {}
    except Exception as err:
        response_body = {'Error:': str(err)}
        logger.info(response_body)

    return {
        'statusCode': status_code,
        'headers': {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET"
        },
        'body': json.dumps(response_body)
    }
