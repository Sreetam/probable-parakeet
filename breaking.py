import requests
from bs4 import BeautifulSoup
import pandas as pd
from dateutil.parser import parse
import time
import re
import csv

from warnings import filterwarnings
import sys
filterwarnings("ignore")

mins = 15
articles = []
rss_list = pd.read_csv('./rss/rss.csv')

for rss in rss_list['rss-url']:
  try:
    r = requests.get(rss, timeout=0.4)
    soupContent = BeautifulSoup(r.content,features='xml')
    items = soupContent.findAll('item')
    if r.status_code==200 and len(items)!=0:
      print('\x1b[2K\rTotal News Content: ' + str(len(items)) + ' : Success: ' + str(r.status_code) + " : " + rss, end="")
    else:
      print('\x1b[2K\rTotal News Content: 0 : Fail: ' + str(r.status_code) + ' : ' + rss, end="")
      continue
  except:
    print('\x1b[2K\rTotal News Content: 0 : Fail: 404 : ' + rss, end="")
    continue
  for i in items:
    article = []
    try:
      date = parse(re.sub("<.+?>", " ", i.find('pubDate').text).strip(), fuzzy=True)
      stamp = date.timestamp()
      if stamp>=time.time() - mins*60:
        article.append(date)
        article.append(stamp)
      else:
        continue
    except:
       continue
    try:
      title = i.find('title').text
      title = re.sub("<.+?>", " ", title)
      title = re.sub("&nbsp;", " ", title)
      title = re.sub("[\n ]+", " ", title).strip()
      article.append(title)
    except: continue
    try:
      description = i.find('description').text
      description = re.sub("<.+?>", " ", description)
      description = re.sub("&nbsp;", " ", description)
      description = re.sub("[\n ]+", " ", description).strip()
      article.append(description)
    except: continue
    articles.append(article)
left_col = ['pubDate', 'timestamp', 'title', 'description']
news = pd.DataFrame(articles, columns=left_col).drop_duplicates().dropna()
news = news.sort_values(by='timestamp', ascending=False)

news.to_csv('./news/breaking.csv', index=False, quoting=csv.QUOTE_ALL)
print("\x1b[2K\rSucces : News Line Length : "+str(len(articles)))