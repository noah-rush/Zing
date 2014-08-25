#!/usr/bin/env python

from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff

from tempfile import TemporaryFile
from xlwt import Workbook
book = Workbook()
sheet1 = book.add_sheet('Venues')
sheet1.write(0,0,'id')
sheet1.write(0,1,'name')
sheet1.write(0,2,'address')



target_url = "http://fringearts.com/programs/festival/"
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file

import connectionBoiler

conn=connectionBoiler.get_conn()

for line in data:
    if "Comedy/Improv" in line:
        print line
        nextLine = line
        while not("src=\"http://fringearts.com/wp-content/themes/fringe/js/isotope.pkgd.min.js\"></script><script>" in nextLine):
            nextLine = data.next()
            if "href" in nextLine:
                rightFind = nextLine.find("\">")
                link = nextLine[6:rightFind]
                print link
                data2 = urllib2.urlopen(link)
                for line2 in data2:
                    print line2


    

				






	