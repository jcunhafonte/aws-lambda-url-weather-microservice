import json
from router import Router


def home(event, **kargs):
    print({"statusCode": 200, "body": json.dumps({"message": f"home!"})})
    return {"statusCode": 200, "body": json.dumps({"message": f"home!"})}


def weather(**kwargs):
    print({"statusCode": 200, "body": json.dumps({"message": "hello unknown!"})})
    print(kwargs)
    return {"statusCode": 200, "body": json.dumps({"message": "hello unknown!"})}


def solar_radiation(**kwargs):
    print({"statusCode": 200, "body": json.dumps({"message": "hello unknown!"})})
    return {"statusCode": 200, "body": json.dumps({"message": "hello unknown!"})}


router = Router()
router.set(path="/", method="GET", handler=home)
router.set(path="/weather", method="GET", handler=weather)
router.set(path="/solar_radiation", method="GET", handler=solar_radiation)


def lambda_handler(event, context):
    path = event["requestContext"]["http"]["path"]
    method = event["requestContext"]["http"]["method"]
    query_string = event["queryStringParameters"]
    func = router.get(path=path, method=method)
    return func(event=event)


if __name__ == "__main__":
    event = {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/my/path",
        "rawQueryString": "",
        "cookies": [],
        "headers": {
        },
        "queryStringParameters": {
        },
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "<urlid>",
            "authentication": None,
            "authorizer": {
                "iam": {
                }
            },
            "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
            "domainPrefix": "<url-id>",
            "http": {
                "method": "GET",
                "path": "/",
                "protocol": "HTTP/1.1",
                "sourceIp": "123.123.123.123",
                "userAgent": "agent"
            },
            "requestId": "id",
            "routeKey": "$default",
            "stage": "$default",
            "time": "12/Mar/2020:19:03:58 +0000",
            "timeEpoch": 1583348638390
        },
        "body": "Hello from client!",
        "pathParameters": None,
        "isBase64Encoded": False,
        "stageVariables": None
    }

    lambda_handler(event, None)