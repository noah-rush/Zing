from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras

conn=connectionBoiler.get_conn()

target_urls = ["http://www.theatrephiladelphia.org/calendar",
			 "http://www.theatrephiladelphia.org/calendar?page=1",
			 "http://www.theatrephiladelphia.org/calendar?page=2",
			 "http://www.theatrephiladelphia.org/calendar?page=3"]
c = conn.cursor()
show = ""
venue = ""
address = ""
producer = ""
description = ""
for target in target_urls:
	data = urllib2.urlopen(target) # it's a file like object and works just like a file
	print "\n\n\n\n"
	for line in data: # files are iterable
		if "event" in line and "field-content" in line and not("More Details" in line)and not("Slideshow_feature" in line): 
			c.execute("SELECT id from fringeshows where name = %s", (show,))
			results = c.fetchall()
			print show
			print producer
			print address
			print venue
			print description
			print "_____________________________________________________"
			if results == []:
				c.execute("SELECT id from fringevenues where name = %s", (producer,))
				venueid = c.fetchall()
				if venueid ==[]:
					c.execute("INSERT INTO fringevenues(name, address) VALUES (%s, %s)", (venue, address))
					c.execute("SELECT id from fringevenues ORDER BY id desc LIMIT 1")
					venueid = c.fetchall()[0][0]
				else:
					venueid = venueid[0][0]
				c.execute("SELECT id from fringeshows where name = %s", (show,))
				if c.fetchall() ==[]:
					c.execute("INSERT INTO fringeshows(name, venueid, producer, description) VALUES(%s, %s, %s, %s)", (show, venueid, producer, description))
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
		if "theatre" in line and "field-content" in line and "div" in line:
			producer = line
			producerfirst = producer.find(">")
			producer = producer[producerfirst+1:]
			producerfirst = producer.find(">")
			producer = producer[producerfirst+1:]
			producerlast = producer.find("<")
			producer = producer[:producerlast]

		conn.commit()
	