import requests
from bs4 import BeautifulSoup
import pandas as pd

rss_link_set_websites = [
    'https://edition.cnn.com/services/rss/',
    'https://edition.cnn.com/services/rss/index.html',
    'https://money.cnn.com/services/rss/',
    'https://www.bbc.co.uk/news/10628494',
    'https://bengali.abplive.com/rss',
    'https://about.fb.com/wp-content/uploads/2016/05/rss-urls-1.pdf',
    'https://www.thehindu.com/rssfeeds/'
]
rss_links = set()
for site in rss_link_set_websites:
  r = requests.get(site)
  soupContent = BeautifulSoup(r.content)
  print(site + ': Success: ', r.status_code)
  items = soupContent.findAll('a', href=True)
  for i in items:
    if '.rss' in i['href'] and '?' not in i['href']:
      rss_links.add(i['href'])