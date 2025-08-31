import json
import boto3
import os
from datetime import datetime

s3 = boto3.client("s3")

def lambda_handler(event, context):
    print("Received event:", event)
    # return {
    #     "statusCode": 400,
    #     "body": json.dumps(event, ensure_ascii=False)  # ← dictをJSON文字列に変換
    # }
    # SQS イベントの場合
    if "Records" in event and event["Records"][0].get("eventSource") == "aws:sqs":
        for record in event["Records"]:
            params = json.loads(record["body"])
        # GETクエリパラメータを取得
        #params = payload.get("queryStringParameters") or {}
    
    # API Gateway イベントの場合
    elif "http" in event["requestContext"]:
        #payload = json.loads(event["body"])
        # GETクエリパラメータを取得
        params = event.get("queryStringParameters") or {}
    
    else:
        params = event
        print("Unknown event source:", event)
        
    print("params:",params)

    try:
        投資番号 = params.get("投資番号")
        投資額 = float(params.get("投資額"))
        年金利 = float(params.get("年金利"))
        経過年数 = int(params.get("経過年数"))
    except (TypeError, ValueError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "投資額, 年金利, 経過年数 は数値で指定してください"}, ensure_ascii=False)
        }

    将来価値 = 投資額 * ((1 + 年金利) ** 経過年数)

    print(将来価値)

    # 保存先のバケット名（環境変数で渡すのがベスト）
    bucket_name = "galaxy-sg-001"

    # ファイル名（タイムスタンプ付きにしてユニーク化）
    file_name = f"results/{投資番号}.json"
    print(file_name)

    # JSONをS3に保存
    result = {
            "No": 投資番号,
            "investAmount": 投資額,
            "rate": 年金利,
            "years": 経過年数,
            "NPV": round(将来価値, 2),
            "CreateDt": datetime.now().strftime('%Y%m%d_%H%M%S')
        }
    
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(result, ensure_ascii=False),
        ContentType="application/json"
    )
    
    return {
        "statusCode": 200,
        "body": result
    }
    
#     # ファイルから JSON 読み込み
# with open("API.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# print(data)

# lambda_handler(data, None)