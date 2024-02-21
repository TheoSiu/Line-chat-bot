import datetime as dt
import requests
import json
import pandas as pd
import pytz 

def notify_weather(today):
    weather_API = "c78bc673af3701bbd7ac6ccf5f595b9e"
    city = 'Taipei'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_API}'

    try:
        r = requests.get(url)
        r.raise_for_status()  # 确保请求成功，否则抛出异常
        data = r.json()  # 直接使用 .json() 将响应内容解析为 JSON 格式

        foresct_temp = {}

        for foresct in data.get('list', []):
            # 使用 UTC 時間
            utc_time = dt.datetime.utcfromtimestamp(foresct['dt'])
            
            # 將 UTC 時間轉換為台灣本地時間
            taipei_timezone = pytz.timezone('Asia/Taipei')
            taipei_time = utc_time.replace(tzinfo=pytz.utc).astimezone(taipei_timezone)
            
            time = taipei_time.strftime('%m-%d %H:%M')
            if time.startswith(today):
                clock = taipei_time.strftime('%H:%M')
                temp = round(foresct['main']['temp'] - 273.15, 1)
                feel_temp = round(foresct['main']['feels_like'] - 273.15, 1)
                foresct_temp[clock] = (temp, feel_temp)
            else:
                break

        selected_times = ['08:00', '14:00', '17:00', '20:00']

        text_weather = f'天氣預報 {today}:\n' + '\n'.join([f"{time}: 溫度 {temp}°C, 體感溫度 {feel_temp}°C" for time, (temp, feel_temp) in foresct_temp.items()])
        return text_weather
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None