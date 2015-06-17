
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras
from urllib import urlretrieve
import urlparse
import urllib
from xlrd import open_workbook
from xlwt import Workbook
conn=connectionBoiler.get_conn()

target_urls = ["http://www.theatrephiladelphia.org/calendar"
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
book = Workbook()

sheet1 = book.add_sheet('PhillyVenues')
sheet1.write(0,0,'name')
sheet1.write(0,1,'picture')
sheet1.write(0,2,'description')
sheet1.write(0,3,'address')
sheet1.write(0,4,'phone')
sheet1.write(0,5,'email')
sheet1.write(0,6,'site')
sheet1.write(0,7,'fb')
sheet1.write(0,8,'twitter')
count = 1
for target in target_urls:
	data = urllib2.urlopen(target) # it's a file like object and works just like a file
	print "\n\n\n\n"
	for line in data: # files are iterable
		if "event" in line and "field-content" in line and not("More Details" in line)and not("Slideshow_feature" in line): 
			show = line
			showfirst = show.find(">")
			show = show[showfirst+1:]
			showfirst = show.find(">")
			show = show[showfirst+1:]
			showlast = show.find("<")
			show = show[:showlast]
			print show
			# c.execute("SELECT id from ZINGSHOWS where name = %s", (show,))
			# showid = c.fetchall()[0][0]
		if "field-content" in line and "/theatres" in line:
		
				name = line[line.find(">")+1:]
				
				venuename = name[name.find(">")+1:name.find("span")-14]
				print venuename
				sheet1.write(count,0,venuename)
				href = line[line.find("href")+6: line.rfind('"')]
				link = "http://www.theatrephiladelphia.org"+href
				data2 = urllib2.urlopen(link)
				for line2 in data2:
						if "views-field-body" in line2:
							desc = data2.next()
							desc = desc[desc.find(";")+2:desc.find("<br>")]
							print desc
							sheet1.write(count,2,desc.decode('utf-8'))
						if "Contact Inform" in line2:
							address1 = data2.next()
							address1 = address1[:address1.find("br")-1]
							address2 = data2.next()
							address2 = address2[:address2.find("br") - 1 ]
							address = address1 + ", \n" +address2
							print address
							sheet1.write(count,3,address)
						if "Phone" in line2:
							phone  = line2
							print phone
							phone =phone.replace("<br>", "")
							phone =phone.replace("Phone: ", "")
							sheet1.write(count,4,phone)
						if "Email" in line2:
							email  = line2[line2.find("mailto")+7:line2.find('">')]
							print email
							sheet1.write(count,5,email)
						if "Website" in line2 and "target" in line2:
							site = line2[line2.find("href") +6:line2.find('">')]
							print site
							sheet1.write(count,6,site)
						if "imagecache-Headshot_Feature_imagelink" in line2:
						
							img = line2
							img = img[img.find("href")+6:img.find("png")+3]
							print img
							sheet1.write(count,1,img)
							urllib.urlretrieve(img, "static/ZingVenueImages/" + venuename + ".png")
						if "Social Media Links" in line2:
							fb = data2.next()
							twit = data2.next()
							fb = fb[fb.find("href")+6: fb.find('">')]
							twit = twit[twit.find("href")+6: twit.find('">')]
							print fb
							print twit
							sheet1.write(count,7,fb)
							sheet1.write(count,8,twit)
							print "\n\n\n\n"
				count = count +1
book.save('zingvenues.xls')
							# c.execute("SELECT id from PHILLYVENUES where name = %s", (venuename,))
							# results = c.fetchall()
							# if len(results) == 0:
							# 	c.execute("""INSERT INTO PHILLYVENUES(name, address, description,
							# 				website, phone, email, facebook, twitter) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
							# 				(venuename, address, desc, site, phone, email, fb, twit))
							# 	conn.commit()
							# c.execute("SELECT id from PHILLYVENUES where name = %s", (venuename,))
							# venueid = c.fetchall()[0][0]
							# c.execute("UPDATE ZINGSHOWS set venueid = %s where id = %s", (venueid, showid))
							# urllib.urlretrieve(img, "static/ZingVenueImages/" + str(venueid) + ".png")
							# conn.commit()



						# urllib.urlretrieve(imageLink, "static/ZingVenueImages/" + venueid + ".jpg")

	# 		results = c.fetchall()
	# 		imagefirst = image.find("<a")
	# 		imagelast = image.find("imagecache")
	# 		image = image[imagefirst + 9 :imagelast-9]
	# 		runfirst = description.find("<strong>")
	# 		running = description[runfirst+8:]
	# 		runlast = running.find("</strong>")
	# 		running = running[:runlast]
	# 		startdate = running[:running.find("-")-1]
	# 		endate = running[running.find("-")+2:]
			

	# 		if endate[len(endate)-4:] == "2014":
	# 			startdate = startdate + ", 2014"

	# 		if endate[len(endate)-4:] == "2015" and startdate[len(startdate)-4:] != "2014":
	# 			startdate = startdate + ", 2015"

	# 		for num in range(0,9):
	# 			if len(endate) > 0:
	# 		 		if endate[0] == str(num):
	# 		 			endate = startdate[:startdate.find(" ")] + " " +  endate

	# 		print image
	# 		print show
	# 		print startdate
	# 		print endate
	# 		print producer
	# 		print address
	# 		print venue
	# 		print description
	# 		print "_____________________________________________________"

			



	# 		c.execute("SELECT id from ZINGVENUES WHERE NAME = %s", (venue,))
	# 		results = c.fetchall()
	# 		if results == []:
	# 		 	c.execute("SELECT id from ZINGVENUES where name = %s", (producer,))
	# 		 	venueid = c.fetchall()
	# 		 	if venueid ==[]:
	# 		 		c.execute("INSERT INTO ZINGVENUES(name, address) VALUES (%s, %s)", (venue, address))
	# 				c.execute("SELECT id from fringevenues ORDER BY id desc LIMIT 1")
	# 		 		venueid = c.fetchall()[0][0]
	# 		 	else:
	# 		 		venueid = venueid[0][0]
	# 		else:
	# 		 	venueid = results[0][0]
	# 		if len(endate) > 0:
	# 			c.execute("""INSERT INTO ZINGSHOWS(pic, name, descript, producer, venueid, start, enddate) 
 #                        	 VALUES(%s,%s,%s,%s,%s,%s,%s)""", (image, show, description, producer, venueid, startdate, endate))
	# 			conn.commit()
	# 		show = line
	# 		showfirst = show.find(">")
	# 		show = show[showfirst+1:]
	# 		showfirst = show.find(">")
	# 		show = show[showfirst+1:]
	# 		showlast = show.find("<")
	# 		show = show[:showlast]
	# 		firstlink = line.find("href")
	# 		link = line[firstlink:]
	# 		lastlink = link.find(">")
	# 		link = link[6:lastlink-1]
	# 		link = "http://www.theatrephiladelphia.org" + link
	# 		data2 = urllib2.urlopen(link) 
	# 		for line2 in data2:
	# 			if "field-content" in line2 and "div" in line2 and "strong" in line2:
	# 				description = line2
	# 			if "<td class=\"views-field views-field-field-venue-value\">" in line2:
	# 				line2 = data2.next().strip()
	# 				venue = line2[3:]
	# 				venue = venue[:venue.find("<br>")]
	# 				address1 = line2[line2.find("<br>")+4:line2.rfind("<br>")]
	# 				address2 = line2[line2.rfind("<br>")+4:line2.rfind("</p>")]
					
	# 				address = address1 +", " + address2
	# 			if "image-fid" in line2:
	# 				image = data2.next()
					
	# 	if "theatre" in line and "field-content" in line and "div" in line:
	# 		producer = line
	# 		producerfirst = producer.find(">")
	# 		producer = producer[producerfirst+1:]
	# 		producerfirst = producer.find(">")
	# 		producer = producer[producerfirst+1:]
	# 		producerlast = producer.find("<")
	# 		producer = producer[:producerlast]

		
	# 