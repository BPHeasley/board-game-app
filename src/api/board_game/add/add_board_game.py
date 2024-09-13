import boto3
import json

from aws_lambda_powertools import Logger

logger = Logger()

dynamodb = boto3.resource('dynamodb')

def add_board_game(event: dict):
    logger.info("Adding a new board game")
    board_game_detail = json.loads(event['body'])
    board_game_title = board_game_detail['title']

    ddb_item = {
        'title':  board_game_title,
        'data': {
            'title': board_game_title,
        }
    }
    table = dynamodb.Table('BoardGamesTable')

    table.put_item(Item=ddb_item, ConditionExpression='attribute_not_exists(title)')

    logger.info(f"Added board game {board_game_title}")

    return board_game_detail

def lambda_handler(event):
    try:
        board_game_detail = add_board_game(event=event)
        response = {
            "statusCode": 200,
            "headers": {},
            "body": json.dumps(board_game_detail)
        }
        return response
    except Exception as err:
        raise