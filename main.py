import os
import json
import http.client


def lambda_handler(event, context):
    print(f"FunctionHandler received: {event}")
    issue_url = event["issue"]["html_url"]
    print(f"Issue: {issue_url}")

    payload = json.dumps({"text": f"Issue Created: {issue_url}"})

    slack_url = os.environ.get("SLACK_URL")
    # https://docs.python.org/3/library/http.client.html
    url_parts = slack_url.split("://")
    host_path = url_parts[1].split("/", 1)
    host = host_path[0]
    if len(host_path > 1):
        path = "/" + host_path[1]
    else:
        path = "/"

    conn = http.client.HTTPSConnection(host)
    headers = {"Content-type": "application/json"}

    conn.request("POST", path, payload, headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")

    print(f"Response status: {response.status}")
    print(f"Response reason: {response.reason}")
    print(f"Response data: {response.data}")
    return {"statusCode": response.status, "body": data}

    # print("Event")
    # print(event)
    # print("context")
    # print(context)
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Return from Lambda')
    # }
