import connectionBoiler
import psycopg2
import psycopg2.extras
conn = connectionBoiler.get_conn()
c =conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
c.execute("CREATE TABLE Fringedates2(id serial PRIMARY KEY, showID int, playing text, playingdate date, ticketlink text, timeOfShow text)")
c.execute("SELECT * FROM Fringedates")
for x in c.fetchall():
	if "at" in x['playing']:
		finddash = x['playing'].find("at") +3 
		if "Saturday" in x['playing']:
			newstr = x['playing'][finddash:]
			if "at" in newstr:
				finddash = newstr.find("at") +3 
			else:
				finddash = newstr.find("-")+6
	else:
		finddash = x['playing'].find("-")+2
	
	timeOfShow = x['playing'][finddash:]
	print "\n"
	c.execute("""INSERT INTO Fringedates2(showID, playing, playingdate, ticketlink,timeOfShow) 
		       VALUES(%s,%s,%s,%s,%s)""", (x['showid'], x['playing'], x['playingdate'], x['ticketlink'], timeOfShow))
conn.commit()




