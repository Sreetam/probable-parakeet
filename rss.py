import scraper
s = scraper.Scraper()
links = s.get_rss(write=True)

# 1 */2 * * * /usr/bin/python3 /home/sr/probable-parakeet/rss.py