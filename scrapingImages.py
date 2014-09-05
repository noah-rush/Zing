
from BeautifulSoup import BeautifulSoup as bs
import urlparse
import urllib2 

from urllib import urlretrieve
import urllib
import os
import sys
import connectionBoiler

def main(url, out_folder):
    data = urllib2.urlopen(url)
    for line in data:
        print line
    data.close()

conn = connectionBoiler.get_conn()
c =conn.cursor()
c.execute("SELECT pic, id, name from Fringeshows")
results = c.fetchall()
out_folder = "/static/fringeImages"
for result in results:
    print result[0]
    print result[1]
    print result[2]
    name =  str(result[1])
    if result[0] != None:
    	urllib.urlretrieve(result[0], "static/Fringeimages/" + name + ".jpg")

       