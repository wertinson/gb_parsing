import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient


client = MongoClient('localhost', 27017)

db = client['news']
news_lenta = db.news_lenta

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"}

response = requests.get('https://lenta.ru/', headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//a[contains(@class, 'card-mini')]")

items_list = []
id = 0
for item in items:
    item_info = {}

    title = item.xpath(".//span[contains(@class, 'card-mini__title')]/text()")
    link = item.xpath("./@href")
    time = item.xpath(".//time[contains(@class, 'card-mini__date')]/text()")

    item_info['site'] = "lenta.ru"
    item_info['title'] = title
    item_info['link'] = link
    item_info['time'] = time

    items_list.append(item_info)

    id += 1
    news_lenta.insert_one({
        "_id": id
        , "site": item_info['site']
        , "title": item_info['title']
        , "link": item_info['link']
        , "time": item_info['time']
    })


pprint(items_list)