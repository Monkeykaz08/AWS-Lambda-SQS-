import json
import boto3
import os

# SQS クライアントを作成
sqs = boto3.client("sqs")

# 環境変数で SQS URL を指定
#https://sqs.ap-northeast-1.amazonaws.com/812063490714/MyQueue
QUEUE_URL = os.environ["QUEUE_URL"]

def lambda_handler(event, context):
    try:
        # API Gateway からのイベントには body が文字列で入る
        body = json.loads(event["body"])

        # 受け取った JSON を SQS に投入
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(body, ensure_ascii=False)
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Message sent to SQS",
                "messageId": response["MessageId"]
            }, ensure_ascii=False)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            }, ensure_ascii=False)
        }
