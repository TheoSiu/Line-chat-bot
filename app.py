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



# def notify_weather(today):
   
#     ## 設定天氣網站的 API 與查詢的城市
#     weather_API = "c78bc673af3701bbd7ac6ccf5f595b9e"
#     city = 'Taipei'
#     url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_API}'
    
#     ## 爬取天氣網站的資訊
#     r = requests.get(url)
#     # data = json.loads(r.text)
#     foresct_temp = {}
    
#     ## 篩選所要的部分資訊
#     try :
#         data = json.loads(r.text)
#         foresct_temp = {}
#         for foresct in data['list']:
#             time= dt.datetime.fromtimestamp(foresct['dt']).strftime('%m-%d %H:%M')
#             if time.startswith(today):
#                 clock = dt.datetime.fromtimestamp(foresct['dt']).strftime('%H:%M')
#                 temp = round(foresct['main']['temp'] - 273.15 , 1)
#                 feel_temp = round(foresct['main']['feels_like'] - 273.15 , 1)
#                 foresct_temp[clock] = (temp, feel_temp)
#             else:
#                 break
#         selected_times = ['08:00', '14:00', '17:00', '20:00']
#     # foresct_temp = pd.DataFrame(coll ).T 
#     # foresct_temp.columns = ['目前溫度' , '體感溫度']
#     # foresct_temp = foresct_temp.loc[selected_times]
#         text_weather = '\n'.join([f"{time}: 溫度 {temp}°C, 體感溫度 {feel_temp}°C" for time, (temp, feel_temp) in foresct_temp.items()])
#         print( 'test success or not', text_weather)
#         return text_weather

#     except:
#         return 'cant get the data'

    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    today= dt.datetime.today().strftime('%m-%d')
    # text_weather= notify_weather(today)
    # text_weather = '\n'.join([f"{time}: 溫度 {temp}°C, 體感溫度 {feel_temp}°C" for time, (temp, feel_temp) in foresct_temp.items()])
    # print("Text Weather:", text_weather)  # 加入日誌

    message = TextSendMessage(text= notify_weather)
    # if not message:
    print('message', message)
    if message:

        line_bot_api.reply_message(event.reply_token, message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='empty data'))


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
