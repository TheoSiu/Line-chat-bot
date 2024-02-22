from linebot import LineBotApi, WebhookHandler
import os
import requests
from linebot.models import *
import schedule
import time

# lineToken = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
lineToken ='3L+VeuaSQtYyvdEfP8/NT9UuRCJWkgpM6i81WxF++6cppQTmfrdI7cQhQXcsRdwkno7qOFGnsyoxy8I8d3gtRV9uonV2IDnId49TqbZXgCVEPRMSDbYKhiUA1a3gVTprDzfXumuY6VolHDmIEO+MJgdB04t89/1O/w1cDnyilFU='
# handler = WebhookHandler(os.environ["CHANNEL_SECRET"])

temp = 'hello'

def sendToLine(token):
    url = "https://notify-api.line.me/api/notify"
    payload = {"message": {temp}}
    headers = {"Authorization": "Bearer " + lineToken}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

# sendToLine(lineToken)


line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
    
user_id = 'U4a3faf91de8aee80b1412e462ae9807e'  # 用户的 Line ID

def send_notification():
    message = TextSendMessage(text='定时通知：獨孤無敵')
    line_bot_api.push_message(user_id, messages=message)

# 设置定时任务，每天的特定时间触发
# schedule.every().day.at("16:58").do(send_notification)
schedule.every(5).minutes.do(send_notification)

while True:
    schedule.run_pending()
    time.sleep(60)