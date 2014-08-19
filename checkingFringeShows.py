
from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras
import dissectingfringe2

conn=connectionBoiler.get_conn()

target_url = "http://www.livearts-fringe.org/festival/index.cfm"
data = urllib2.urlopen(target_url)

c = conn.cursor()




for line in data:
    if "Comedy" in line:
        test = ""
        while(not("<div id=\"footer\">" in test)):
            test = data.next()
            if("a href" in test):
                first = test.find("\"")+1
                last = test.find("\">")
                link = test[first:last]
                firstName = test.find("<i>")
                name = test[firstName+3:]
                lastName = name.find("<")
                name = name[:lastName]
                c.execute("SELECT id from Fringeshows where name = %s", (name,))
                if c.fetchall() == []:
                	print name
                	print link
                	dissectingfringe2.findData(link)
                