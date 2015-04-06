from xlrd import open_workbook
from xlwt import Workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras
import feedparser




def update():
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
	 			   # "http://citypaper.net/rss/arts/", 
				   "http://feeds.feedburner.com/ShapiroOnTheater", 
	 			   "http://feeds.feedburner.com/PW-ArtsCulture", 
	 			   "http://www.philly.com/phillystage.rss"]


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
			elif 'creator' in d.entries[entry]:
				author = d.entries[entry]['dc:creator']
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
				c.execute("""SELECT id from ZingOutsideContent where title = %s""",
							(d['entries'][entry]['title'],) )
				check = c.fetchall()
				if len(check) == 0:
					pwTheatre = True
					# if d['feed']['link'] == 'http://www.philadelphiaweekly.com/arts-and-culture':
					# 	testurl = link[link.rfind("/"):]
					# 	goto = "http://www.philadelphiaweekly.com/arts-and-culture/stage" + testurl
					# 	try:
					# 		handle = urllib2.urlopen(goto)
    	# 					# and open it to return a handle on the url
					# 	except urllib2.HTTPError, e:
					# 		print 'We failed with error code - %s.' % e.code
					# 		print 'We failed with error code - %s.' % urllib2.HTTPError
    	# 					if e.code == 404:
  			# 					pwTheatre = False

   					if d['feed']['link'] == 'http://www.philadelphiaweekly.com/arts-and-culture':
   						if pwTheatre:
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
							 				c.execute("SELECT id FROM ZingOutsideShowTags where articleid = %s and showid = %s", (articleID, showid))
							 				check2 = c.fetchall()
							 				if len(check2) == 0:
							 					c.execute("INSERT INTO ZingOutsideShowTags(articleid, showid) VALUES(%s,%s)", (articleID, showid))
							 	else:
							 		if name in data: 
							 			print showid
							 			print name
							 			c.execute("SELECT id FROM ZingOutsideShowTags where articleid = %s and showid = %s", (articleID, showid))
							 			check2 = c.fetchall()
							 			if len(check2) == 0:
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
						 	if d['feed']['link'] == 'http://www.philly.com/r?19=960&32=3796&7=989523&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fblogs%2Fphillystage%2F':
						 		data = data[data.find("<div class=\"article-firstGraf\""):]
						 		data = data[:data.find("<div id=\"authorInfo\">")]
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
						 			if i['term'].lower() == name.lower():
						 				c.execute("SELECT id FROM ZingOutsideShowTags where articleid = %s and showid = %s", (articleID, showid))
						 				check2 = c.fetchall()
						 				if len(check2) == 0:
						 					c.execute("INSERT INTO ZingOutsideShowTags(articleid, showid) VALUES(%s,%s)", (articleID, showid))
						 	else:
						 		if name.lower() in data.lower(): 
						 			print showid
						 			print name
						 			boldStart = data.find(name)
						 			data = data[boldStart-60:boldStart] + "<b>" + name + "</b>" + data[boldStart+len(name):boldStart+len(name)+60]
						 			print data
									c.execute("INSERT INTO SNIPPETS(articleid, snippet) VALUES(%s,%s)", (articleID, data))
						 			c.execute("SELECT id FROM ZingOutsideShowTags where articleid = %s and showid = %s", (articleID, showid))
						 			check2 = c.fetchall()
						 			if len(check2) == 0:
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
