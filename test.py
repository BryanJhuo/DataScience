import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
import calendar

def month_calendar(chinese_year, month):
    year = chinese_year + 1911
    calendar.setfirstweekday(6)
    date = str(calendar.month(year, month))
    day = date[38:].strip().replace('\n', ' ')
    day = day.replace('  ',' ').split(' ')
    return {month : day}

yearOfDay = []
for i in range(1, 13, 1):
    yearOfDay.append(month_calendar(112, i))

data = pd.DataFrame()
for dict in yearOfDay:
    for key, value in dict.items():
        for day in value:
            if int(day) < 10: day = "0" + day
            if key < 10: 
                date = "2023-" + "0" + str(key) + "-" + day
            else : 
                date = "2023-" + str(key) + "-" + day
            print(date + "\n--------")

            url = f'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={date.replace('-', '')}&type=ALLBUT0999'
            req = requests.get(url)
            reqJson = req.json()
            if reqJson['stat'] == 'OK':
                stock = pd.DataFrame(reqJson['data9'], columns = reqJson['fields9'])
                stock['date'] = date 
                data = pd.concat([data, stock])
        time.sleep(5)

data.to_csv('../DataScience/stock_data_2023.csv')