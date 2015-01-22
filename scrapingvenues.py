
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras
from urllib import urlretrieve

conn=connectionBoiler.get_conn()

target_urls = ["http://www.theatrephiladelphia.org/theatres?page=1",
			 "http://www.theatrephiladelphia.org/theatres",
			]
c = conn.cursor()


for target in target_urls:
	data = urllib2.urlopen(target) # it's a file like object and works just like a file
	print "\n\n\n\n"
	for line in data: # files are iterable
		if "imagecache-Program_Thumb_defaul" in line:
			print line[line.find("src")+5: line.find("png")+3]
			imagelink = line[line.find("src")+5: line.find("png")+3]
		if "field-content" in line and "/theatres" in line:
		
			name = line[line.find(">")+1:]
			print name[name.find(">")+1:name.find("span")-6]
			venuename = name[name.find(">")+1:name.find("span")-6]
			c.execute("SELECT id from ZINGVENUES where name = %s", (venuename,))
			results = c.fetchall()
			if len(results)>0:
				venueid = results[0][0]
				print venueid
				href = line[line.find("href")+6: line.rfind('"')]
				link = "http://www.theatrephiladelphia.org"+href
				
				data2 = urllib2.urlopen(link)
				for line2 in data2:
					if "views-field-body" in line2:
						desc = data2.next()
						desc = desc[desc.find(";")+2:desc.find("<br>")]
						print desc
						print "\n\n"
						urllib.urlretrieve(imageLink, "static/ZingVenueImages/" + venueid + ".jpg")
