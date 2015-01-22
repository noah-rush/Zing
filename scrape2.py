
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras

conn=connectionBoiler.get_conn()

target_urls = ["http://www.theatrephiladelphia.org/calendar",
			 "http://www.theatrephiladelphia.org/calendar?page=1",
			 "http://www.theatrephiladelphia.org/calendar?page=2",
			]
c = conn.cursor()


show = ""
venue = ""
address = ""
producer = ""
description = ""
image = ""
running = ""
startdate = ""
endate = ""
for target in target_urls:
	data = urllib2.urlopen(target) # it's a file like object and works just like a file
	print "\n\n\n\n"
	for line in data: # files are iterable
		if "event" in line and "field-content" in line and not("More Details" in line)and not("Slideshow_feature" in line): 
			c.execute("SELECT id from fringeshows where name = %s", (show,))
			results = c.fetchall()
			imagefirst = image.find("<a")
			imagelast = image.find("imagecache")
			image = image[imagefirst + 9 :imagelast-9]
			runfirst = description.find("<strong>")
			running = description[runfirst+8:]
			runlast = running.find("</strong>")
			running = running[:runlast]
			startdate = running[:running.find("-")-1]
			endate = running[running.find("-")+2:]
			

			if endate[len(endate)-4:] == "2014":
				startdate = startdate + ", 2014"

			if endate[len(endate)-4:] == "2015" and startdate[len(startdate)-4:] != "2014":
				startdate = startdate + ", 2015"

			for num in range(0,9):
				if len(endate) > 0:
			 		if endate[0] == str(num):
			 			endate = startdate[:startdate.find(" ")] + " " +  endate

			print image
			print show
			print startdate
			print endate
			print producer
			print address
			print venue
			print description
			print "_____________________________________________________"

			



			#c.execute("SELECT id from ZINGVENUES WHERE NAME = %s", (venue,))
			# results = c.fetchall()
			# if results == []:
			#  	#c.execute("SELECT id from ZINGVENUES where name = %s", (producer,))
			#  	#venueid = c.fetchall()
			#  	# if venueid ==[]:
			#  	# 	c.execute("INSERT INTO ZINGVENUES(name, address) VALUES (%s, %s)", (venue, address))
			# 		# c.execute("SELECT id from fringevenues ORDER BY id desc LIMIT 1")
			#  	# 	venueid = c.fetchall()[0][0]
			#  	# else:
			#  	# 	venueid = venueid[0][0]
			# else:
			#  	# venueid = results[0][0]
			if len(endate) > 0:
				c.execute("SELECT id from ZINGSHOWS")
				ids = c.fetchall()
				if len(ids) == 0:
					c.execute("""INSERT INTO ZINGSHOWS(pic, name, descript, producer,  start, enddate) 
                        	 VALUES(%s,%s,%s,%s,%s,%s,%s)""", (image, show, description, producer, startdate, endate))
					conn.commit()
			show = line
			showfirst = show.find(">")
			show = show[showfirst+1:]
			showfirst = show.find(">")
			show = show[showfirst+1:]
			showlast = show.find("<")
			show = show[:showlast]
			firstlink = line.find("href")
			link = line[firstlink:]
			lastlink = link.find(">")
			link = link[6:lastlink-1]
			link = "http://www.theatrephiladelphia.org" + link
			data2 = urllib2.urlopen(link) 
			for line2 in data2:
				if "field-content" in line2 and "div" in line2 and "strong" in line2:
					description = line2
				if "<td class=\"views-field views-field-field-venue-value\">" in line2:
					line2 = data2.next().strip()
					venue = line2[3:]
					venue = venue[:venue.find("<br>")]
					address1 = line2[line2.find("<br>")+4:line2.rfind("<br>")]
					address2 = line2[line2.rfind("<br>")+4:line2.rfind("</p>")]
					
					address = address1 +", " + address2
				if "image-fid" in line2:
					image = data2.next()
					
		if "theatre" in line and "field-content" in line and "div" in line:
			producer = line
			producerfirst = producer.find(">")
			producer = producer[producerfirst+1:]
			producerfirst = producer.find(">")
			producer = producer[producerfirst+1:]
			producerlast = producer.find("<")
			producer = producer[:producerlast]

		
	