import datetime
import requests
import json
import csv
import os
import sys
import pandas as pd
import pathlib

# 取得したい情報の設定
url = "https://api.syosetu.com/novelapi/api/"
ncode = ['N8459GK','N0611EM','N3976GK','N1517GM']
ncodes = ('-'.join(ncode))
payload = {'out': 'json', 'ncode': ncodes }
now_date = datetime.date.today().strftime("%Y/%m/%d")
now_time = datetime.datetime.now().strftime("%H:%M:%S")

# APIへアクセス
r = requests.get(url, params=payload)
x = r.json()


datas = []
datas.extend(x[1:])

for d in datas:
    data = pd.DataFrame({
        '総合評価ポイント': [d['global_point']],
        '日間ポイント': [d['daily_point']],
        '週間ポイント': [d['weekly_point']],
        '月間ポイント': [d['monthly_point']],
        '四半期ポイント': [d['quarter_point']],
        '年間ポイント': [d['yearly_point']],
        '話数': [d['general_all_no']],
        '文字数': [d['length']],
        'ブックマーク数': [d['fav_novel_cnt']],
        '感想数': [d['impression_cnt']],
        'レビュー数': [d['review_cnt']], 
        '評価ポイント': [d['all_point']],
        '評価者数': [d['all_hyoka_cnt']],
        '会話率': [d['kaiwaritu']],
        '小説の更新日時': [d['novelupdated_at']]}, index=[now_date])
    
    file_path = '/usr/src/app/'
    # file_path = '/Users/makidaisuke/Desktop/Cron/python-cron/'

    if  os.path.exists(file_path + 'novel/' + d['title'] + '.csv'):
        data.to_csv(file_path + d['title'] + '.csv', header=False, mode='a', encoding='utf-16')
    else:
        pathlib.Path(file_path + d['title'] + '.csv').touch()
        data.to_csv(file_path + d['title'] + '.csv', encoding='utf-16')
        print('完了1/2 「新規作成」')

print('完了1/2 ')

# デイリーポイント
payload_daily = {'out': 'json', 'order': 'dailypoint', 'biggenre': '2', 'of': 't-g-l-its-iti-izk-nu'}
r_daily = requests.get(url, params=payload_daily)
x_daily = r_daily.json()

daily_all_datas = []
daily_all_datas.extend(x_daily[1:])

title = 0
genre = 0
length = 0
iszankoku = 0
istensei = 0
istenni = 0
    
    
for d in daily_all_datas:
    title = title + (len(d['title']))
    genre = genre + d['genre']
    length = length + d['length']
    iszankoku = iszankoku + d['iszankoku']
    istensei = istensei + d['istensei']
    istenni = istenni + d['istenni']

# 平均値
n = len(daily_all_datas)
title = title / n
genre = genre / n
length = length / n
iszankoku = iszankoku / n
istensei = istensei / n
istenni = istenni / n

df = pd.DataFrame({
    'タイトル': [title],
    'ジャンル': [genre],
    '文字数': [length],
    '残酷': [iszankoku],
    '転生': [istensei],
    '転移': [istenni]}, index=[now_date])

df.to_csv(file_path + 'novel.csv', header=False, mode='a', encoding='utf-16')

print('完了2/2 ')
print(now_date, now_time)
