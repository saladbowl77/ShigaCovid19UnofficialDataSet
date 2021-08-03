import json #標準ライブラリ
import csv #標準ライブラリ
from os.path import join, dirname #標準ライブラリ
from datetime import datetime, timezone, timedelta

import feedparser #pip install feedparser
import requests #pip install request

from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy

from dateutil.parser import parse

import os
import pprint
import time
import urllib.error
import urllib.request

import datetime

#環境変数読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

consumer_key = getenv("TWITTER_API_KEY")
consumer_secret= getenv("TWITTER_API_SECRET")
access_key = getenv("TWITTER_ACCESS_TOKEN")
access_secret = getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

tweetMessages = []
tweetMessagesImg = []

def download_file(url, file_name):
    import requests

    response = requests.get(url)
    image = response.content

    with open(file_name, "wb") as aaa:
        aaa.write(image)

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

today=datetime.date.today() 
oneday=datetime.timedelta(days=1) 
yesterday=today-oneday

tweetText = '昨日' + str(yesterday.month) + '/' + str(yesterday.day) +'の滋賀県コロナ情報まとめ 1\n\n'\
    + '陽性者数の内訳と陽性確認者数推移カレンダー、サイト開設から現在までの推移を表示しています。\n\n'\
    + '#滋賀県 #コロナ #滋賀県コロナ #コロナウィルス\n\n'\
    + '詳しく見たい方はこちら↓\n'\
    + 'https://stopcovid19-shiga.jp'
print(tweetText)

for downloadImg in ["dataWrapTop_div","covid","bed_used","bed_count","admission_rate","pcr","pcr2","graphTransition","GenGraphWap","OldGraphWap","covid19DataTable","covid2WeekCalendar"]:
    url = 'https://stopcovid19-shiga.jp/twitterCard/top/' + downloadImg + '.png'
    dst_path = join(dirname(__file__), 'tmp/' + downloadImg + '.png')
    download_file(url, dst_path)

media_ids = []
for image in [join(dirname(__file__), 'tmp/dataWrapTop_div.png'),join(dirname(__file__), 'tmp/covid.png'),join(dirname(__file__), 'tmp/covid2WeekCalendar.png'),join(dirname(__file__), 'tmp/graphTransition.png')]:
    img = api.media_upload(image)
    media_ids.append(img.media_id)

my_status = api.update_status(status = tweetText, media_ids = media_ids)

tweetText = '昨日' + str(yesterday.month) + '/' + str(yesterday.day) +'の滋賀県コロナ情報まとめ 2\n\n'\
    + '昨日のPCR検査の情報や病床入院数に関する情報です。\n'\
    + '#滋賀県 #コロナ #滋賀県コロナ #コロナウィルス\n'\
    + '詳しく見たい方はこちら↓\n'\
    + 'https://stopcovid19-shiga.jp'

media_ids = []
for image in [join(dirname(__file__), 'tmp/bed_count.png'),join(dirname(__file__), 'tmp/bed_used.png'),join(dirname(__file__), 'tmp/admission_rate.png'),join(dirname(__file__), 'tmp/pcr.png')]:
    img = api.media_upload(image)
    media_ids.append(img.media_id)

my_status = api.update_status(status = tweetText,in_reply_to_status_id = my_status.id, media_ids = media_ids)
