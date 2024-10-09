import boto3
import json
import os

# from aws_lambda_powertools import Logger

# logger = Logger()

dynamodb = boto3.resource('dynamodb',  region_name='us-east-1')
board_games_table = os.getenv('TABLE_NAME')


def add_board_game(event: dict):
    # logger.info("Adding a new board game")
    board_game_detail = json.loads(event['body'])
    board_game_title = board_game_detail['title']

    ddb_item = {
        'title': board_game_title,
        'data': {
            'title': board_game_title,
        }
    }
    table = dynamodb.Table(board_games_table)

    table.put_item(Item=ddb_item, ConditionExpression='attribute_not_exists(title)')

    # logger.info(f"Added board game {board_game_title}")

    return board_game_detail


def lambda_handler(event, context):
    try:
        board_game_detail = add_board_game(event=event)
        response = {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(board_game_detail)
        }
        return response
    except Exception as err:
        raise
