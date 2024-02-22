from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import datetime as dt
import requests
import json
import pandas as pd
from package import notify_weather
import pytz
import schedule
import time

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["CHANNEL_SECRET"])


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"
    
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_id = event.source.user_id
#     # 将 user_id 存储在您的数据库或其他存储中
#     save_user_id_to_database(user_id)
#     # 其他处理消息的逻辑

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    ## 獲得今天的日期，並轉為台灣的時區
    today = dt.datetime.today()
    taipei_tz = pytz.timezone('Asia/Taipei')
    today = today.replace(tzinfo = pytz.utc).astimezone(taipei_tz).strftime('%m-%d')
    text_weather = notify_weather(today)
    print('日期:', today)
    print("Text Weather:", text_weather)  # 加入日志
    user_id = event.source.user_id
    print(user_id)
    # all_user_ids = get_all_user_ids_from_database()
    # print(all_user_ids)

    if text_weather:  # 检查消息内容是否不为空
        message = TextSendMessage(text = text_weather)
        line_bot_api.reply_message(event.reply_token, message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='empty data'))

user_id = 'U4a3faf91de8aee80b1412e462ae9807e'  # 用户的 Line ID

def send_notification():
    message = TextSendMessage(text='定时通知：这是一条定时发送的消息！')
    line_bot_api.push_message(user_id, messages=message)

# 设置定时任务，每天的特定时间触发
# schedule.every().day.at("16:58").do(send_notification)
schedule.every(5).minutes.do(send_notification)

while True:
    schedule.run_pending()
    time.sleep(1)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
