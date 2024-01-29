# import schedule
import time
from datetime import datetime, time as dt_time
import openpyxl
import requests
from bs4 import BeautifulSoup

def job():
    wb = openpyxl.load_workbook(r'C:\Users\user\Desktop\爬蟲\test.xlsx')
    ws = wb.active

    url = 'http://www.tssc.tw/'
    web = requests.get('http://www.tssc.tw/')
    soup = BeautifulSoup(web.text, "html.parser")
    number = soup.find_all('span', class_='number-current')
    peo = number[1].text
    current_time = datetime.now().strftime('%m-%d')
    date = datetime.now().strftime('%H:%M')
    weekday = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    weekofday = weekday[datetime.now().weekday()]

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
    wb.save(r'C:\Users\user\Desktop\爬蟲\test.xlsx') 
    # 这里写你要运行的程序或函数
    print(f"已執行一次任務{datetime.now().strftime('%H:%M')}")

job()
# # 设置每天的定时时间（24小时制）
# schedule.every(30).minutes.do(job)
# # 可以设置多个定时任务，如下
# # schedule.every().day.at("12:00").do(another_job)

# # 让程序一直运行，直到手动终止
# start_time = dt_time(6, 30)
# end_time = dt_time(21, 30)
# print(schedule.get_jobs())
# # 让程序一直运行，每分钟检查一次是否有任务需要执行
# while True:
#     Now = datetime.now().time()
    
#     # 检查当前时间是否在指定的时间范围内
#     if start_time <= Now <= end_time:
#         schedule.run_pending()
    
#     elif input("输入 'quit' 即中止程序：").lower() == 'quit':
#         print("程序终止。")
#         schedule.clear()
#         break
        
#     else:
#         pass
#     time.sleep(1)  # 每分钟检查一次是否有任务需要执行
