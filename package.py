import datetime as dt
import requests
import json
import pandas as pd

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
            time = dt.datetime.fromtimestamp(foresct['dt']).strftime('%m-%d %H:%M')
            if time.startswith(today):
                clock = dt.datetime.fromtimestamp(foresct['dt']).strftime('%H:%M')
                temp = round(foresct['main']['temp'] - 273.15, 1)
                feel_temp = round(foresct['main']['feels_like'] - 273.15, 1)
                foresct_temp[clock] = (temp, feel_temp)
            else:
                break

        selected_times = ['08:00', '14:00', '17:00', '20:00']
        text_weather = '\n'.join([f"{time}: 溫度 {temp}°C, 體感溫度 {feel_temp}°C" for time, (temp, feel_temp) in foresct_temp.items()])
        print('test success or not', text_weather)
        return text_weather

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        return 'HTTP Error'
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        return 'Connection Error'
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        return 'Timeout Error'
    except requests.exceptions.RequestException as err:
        print(f"Other Request Error: {err}")
        return 'Other Request Error'
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return 'Unexpected Error'