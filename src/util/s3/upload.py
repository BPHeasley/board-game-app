import os
import boto3

board_games_bucket = os.getenv('BUCKET_NAME')


def lambda_handler(event, context):
    file_name = 'index.html'
    file_content = 'This is the content of the file.'

    s3 = boto3.client('s3')
    s3.put_object(Body=file_content, Bucket=board_games_bucket, Key=file_name)
    return {
        'statusCode': 200,
        'body': 'File uploaded successfully.'
    }
