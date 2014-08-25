from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras

conn=connectionBoiler.get_conn()

target_url = "http://fringearts.com/event/eugene-ionescos-rhinoceros/"
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file

c = conn.cursor()
showid = 897


for line in data: # files are iterable
   if "showtimes" in line:
        nextline = line
        while not("></div></div></div><div" in nextline):
            
            if "<p>" in nextline:
                playing = nextline
                left = playing.find("<p")
                right = playing.find("<a")
                playing = playing[left+3:right-1]
                dayleft = playing.find(" ")
                dayright = playing.find("at")
                day = playing[dayleft+1:dayright-1]

                playingdate = "9/" + day + "/2014"
            if "href" in nextline:
                link = nextline
                left = link.find("href")
                right = link.find(">Bu")
                link = link[left+6:right-1]
                print playing +"\n" + link + playingdate + "\n\n" 
                c.execute("INSERT INTO Fringedates(showid,playing, playingdate, ticketlink) VALUES(%s,%s,%s,%s)", (showid, playing, playingdate, link))
            nextline = data.next()
            conn.commit()









