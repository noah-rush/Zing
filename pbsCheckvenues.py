from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras

conn=connectionBoiler.get_conn()

target_url = "http://www.whyy.org/artsandculture/artscalendar_theater.html"
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
c = conn.cursor()
c.execute("SELECT name from Fringevenues")
print c.fetchall()
for line in data: # files are iterable
   if "<p><a href=" in line and "class=\"contentlink\"" in line:
        first = line.find("class")
        venue = line[first + 20:]
        last = venue.find("<")
        venue = venue[:last]
        firstlink = line.find("href")
        link = line[firstlink + 6:]
        lastlink = line.find("class")
        link = link[:lastlink-14]
        line2 = data.next()
        end = line2.find("<")
        line2 = line2[:end]
        c.execute("SELECT id from Fringevenues where name = %s", (venue,))
        results = c.fetchall()
        if results == []:
            c.execute("INSERT INTO Fringevenues(name, address) VALUES (%s,%s)", (venue, line2))
            c.execute("SELECT id from Fringevenues where name = %s", (venue,))
            venueid = c.fetchall()[0]
            c.execute("INSERT INTO venueInfo(venueid, website) VALUES (%s, %s)", (venueid, link))
            conn.commit()
        print results
        print venue
        print link
        print line2
       
