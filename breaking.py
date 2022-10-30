import scraper
s = scraper.Scraper()
links = s.get_rss(from_file=True)
breaking = s.breaking(write=True)

# */10 * * * * /usr/bin/python3 /home/sr/probable-parakeet/breaking.py