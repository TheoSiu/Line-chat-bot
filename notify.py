from linebot import LineBotApi, WebhookHandler
import os


lineToken = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
# handler = WebhookHandler(os.environ["CHANNEL_SECRET"])

temp = 'hello'

def sendToLine(token):
    url = "https://notify-api.line.me/api/notify"
    payload = {"message": {temp}}
    headers = {"Authorization": "Bearer " + lineToken}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


sendToLine(lineToken)