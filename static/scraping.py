from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras

conn=connectionBoiler.get_conn()

target_url = "http://phindie.com/author/henrik-eger/"
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
name = ""
producer =""
photoUrl = ""
description = ""
venue = ""
addressData = ""
venueid = ""
for line in data: # files are iterable
	if "h3" in line and "href" in line:
		print line