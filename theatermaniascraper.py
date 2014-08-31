from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras
import feedparser

conn=connectionBoiler.get_conn()

target_urls = ["http://www.theatermania.com/rss.xml/",
 			   "http://www.broadstreetreview.com/rss", 
 			   "http://phindie.com/feed/", 
 			   "http://citypaper.net/rss/arts/", 
			   "http://feeds.feedburner.com/ShapiroOnTheater", 
 			   "http://feeds.feedburner.com/PW-ArtsCulture"]
for target in target_urls:
	print "\n\n\n\n"
	d = feedparser.parse(target)
	title =  d['feed']['title']
	print d['feed']['link']
	print d.feed.subtitle
	length = len(d['entries'])
	print len(d['entries'])

	for entry in range(length):
		if 'author' in d.entries[entry]:
			author = d.entries[entry]['author']
		else: 
			author = "unspecified"
		if 'pubDate' in d.entries[entry]:
			date = d.entries[entry]['pubDate']
		else: 
			date = "unspecified"
		link = d.entries[entry]['link']
		desc = d.entries[entry]['description']
		if title =="TheaterMania.com":
			if "phil" in link:
				print d['entries'][entry]['title'] 
				print link
		else:
			print d['entries'][entry]['title'] 
			print link
			print desc
			print author
			print date



