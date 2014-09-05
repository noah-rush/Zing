from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras
import feedparser

conn=connectionBoiler.get_conn()
c=conn.cursor()

target_urls = ["http://www.theatermania.com/rss.xml/",
 			   "http://www.broadstreetreview.com/rss", 
 			   "http://phindie.com/feed/", 
 			   "http://citypaper.net/rss/arts/", 
			   "http://feeds.feedburner.com/ShapiroOnTheater", 
 			   "http://feeds.feedburner.com/PW-ArtsCulture"]
for target in target_urls:
	print "\n\n\n\n"
	d = feedparser.parse(target)
	link =  d['feed']['link']
	print link
	##c.execute("INSERT INTO reviewTags(pic, ")