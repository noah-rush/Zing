from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras

conn=connectionBoiler.get_conn()

target_url = "http://www.whyy.org/artsandculture/artscalendar_theater.html"
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
c = conn.cursor()
c.execute("SELECT name from Karlvenues")
results = c.fetchall()
for venue in results:
	c.execute("SELECT id from Fringevenues where name = %s", venue)
	if c.fetchall() ==[]:
		c.execute("SELECT name, address from Karlvenues where name = %s", venue)
		results = c.fetchall()
		c.execute("INSERT INTO Fringevenues(name, address) VALUES (%s,%s)", (results[0][0], results[0][1]))
		conn.commit()
		print results
