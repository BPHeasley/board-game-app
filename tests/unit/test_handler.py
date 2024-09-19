# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import os
import boto3
import uuid
import pytest
from moto import mock_dynamodb
from contextlib import contextmanager
from unittest.mock import patch

MOCK_BOARD_GAME_TABLE_NAME = 'MockBoardGames'
MOCK_BOARD_GAME_TITLE = 'unit-test-title'
MOCK_BOARD_GAME_TITLE_2 = 'unit-test-title-2'


def mock_game():
    return MOCK_BOARD_GAME_TITLE


@contextmanager
def my_test_environment():
    with mock_dynamodb():
        set_up_dynamodb()
        put_data_dynamodb()
        yield


def set_up_dynamodb():
    conn = boto3.client(
        'dynamodb'
    )
    conn.create_table(
        TableName=MOCK_BOARD_GAME_TABLE_NAME,
        KeySchema=[
            {'AttributeName': 'title', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'title', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )


def put_data_dynamodb():
    conn = boto3.client(
        'dynamodb'
    )
    conn.put_item(
        TableName=MOCK_BOARD_GAME_TABLE_NAME,
        Item={
            'title': {'S': MOCK_BOARD_GAME_TITLE}
        }
    )
    conn.put_item(
        TableName=MOCK_BOARD_GAME_TABLE_NAME,
        Item={
            'title': {'S': MOCK_BOARD_GAME_TITLE_2}
        }
    )


@patch.dict(os.environ, {'TABLE_NAME': MOCK_BOARD_GAME_TABLE_NAME, 'AWS_XRAY_CONTEXT_MISSING': 'LOG_ERROR'})
def test_get_list_of_board_games():
    with my_test_environment():
        from src.api.board_game import get
        with open('./events/event-get-all-board-games.json', 'r') as f:
            apigw_get_all_board_games_event = json.load(f)
        expected_response = [
            {
                'title': MOCK_BOARD_GAME_TITLE,
            },
            {
                'title': MOCK_BOARD_GAME_TITLE_2,
            }
        ]
        ret = get.get_all_board_games.lambda_handler(apigw_get_all_board_games_event, '')
        assert ret['statusCode'] == 200
        data = json.loads(ret['body'])
        assert data == expected_response


def test_get_single_board_game():
    with my_test_environment():
        from src.api.board_game import get
        with open('./events/event-get-board-game-by-title.json', 'r') as f:
            apigw_event = json.load(f)
        expected_response = {
            'title': MOCK_BOARD_GAME_TITLE
        }
        ret = get.get_board_game.lambda_handler(apigw_event, '')
        assert ret['statusCode'] == 200
        data = json.loads(ret['body'])
        assert data == expected_response


def test_get_single_board_game_wrong_title():
    with my_test_environment():
        from src.api.board_game import get
        with open('./events/event-get-board-game-by-title.json', 'r') as f:
            apigw_event = json.load(f)
        apigw_event['pathParameters']['title'] = 'wrong-title'
        apigw_event['rawPath'] = '/boardgames/wrong-title'
        ret = get.get_board_game.lambda_handler(apigw_event, '')
        assert ret['statusCode'] == 404
        assert json.loads(ret['body']) == {}


# @patch('uuid.uuid1', mock_uuid)
# @pytest.mark.freeze_time('2001-01-01')
def test_add_board_game():
    with my_test_environment():
        from src.api.board_game import add
        with open('./events/event-add-board-game.json', 'r') as f:
            apigw_event = json.load(f)
        expected_response = json.loads(apigw_event['body'])
        ret = add.add_board_game.lambda_handler(apigw_event, '')
        assert ret['statusCode'] == 200
        data = json.loads(ret['body'])
        assert data['title'] == MOCK_BOARD_GAME_TITLE


# def test_delete_board_game():
#     with my_test_environment():
#         from src.api.board_game import delete
#         with open('./events/event-delete-user-by-id.json', 'r') as f:
#             apigw_event = json.load(f)
#         ret = delete.delete_board_game.lambda_handler(apigw_event, '')
#         assert ret['statusCode'] == 200
#         assert json.loads(ret['body']) == {}
