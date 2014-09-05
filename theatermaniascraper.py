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
	title =  d['feed']['title']
	print d['feed']['link']
	print d.feed.subtitle
	length = len(d['entries'])
	print len(d['entries'])
	print "______________       _ _________   ___________    ___"

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
			# c.execute("""INSERT INTO OutsideContent(title, publication, link, descript, author, published) 
			# 		  VALUES(%s,%s,%s,%s,%s, %s)""", 
			# 		  (d['entries'][entry]['title'], d['feed']['link'], link, desc,author,date))
			# print d['entries'][entry]['title'] 
			print link
			print desc
			print author
			print date
			print "_____________________________________"
			data = urllib2.urlopen(link)
			data = data.read()
			c.execute("SELECT id from OutsideContent where link = %s", (link,))
			articleID = c.fetchall()[0][0]
			
			c.execute("SELECT id, name from Fringeshows")
			shows = c.fetchall()
			print shows
			for show in shows:
			 	showid = show[0]
			 	name = show[1]
			 	print showid
			 	print name
			 	if name in data: 
			 		c.execute("INSERT INTO contentconnection(articleid, showid) VALUES(%s,%s)", (articleID, showid))
			conn.commit()



