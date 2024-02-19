from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import datetime as dt
import requests
import json
import pandas as pd

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



def notify_weather(today):
    
    ## 設定天氣網站的 API 與查詢的城市
    weather_API = "c78bc673af3701bbd7ac6ccf5f595b9e"
    city = 'Taipei'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_API}'
    
    ## 爬取天氣網站的資訊
    r = requests.get(url)
    data = json.loads(r.text)
    coll = {}
    
    ## 篩選所要的部分資訊
    for foresct in data['list']:
        time= dt.datetime.fromtimestamp(foresct['dt']).strftime('%m-%d %H:%M')
        if time.startswith(today):
            clock = dt.datetime.fromtimestamp(foresct['dt']).strftime('%H:%M')
            temp = round(foresct['main']['temp'] - 273.15 , 1)
            feel_temp = round(foresct['main']['feels_like'] - 273.15 , 1)
            coll[clock] = (temp, feel_temp)
        else:
            break

    selected_times = ['08:00', '14:00', '17:00', '20:00']
    foresct_temp = pd.DataFrame(coll ).T 
    foresct_temp.columns = ['目前溫度' , '體感溫度']
    foresct_temp = foresct_temp.loc[selected_times]
    return foresct_temp


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    today= dt.datetime.today().strftime('%m-%d')

    message = TextSendMessage(text= notify_weather(today))
    line_bot_api.reply_message(event.reply_token, message)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
