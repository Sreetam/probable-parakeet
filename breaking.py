import requests
from bs4 import BeautifulSoup
import pandas as pd
from dateutil.parser import parse
import time
import re
import csv

mins = 15
articles = []
rss_list = pd.read_csv('./rss/rss.csv')

for rss in rss_list['rss-url']:
  try:
    for i in range(2):
      r = requests.get(rss, timeout=0.4)
      if r.status_code==200:
        break
    soupContent = BeautifulSoup(r.content,features='xml')
    items = soupContent.findAll('item')
    if r.status_code==200 and len(items)!=0:
      print('Total News Content: ' + str(len(items)) + ' : Success: ' + str(r.status_code) + " : " + rss)
    else:
      print('Total News Content: 0 : Fail: ' + str(r.status_code) + ' : ' + rss)
      continue
  except:
    print('Total News Content: 0 : Fail: 404 : ' + rss)
    continue
  for i in items:
    article = []
    try:
      date = re.sub("<.+?>", " ", i.find('pubDate').text).strip()
      stamp = parse(date, fuzzy=True).timestamp()
      if stamp>=time.time() - mins*60:
        article.append(date)
        article.append(stamp)
      else:
        continue
    except:
       continue
    try: article.append(re.sub("<.+?>", " ", i.find('title').text).strip())
    except: continue
    try: article.append(re.sub("<.+?>", " ", i.find('description').text).strip())
    except: continue
    articles.append(article)
left_col = ['pubDate', 'timestamp', 'title', 'description']
news = pd.DataFrame(articles, columns=left_col).drop_duplicates().dropna()
news = news.sort_values(by='timestamp', ascending=False)

news.to_csv('./news/breaking.csv', index=False, quoting=csv.QUOTE_ALL)