from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras
import urlparse
import urllib2 

from urllib import urlretrieve
import urllib
import os
import sys
import connectionBoiler


conn=connectionBoiler.get_conn()

target_url = "http://fringearts.com/programs/festival/"
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
c = conn.cursor()



for line in data: # files are iterable
    if "src" in line:
        if "landscape" in line:
            linkright = line.find("jpg")
            link = line[5:linkright+3]
            nameLeft = line.find("alt")
            nameRight = line.find("class")
            name = line[nameLeft+5:nameRight-2]
            print link
            print name
            if name == 'Experiment #39 (OLD CITY)':
                name = 'Experiment #39'
            c.execute("SELECT id from Fringeshows where name = %s", (name,))
            results = c.fetchall()[0][0]
            print results
            c.execute("UPDATE Fringeshows SET pic = %s where id = %s", (link,results))
            conn.commit()
            urllib.urlretrieve(link, "static/Fringeimages/" + name + ".jpg")




