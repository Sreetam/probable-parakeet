import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

rss_list = pd.read_csv('raw_rss_list.csv')

goodlinks = []
for rss in rss_list['rss-url']:
  try:
    for i in range(5):
      r = requests.get(rss, timeout=0.5)
      if r.status_code==200:
        break
    soupContent = BeautifulSoup(r.content,features='xml')
    items = soupContent.findAll('item')
    if r.status_code==200 and len(items)!=0:
      print('Total News Content: ' + str(len(items)) + ' : Success: ' + str(r.status_code) + ' : ' + rss)
      goodlinks.append(rss)
    else:
      print('Total News Content: 0 : Fail: ' + str(r.status_code) + ' : ' + rss)
  except:
    print('Total News Content: 0 : Fail: 404 : ' + rss)

rss_list.loc[rss_list['rss-url'].isin(goodlinks)].to_csv('rss.csv', index=False, quoting=csv.QUOTE_ALL)