import json

def lambda_handler(event, context):
    print("Received event:", event)
    # return {
    #     "statusCode": 400,
    #     "body": json.dumps(event, ensure_ascii=False)  # ← dictをJSON文字列に変換
    # }

    # GETクエリパラメータを取得
    params = event.get("queryStringParameters") or {}

    print("params:",params)

    try:
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

    return {
        "statusCode": 200,
        "body": json.dumps({
            "投資額": 投資額,
            "年金利": 年金利,
            "経過年数": 経過年数,
            "将来価値": round(将来価値, 2)
        }, ensure_ascii=False)
    }
