import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from dateutil.parser import parse
import time
import re
import re
import nltk
import pke
import csv

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus.reader import wordlist

stop_words = set(stopwords.words('english'))

mins = 60 * 24
articles = []
rss_list = pd.read_csv('https://raw.githubusercontent.com/Sreetam/probable-parakeet/main/rss.csv')
interests = ['general', 'politics']
countries = ['US', 'IN', 'GB']

rss_list = rss_list.loc[rss_list.category.isin(interests)]
rss_list = rss_list.loc[rss_list.country.isin(countries)]

for rss in rss_list['rss-url']:
  try:
    for i in range(5):
      r = requests.get(rss, timeout=0.5)
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
      date = i.find('pubDate').text
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
    try: article.append(i.find('link').text.strip())
    except: continue
    article.append(rss)
    articles.append(article)
col = ['pubDate', 'timestamp', 'title', 'description', 'link', 'rss-url']
news = pd.DataFrame(articles, columns=col).drop_duplicates().dropna()
news = news.sort_values(by='timestamp', ascending=False)
news = pd.merge(news, rss_list, how='inner', on='rss-url')
col = news.columns

def pre_process(text):
  text = text.lower()
  text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
  # remove special characters and digits
  text=re.sub("(\\d|\\W)+"," ",text)
  # Convert to list from string
  word_list = text.split()
  # remove words less than three letters
  word_list = [word for word in word_list if len(word) >= 3 and word not in stop_words]
  # lemmatize
  lmtzr = WordNetLemmatizer()
  lemmatized_list = [lmtzr.lemmatize(word) for word in word_list]
  viral_tags = nltk.pos_tag(lemmatized_list)
  viral = [i[0] for i in viral_tags if i[1] in ['NN','NNS', 'NNP', 'NNPS']]
  return set(viral)

def extract(text):
  # define the set of valid Part-of-Speeches
  pos = {'NOUN', 'PROPN', 'ADJ'}
  # create a SingleRank extractor.
  try:
    extractor = pke.unsupervised.SingleRank()
    # load the content of the document.
    extractor.load_document(input=text, language='en', normalization=None)
    # select the longest sequences of nouns and adjectives as candidates.
    extractor.candidate_selection(pos=pos)
    # weight the candidates using the sum of their word's scores that are
    # computed using random walk. In the graph, nodes are words of
    # certain part-of-speech (nouns and adjectives) that are connected if
    # they occur in a window of 10 words.
    extractor.candidate_weighting(window=10, pos=pos)
    # get the 10-highest scored candidates as keyphrases
    keyphrases = extractor.get_n_best(n=10)
    return [i[0] for i in keyphrases]
  except:
    print(text)
    return[]

news['keyphrases'] = news['description'].apply(lambda x:extract(x))
news['key_words'] = news['keyphrases'].apply(lambda x:pre_process(' '.join(x)))

news.to_csv('news.csv', index=False, quoting=csv.QUOTE_ALL)