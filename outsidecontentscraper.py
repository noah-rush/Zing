from xlrd import open_workbook
from xlwt import Workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras
import feedparser

conn=connectionBoiler.get_conn()
c=conn.cursor()

book = Workbook()
sheet1 = book.add_sheet('Outside Articles')
sheet1.write(0,0,'id')
sheet1.write(0,1,'publication')
sheet1.write(0,2,'title')
sheet1.write(0,3,'author')
sheet1.write(0,4,'description')
sheet1.write(0,5,'link')
sheet1.write(0,6,'published')

target_urls = ["http://www.theatermania.com/rss.xml/",
 			   "http://www.broadstreetreview.com/rss", 
 			   "http://phindie.com/feed/", 
 			   "http://citypaper.net/rss/arts/", 
			   "http://feeds.feedburner.com/ShapiroOnTheater", 
 			   "http://feeds.feedburner.com/PW-ArtsCulture"]


# target_urls = ["http://feeds.feedburner.com/PW-ArtsCulture"]
###phindie is using tags /// citypaper is only scanning from article content //// 



counter = 1
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
		if 'pubdate' in d.entries[entry]:
			date = d.entries[entry]['dc:date']
		else: 
			date = "unspecified"
		link = d.entries[entry]['link']
		desc = d.entries[entry]['description']
		if title =="TheaterMania.com":
			if "phil" in link:
				print d['entries'][entry]['title'] 
				print link
		else:
			c.execute("""INSERT INTO ZingOutsideContent(title, publication, link, descript, author, published) 
				  VALUES(%s,%s,%s,%s,%s, %s)""", 
					  (d['entries'][entry]['title'], d['feed']['link'], link, desc,author,date))
			print d['entries'][entry]['title'] 
			
			print link
			print desc
			print author
			print date
			print "_____________________________________"
			data = urllib2.urlopen(link)
			data = data.read()
			c.execute("SELECT id from ZingOutsideContent where link = %s", (link,))
			articleID = c.fetchall()[0][0]
			
			c.execute("SELECT id, name from Zingshows")
			shows = c.fetchall()
			print shows
			counter = counter + 1
			showcounter = 0
			if d['feed']['link'] == 'http://phindie.com':
			 		elements = len(d.entries[entry])
			 		tags = d.entries[entry]['tags']
			 		for i in tags:
			 			print i['term']
			for show in shows:
			 	showid = show[0]
			 	name = show[1]
			 	if d['feed']['link'] == 'http://citypaper.net':
			 		data = data[data.find("<!-- Content -->"):]
			 		data = data[:data.find("<!-- Social -->")]
			 	if d['feed']['link'] == 'http://www.philadelphiaweekly.com/arts-and-culture':
			 		data = data[data.find("<!-- BEGIN EDITORIAL COPY -->"):]
			 		data = data[:data.find("<!-- END EDITORIAL COPY -->")]
			 		
				if d['feed']['link'] == 'http://bsr2.dev/index.php':
					data = data[data.find("<section>"):]
			 		data = data[:data.find("</section")]
			 	if d['feed']['link'] == 'http://www.newsworks.org/':
					data = data[data.find("articleBody"):]
			 		data = data[:data.find("</article>")]

			 	if d['feed']['link'] == 'http://phindie.com':
			 		elements = len(d.entries[entry])
			 		tags = d.entries[entry]['tags']
			 		for i in tags:
			 			if i['term'] == name:
			 				c.execute("INSERT INTO ZingOutsideShowTags(articleid, showid) VALUES(%s,%s)", (articleID, showid))
			 	else:
			 		if name in data: 
			 			print showid
			 			print name
			 			c.execute("INSERT INTO ZingOutsideShowTags(articleid, showid) VALUES(%s,%s)", (articleID, showid))
			 			sheet1.write(counter,7+showcounter,name)
			 			showcounter = showcounter +1
			sheet1.write(counter,0,'id')
			sheet1.write(counter,1,d['feed']['link'])
			sheet1.write(counter,2,d['entries'][entry]['title'])
			sheet1.write(counter,3,author)
			sheet1.write(counter,4,desc)
			sheet1.write(counter,5,link)
			sheet1.write(counter,6,date)
			conn.commit()

book.save('outsideArticles.xls')