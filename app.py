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
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, URIAction
from io import BytesIO


app = Flask(__name__)
token= "3L+VeuaSQtYyvdEfP8/NT9UuRCJWkgpM6i81WxF++6cppQTmfrdI7cQhQXcsRdwkno7qOFGnsyoxy8I8d3gtRV9uonV2IDnId49TqbZXgCVEPRMSDbYKhiUA1a3gVTprDzfXumuY6VolHDmIEO+MJgdB04t89/1O/w1cDnyilFU="
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
    
### 收到位置訊息，傳送當前天氣 ###
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    # 取得位置訊息
    location_message = event.message
    address = location_message.address.replace('台', '臺')
    reply_message = f"{Weather.Now_weather(address)}  \n\n{Weather.forecast(address)}"
    # # 回傳位置信息
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text= event.message.text
    if text == '天氣資訊':

        message = TextSendMessage(text = '請分享位置資訊')
        line_bot_api.reply_message(event.reply_token, message)

    if text == '今日運勢':

        message = TextSendMessage(text = '請輸入星座名稱')
        line_bot_api.reply_message(event.reply_token, message)

    for con in Weather.Total_Con:
        if text in con:
            print(text, '==================')
            reply_message = Weather.Horoscope(text)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請點擊選單，獲取資訊'))

    # else:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text='empty data'))

# user_id = 'U4a3faf91de8aee80b1412e462ae9807e'  # 用户的 Line ID

# 創建 RichMenu
rich_menu_to_create_1 = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=False,
    name="Nice richmenu",
    chat_bar_text="開啟選單",
    areas=[
        # 左半部
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1250, height=1686),
            action=MessageAction(label='Left', text='天氣資訊')
            # action={'type': 'message', 'label': 'Left', 'text': 'Left Menu'}
        ),
        # 右半部
        RichMenuArea(
            bounds=RichMenuBounds(x=1251, y=0, width=1250, height=1686),
            action=MessageAction(label='Right', text='今日運勢')
        ),
    ]
)

# # 上傳豐富菜單圖片
# with open("https://i.imgur.com/srvVVsd.jpeg", "rb") as f:

#     rich_menu_id_1 = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create_1)
#     line_bot_api.set_rich_menu_image(rich_menu_id_1, "image/jpeg", f)
# line_bot_api.set_default_rich_menu(rich_menu_id_1)

url = "https://i.imgur.com/srvVVsd.jpeg"
response = requests.get(url)

# 確認回應狀態碼
if response.status_code == 200:
    # 將圖片的二進制數據轉換為 BytesIO 對象
    image_data = BytesIO(response.content)
    
    # 創建 Line Bot 選單
    rich_menu_id_1 = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create_1)
    
    # 設置選單背景圖片
    line_bot_api.set_rich_menu_image(rich_menu_id_1, "image/jpeg", image_data)
    
    # 設置預設的 Line Bot 選單
    line_bot_api.set_default_rich_menu(rich_menu_id_1)
# else:
#     print("無法從 URL 獲取圖片")
# imgur_image_url = "https://imgur.com/a/Bqq1lI8"
# response = requests.get(imgur_image_url)

# 確認回應狀態碼
# if response.status_code == 200:
#     # 將圖片作為二進制數據寫入暫存檔
#     with open("temp_image.jpg", "wb") as f:
#         f.write(response.content)

#     # 設置 Line Bot 選單背景圖片
#     # rich_menu_id_1 = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create_1)
#     with open("temp_image.jpg", "rb") as f:
#         rich_menu_id_1 = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create_1)
#         line_bot_api.set_rich_menu_image(rich_menu_id_1, "image/jpeg", f)
    
#     # 設置預設的 Line Bot 選單
#     line_bot_api.set_default_rich_menu(rich_menu_id_1)

#     # 刪除暫存檔
#     import os
#     os.remove("temp_image.jpg")
# else:
#     print("Failed to download the image.")

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    # app.run(host="0.0.0.0", port=port)
