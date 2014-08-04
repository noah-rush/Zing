from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff
import connectionBoiler
import psycopg2.extras

conn=connectionBoiler.get_conn()

target_url = "http://www.livearts-fringe.org/festival/index.cfm"
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file
name = ""
producer =""
photoUrl = ""
description = ""
venue = ""
addressData = ""
venueid = ""
for line in data: # files are iterable
    c=conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if "font-size:12pt; color:#1C3762;font-weight:bold;" in line:
        first = line.find("font-size:12pt; color:#1C3762;font-weight:bold;") +2
        first = first + len("font-size:12pt; color:#1C3762;font-weight:bold;")
        last = line.find("</span>")
        name = line[first: last]
        #print name
    if "span style=\"font-size:11pt;\"" in line:
    	first = line.find("span style=\"font-size:11pt;\"") + 1
    	first = first + len("span style=\"font-size:11pt;\"")
    	last = line.find("</span>")
    	producer = line[first: last]
    	#print producer
    if "alt=\"\" />" in line and "valign=\"top\""in line:
        # if len(photoUrl)>0:
        #     c.execute("""SELECT *
        #               FROM Fringevenues
        #               where name = %s""", (venue,))
        #     results = c.fetchall()
        #     if results == []:
        #         c.execute("""INSERT INTO Fringevenues(name, address)
        #                   VALUES (%s, %s)""", (venue.strip(), addressData.strip()))
        #         c.execute("""SELECT id 
        #                     FROM Fringevenues where name = %s""", (venue,))
        #         if c.fetchall() != []:
        #             venueid = c.fetchall()[0]['id']
        #     else: 
        #         venueid = results[0]['id']
        #     c.execute("""INSERT INTO fringeshows(name, venueid, pic, producer, description)
        #               VALUES(%s,%s,%s,%s,%s)""", (name, venueid, photoUrl, producer, description))
        #     conn.commit()

    	first = line.find("src=") +5 
    	last = line.find("alt")-2
    	photoUrl = line[first:last]
    	photoUrl = "http://fringearts.net" + photoUrl
    	#print photoUrl
    if "background-color:rgba(240,240,240,1)" in line:
    	first = line.find("1);") +6
    	last = line.find("<br") -1
    	review = line[first:last]
    	#print review 
    	linetwo = data.next()
    	first = linetwo.find("<em>") - 2
    	if first == -3:
    		first = linetwo.find("<i>") -2
    	reviewer = linetwo[:first]
    	last = linetwo.find("</em>")
    	if last == -1:
    		last = linetwo.find("</i>")
    	first = first + 6
    	reviewSource = linetwo[first: last]
    	#print reviewer.strip()
    	#print reviewSource
    	tagline = data.next()
    	if reviewSource != "Huffington Post":
    		while(tagline.find("<table") ==-1):
    			tagline = tagline + data.next()
    	else: 
    		while(tagline.find("<p><table style-\"font-size:8pt;\"><tr>") ==-1):
    			tagline = tagline + data.next()
    	last = tagline.find("<a href=")
    	if last == -1:
    		last = tagline.find("<p><table style-\"font-size:8pt;\"><tr>")
    	address = tagline[last:]
    	address = address[:address.rfind("</p>")]
    	description = tagline[:last]
    	venueStart = description.rfind("</p>")
    	venue = description[venueStart:]
    	description = description[:(venueStart+4)]
        description = review + reviewer + description
    	venueFirst = venue.find("<b>")+3
    	venueLast = venue.find("</b>")
    	venue = venue[venueFirst: venueLast]
    	#print description.strip()
    	#print venue.strip()
    	addresslink = address[address.find("\""):address.find(">")]
    	#print addresslink
    	address = address[address.find(">") +1 :]
    	#print address
    	addressData = address[:address.find("<")]
    	#print addressData
    	addressDescript = address[address.find(">") +2:]
    	#print addressDescript
        datelist = []
    	dates = ""
    	dates2 = ""
    	while(not("</table" in dates)):
    		dates = dates + data.next()
    	if reviewer.strip() == "Nelson Pressley": 
    		while(not("</table" in dates2)):
    			dates2 = dates2 + data.next()
    	for mazeebo in iter(dates.splitlines()):
            if "<a" in mazeebo and "Sept" in mazeebo:
                datelist.append(mazeebo)
        for mazeebo in iter(dates2.splitlines()):
            if "<a" in mazeebo and "Sept" in mazeebo:
                datelist.append(mazeebo)
        c.execute("SELECT id from Fringeshows where name  =%s", (name,))
        showid = c.fetchall()[0]['id']
        for date in datelist:
            date = date.strip()
            first = date.find("\"")
            last = date.find(">")
            ticketlink = date[first+1: last-1]
            print name
            print ticketlink
            playing = date[last +1:]
            playing = playing[:playing.find("<")]
            print playing
            playingdate = playing[playing.find("t") +1: playing.find("at")-1]
            playingdate = "September" + playingdate +", 2014"
            print playingdate
            c.execute("INSERT INTO Fringedates(showid, playing, playingdate, ticketlink) VALUES(%s,%s,%s,%s)", (showid,playing, playingdate, ticketlink ))
            conn.commit()









