# test_lambda_mock.py
import json
from lambda_function import lambda_handler
from moto import mock_aws
import boto3

@mock_aws
def test_sqs_event():
    # モックS3作成
    s3 = boto3.client("s3", region_name="ap-northeast-1")
    # s3.create_bucket(Bucket="galaxy-sg-001")

    # 擬似SQSイベント
    for i in range(30):
        
        #投資番号をiを利用して生成　Tから始まる５桁で
        InvestmentNo = f"X{str(i).zfill(3)}"
        sqs_event = {
            "Records": [
                {
                    "eventSource": "aws:sqs",
                    "body": json.dumps({
                    "投資番号": InvestmentNo,
                    "投資額": 150000,
                    "年金利": 0.04,
                    "経過年数": 9
                }, ensure_ascii=False)
                }
            ]
        }
        
            
        res = lambda_handler(sqs_event, None)
        print(json.dumps(res, ensure_ascii=False, indent=2))            


    # モックS3から内容確認
    # obj = s3.get_object(Bucket="galaxy-sg-001", Key="results/T003.json")
    # print("S3 Saved Content:", obj["Body"].read().decode("utf-8"))
    
    

if __name__ == "__main__":
    test_sqs_event()
