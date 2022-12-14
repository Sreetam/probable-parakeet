import requests
from bs4 import BeautifulSoup
import pandas as pd
from dateutil.parser import parse
import time
import re
import csv
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer


from warnings import filterwarnings
filterwarnings("ignore")
class Scraper:
    def __init__(self) -> None:
        self.path = '/home/sr'
        self.interests = ['general', 'politics']
        self.countries = ['US', 'IN']
        self.rss = None
        self.rss_links = []
        self.breaking_news = []
        self.news = []
        self.breaking_news_schema = ['pubDate', 'timestamp', 'title', 'description', 'img']
        self.news_schema = ['pubDate', 'timestamp', 'title', 'description', 'link', 'rss-url', 'img', 'country', 'category']
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
    def get_rss(self, verbose=False, write=False, from_file=False):
        self.rss_links = []
        if from_file==True:
            self.rss = pd.read_csv(self.path + '/probable-parakeet/data/rss.csv')
            self.rss_links = list(self.rss['rss-url'])
            return self.rss_links
        rss_list = pd.read_csv(self.path + '/probable-parakeet/data/raw_rss_list.csv')
        rss_list = rss_list.loc[rss_list.category.isin(self.interests)]
        rss_list = rss_list.loc[rss_list.country.isin(self.countries)]
        for rss in rss_list['rss-url']:
            try:
                for i in range(5):
                    r = requests.get(rss, timeout=1)
                    if r.status_code==200:
                        break
                soupContent = BeautifulSoup(r.content,features='xml')
                items = soupContent.findAll('item')
                if r.status_code==200 and len(items)!=0:
                    if verbose==True:
                        print('Total News Content: ' + str(len(items)) + ' : Success: ' + str(r.status_code) + ' : ' + rss)
                    self.rss_links.append(rss)
                else:
                    if verbose==True:
                        print('Total News Content: 0 : Fail: ' + str(r.status_code) + ' : ' + rss)
            except:
                if verbose==True:
                    print('Total News Content: 0 : Fail: 404 : ' + rss)
        self.rss = rss_list.loc[rss_list['rss-url'].isin(self.rss_links)].copy()
        if write==True:
            self.rss.to_csv(self.path + '/probable-parakeet/data/rss.csv', index=False, quoting=csv.QUOTE_ALL)
        return self.rss_links
    def breaking(self, from_file=False, write=False, verbose=False, mins=15):
        self.breaking_news = []
        if from_file==True:
            self.breaking_news = [list(i) for i in pd.read_csv(self.path + "/probable-parakeet/data/breaking.csv").values]
            return self.breaking_news
        for rss in self.rss_links:
            try:
                r = requests.get(rss, timeout=0.4)
                soupContent = BeautifulSoup(r.content,features='xml')
                items = soupContent.findAll('item')
                if r.status_code==200 and len(items)!=0:
                    if verbose==True:
                        print('\x1b[2K\rTotal News Content: ' + str(len(items)) + ' : Success: ' + str(r.status_code) + " : " + rss, end="")
                else:
                    if verbose==True:
                        print('\x1b[2K\rTotal News Content: 0 : Fail: ' + str(r.status_code) + ' : ' + rss, end="")
                    continue
            except:
                if verbose==True:
                    print('\x1b[2K\rTotal News Content: 0 : Fail: 404 : ' + rss, end="")
                continue
            for i in items:
                article = []
                try:
                    date = parse(re.sub("<.+?>", " ", i.find('pubDate').text).strip(), fuzzy=True)
                    stamp = date.timestamp()
                    if stamp>=time.time() - mins*60:
                        article.append(date.strftime('%d-%m-%Y %H:%M:%S %Z'))
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
                except:
                    continue
                try:
                    description = i.find('description').text
                    description = re.sub("<.+?>", " ", description)
                    description = re.sub("&nbsp;", " ", description)
                    description = re.sub("[\n ]+", " ", description).strip()
                    article.append(description)
                except:
                    continue
                try:
                    article.append(i.thumbnail['url'])
                except:
                    try:
                        article.append(i.content['url'])
                    except:
                        try:
                            article.append(i.image.text)
                        except:
                            article.append("")
                self.breaking_news.append(article)
        if write==True:
            news = pd.DataFrame(self.breaking_news, columns=self.breaking_news_schema).drop_duplicates().dropna()
            news = news.sort_values(by='timestamp', ascending=False)
            news.to_csv(self.path + '/probable-parakeet/data/breaking.csv', index=False, quoting=csv.QUOTE_ALL)
            news.to_json(self.path + '/probable-parakeet/src/data/breaking.json', orient="split", indent=4)
        return self.breaking_news
    def get_news(self, from_file=False, write=False, verbose=False, mins=15):
        self.news = []
        if from_file==True:
            self.news = [list(i) for i in pd.read_csv(self.path + "/probable-parakeet/data/news.csv").values]
            return self.news
        for rss_index in self.rss.index:
            rss = self.rss['rss-url'][rss_index]
            try:
                for i in range(5):
                    r = requests.get(rss, timeout=0.5)
                    if r.status_code==200:
                        break
                soupContent = BeautifulSoup(r.content,features='xml')
                items = soupContent.findAll('item')
                if r.status_code==200 and len(items)!=0:
                    if verbose==True:
                        print('\x1b[2K\rTotal News Content: ' + str(len(items)) + ' : Success: ' + str(r.status_code) + " : " + rss, end="")
                else:
                    if verbose==True:
                        print('\x1b[2K\rTotal News Content: 0 : Fail: ' + str(r.status_code) + ' : ' + rss, end="")
                    continue
            except:
                if verbose==True:
                    print('\x1b[2K\rTotal News Content: 0 : Fail: 404 : ' + rss, end="")
                continue
            for i in items:
                article = []
                try:
                    date = parse(re.sub("<.+?>", " ", i.find('pubDate').text).strip(), fuzzy=True)
                    stamp = date.timestamp()
                    if stamp>=time.time() - mins*60:
                        article.append(date.strftime('%d-%m-%Y %H:%M:%S'))
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
                except:
                    continue
                try:
                    description = i.find('description').text
                    description = re.sub("<.+?>", " ", description)
                    description = re.sub("&nbsp;", " ", description)
                    description = re.sub("[\n ]+", " ", description).strip()
                    article.append(description)
                except:
                    continue
                try:
                    article.append(i.find('link').text.strip())
                except:
                    continue
                article.append(rss)
                try:
                    article.append(i.content['url'])
                except:
                    try:
                        article.append(i.thumbnail['url'])
                    except:
                        try:
                            article.append(i.image.text)
                        except:
                            article.append("")
                article.append(self.rss['country'][rss_index])
                article.append(self.rss['category'][rss_index])
                self.news.append(article)
        if write==True:
            news = pd.DataFrame(self.news, columns=self.news_schema).drop_duplicates().dropna()
            news = news.sort_values(by='timestamp', ascending=False)
            news.to_csv(self.path + '/probable-parakeet/data/news.csv', index=False, quoting=csv.QUOTE_ALL)
            news.to_json(self.path + '/probable-parakeet/src/data/news.json', orient="split", indent=4)
        return self.news
    def pre_process(self, text):
        text = text.lower()
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)
        # Convert to list from string
        word_list = text.split()
        # remove words less than three letters
        word_list = [word for word in word_list if len(word) >= 3 and word not in self.stop_words]
        # lemmatize
        lmtzr = WordNetLemmatizer()
        lemmatized_list = [lmtzr.lemmatize(word) for word in word_list]
        viral_tags = nltk.pos_tag(lemmatized_list)
        viral = [i[0] for i in viral_tags if i[1] in ['NN','NNS', 'NNP', 'NNPS']]
        return viral