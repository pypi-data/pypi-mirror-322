import boto3
import json
import os

def get_session():
    # aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    # aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region_name = os.getenv('AWS_REGION')

    session = boto3.Session(
        # aws_access_key_id=aws_access_key_id,
        # aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    return session

def sqs_deliver_message(message):
    session = get_session()
    # Create SQS client
    sqs = session.client('sqs')

    # Send message to SQS queue
    queue_url = os.getenv('AWS_SQS_URL')
    if(queue_url is None):
        # raise Exception("AWS_SQS_URL is not set in environment variables")
        raise Exception("No tengo la AWS_SQS_URL parse, pidaselo a Don Manu")
                        
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(message),
        MessageGroupId=os.getenv('AWS_SQS_MESSAGE_GROUP_ID'),
    )

    return response