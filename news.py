import scraper
s = scraper.Scraper()
links = s.get_rss(from_file=True)
news = s.get_news(write=True)

# */30 * * * * /usr/bin/python3 /home/sr/probable-parakeet/news.py