import os

import boto3

board_games_bucket = os.getenv('BOARD_GAME_BUCKET')


def lambda_handler(event, context):
    bucket_name = board_games_bucket
    file_name = 'index.html'
    file_content = 'This is the content of the file.'

    s3 = boto3.client('s3')
    s3.put_object(Body=file_content, Bucket=bucket_name, Key=file_name)
    return {
        'statusCode': 200,
        'body': 'File uploaded successfully.'
    }
