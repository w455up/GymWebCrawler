import time
from datetime import datetime, time as dt_time
import openpyxl
import requests
from bs4 import BeautifulSoup
import pytz
def job():
    wb = openpyxl.load_workbook('test.xlsx')
    ws = wb.active

    url = 'http://www.tssc.tw/'
    web = requests.get('http://www.tssc.tw/')
    soup = BeautifulSoup(web.text, "html.parser")
    number = soup.find_all('span', class_='number-current')
    peo = number[1].text
    current_time = datetime.now(pytz.timezone('Asia/Taipei')).strftime('%m-%d')
    date = datetime.now().strftime('%H:%M')
    weekday = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    weekofday = weekday[datetime.now(pytz.timezone('Asia/Taipei')).weekday()]

    url2 = 'https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0001-001?Authorization=CWA-AC5922D2-E03C-4C0D-9818-42B17D48DF87&downloadType=WEB&format=JSON'
    data = requests.get(url2)
    data_json = data.json()
    location = data_json['cwaopendata']['dataset']['Station']
    dictionary = {}
    for i in location:
        name = i['StationName']                    # 測站地點
        city = i['GeoInfo']['CountyName']  # 城市
        area = i['GeoInfo']['TownName']  # 行政區
        temp = i['WeatherElement']['AirTemperature']
        weather = i['WeatherElement']['Weather']
        msg = f'{temp}度, 天氣{weather}'
        try:
            dictionary[city][name]=msg   # 記錄地區和描述
        except:
            dictionary[city] = {}        # 如果每個縣市不是字典，建立第二層字典
            dictionary[city][name]=msg   # 記錄地區和描述

    ws.append([peo, date, current_time, weekofday, dictionary['新北市']['淡水觀海']])
    wb.save('test.xlsx') 
    print(f"已執行一次任務{datetime.now(pytz.timezone('Asia/Taipei')).strftime('%H:%M')}")

job()
