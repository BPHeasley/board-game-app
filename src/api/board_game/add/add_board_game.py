import boto3
import json
import os

from aws_lambda_powertools import Logger

logger = Logger()

dynamodb = boto3.resource('dynamodb',  region_name='us-east-1')
board_games_table = os.getenv('TABLE_NAME')


def add_board_game(event: dict):
    logger.info("Adding a new board game")
    logger.info(event)
    board_game_details = json.loads(event['body'])
    board_game_title = board_game_details['title']
    board_game_desc = board_game_details['desc']
    board_game_players = board_game_details['players']
    board_game_winner = board_game_details['winner']

    ddb_item = {
        'title': board_game_title,
        'data': {
            'title': board_game_title,
            'desc': board_game_desc,
            'players': board_game_players,
            'winner': board_game_winner
        }
    }
    table = dynamodb.Table(board_games_table)

    table.put_item(Item=ddb_item)

    logger.info(f"Added board game {board_game_title}")

    return board_game_details


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
        raise err
