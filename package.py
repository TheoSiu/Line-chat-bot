import datetime as dt
import requests
import json
import pandas as pd
import pytz 
import numpy as np

class Weather:
    # weather_API = "c78bc673af3701bbd7ac6ccf5f595b9e"
    weather_API = 'CWA-6F6F89AE-BC6D-4644-BCDB-47912927DE5A'
    json_api = {
            "宜蘭縣": "F-D0047-001", "桃園市": "F-D0047-005", "新竹縣": "F-D0047-009", "苗栗縣": "F-D0047-013",
            "彰化縣": "F-D0047-017", "南投縣": "F-D0047-021", "雲林縣": "F-D0047-025", "嘉義縣": "F-D0047-029",
            "屏東縣": "F-D0047-033", "臺東縣": "F-D0047-037", "花蓮縣": "F-D0047-041", "澎湖縣": "F-D0047-045",
            "基隆市": "F-D0047-049", "新竹市": "F-D0047-053", "嘉義市": "F-D0047-057", "臺北市": "F-D0047-061",
            "高雄市": "F-D0047-065", "新北市": "F-D0047-069", "臺中市": "F-D0047-073", "臺南市": "F-D0047-077",
            "連江縣": "F-D0047-081", "金門縣": "F-D0047-085"
        }


    @classmethod
    def notify_weather(cls, today):
        weather_API = "c78bc673af3701bbd7ac6ccf5f595b9e"
        city = 'Taipei'
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={cls.weather_API}'

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
        

    @classmethod
    def Now_weather(cls, address):
        weather_url =f'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization={cls.weather_API}&downloadType=WEB&format=JSON'

        ## 取得天氣即時資料 ##
        weather= requests.get(weather_url)
        weather_json = weather.json()
        weather_json
        weath_loc = weather_json['cwaopendata']['dataset']['Station']#[0]['GeoInfo']#['CountyName']
        found= False
        
        ## 篩選本地區的天氣資料
        for loc in weath_loc:
            if loc['GeoInfo']['TownName'] in address:
                found= True
                return (f"{loc['GeoInfo']['CountyName']} {loc['GeoInfo']['TownName']}\n"
                        f"當前溫度: {loc['WeatherElement']['AirTemperature']}°C \n"
                        f"降雨量: {loc['WeatherElement']['Now']['Precipitation']}mm"
                        )

        ## 若本地區無資料，用同個縣市的天氣資料取平均
        if not found:
            coll_temp = []
            coll_rain = []
            county_name = None

            for loc in weath_loc:
                if loc['GeoInfo']['CountyName'] in address:
                    county_name = loc['GeoInfo']['CountyName']
                    
                    coll_temp.append(float(loc['WeatherElement']['AirTemperature']))
                    coll_rain.append(float(loc['WeatherElement']['Now']['Precipitation']))
                    break
            if county_name is not None:
                
                return (f"{county_name}\n"
                        f"當前溫度: {round(np.mean(coll_temp), 1)}°C \n"
                        f"降雨量: {round(np.mean(coll_rain), 1)}"
                        )
            
            else:
                return "未找到天氣資料"
            
    @classmethod
    def forecast(cls, address):
        for code in cls.json_api:
            if code in address:
                print(code, cls.json_api[code])
                local_code = cls.json_api[code]
                
        url_local = f'https://opendata.cwa.gov.tw/api/v1/rest/datastore/{local_code}?Authorization={cls.weather_API}&elementName=WeatherDescription'
        weather_for= requests.get(url_local)
        weather_for= weather_for.json()
        condition = False
        now= dt.datetime.today()
        msg = ''
        for local in weather_for['records']['locations'][0]['location']:
            if local ['locationName'] in address:

                condition = False
                for time in local['weatherElement'][0]['time']:
                    start_str = time['startTime']
                    end_str = time['endTime']
                    start_time = dt.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
                    end_time = dt.datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
                    if condition:
                        msg = f"未來時段天氣預報: \n{time['elementValue'][0]['value']}"
                        break
                    if (start_time <= now <= end_time) or (now < start_time and now < end_time):
                        condition = False
                        
                    if now < start_time and now < end_time:
                        msg = f"未來時段天氣預報: \n{time['elementValue'][0]['value']}"
                        break
        
        return msg