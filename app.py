from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import datetime as dt
import requests
import json
import pandas as pd
from package import Weather
import pytz
import schedule
import time
import numpy as np

app = Flask(__name__)
# CHANNEL_ACCESS_TOKEN= "3L+VeuaSQtYyvdEfP8/NT9UuRCJWkgpM6i81WxF++6cppQTmfrdI7cQhQXcsRdwkno7qOFGnsyoxy8I8d3gtRV9uonV2IDnId49TqbZXgCVEPRMSDbYKhiUA1a3gVTprDzfXumuY6VolHDmIEO+MJgdB04t89/1O/w1cDnyilFU="
# CHANNEL_SECRET=1fee91f8ffb4152aa8a54ea04e5a05ef
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

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
    

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # 取得位置訊息
    location_message = event.message
    address = location_message.address.replace('台', '臺')
    # weath= Weather
    # now_weather = weath.Now_weather(address)
    now_weather = f"{Weather.Now_weather(address)}  \n\n{Weather.forecast(address)}"
    # print(type(address))
    # now_weather = Weather.Now_weather(address)
    # # 回傳位置信息
    # reply_message = f"您的位置是：\n緯度:{latitude}\n經度:{longitude}\n地址:{address}"
    reply_message= now_weather
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


### 收到位置訊息，傳送當前天氣 ###
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):

    # 獲得今天的日期，並轉為台灣的時區
    today = dt.datetime.today()
    taipei_tz = pytz.timezone('Asia/Taipei')
    today = today.replace(tzinfo = pytz.utc).astimezone(taipei_tz).strftime('%m-%d')
    # text_weather = notify_weather(today)
    weath= Weather
    text_weather = weath.notify_weather(today)
    print('日期:', today)
    print("Text Weather:", text_weather)  # 加入日志
    user_id = event.source.user_id
    print(f'Line API: {line_bot_api}')

    if text_weather:  # 检查消息内容是否不为空
        message = TextSendMessage(text = text_weather)
    # message = TextSendMessage(text = 'hello _ haha')
    line_bot_api.reply_message(event.reply_token, message)

    # else:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='empty data'))

user_id = 'U4a3faf91de8aee80b1412e462ae9807e'  # 用户的 Line ID

@app.route("/test_new_feature")
def test_new_feature():

    # 在這裡添加你的新功能的測試邏輯
    return "Testing the new feature!"


# def send_notification():
#     message = TextSendMessage(text='定时通知：我很棒的')
#     line_bot_api.push_message(user_id, messages=message)

# 设置定时任务，每天的特定时间触发
# schedule.every().day.at("16:58").do(send_notification)
# schedule.every(5).minutes.do(send_notification)

# while True:
#     schedule.run_pending()
#     time.sleep(60)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    # app.run(host="0.0.0.0", port=port)
