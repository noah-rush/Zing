import connectionBoiler 
conn = connectionBoiler.get_conn()
c = conn.cursor()
c.execute("SELECT id from Fringeshows")
results = c.fetchall()
print results
for x in results:
	print x
	c.execute("INSERT INTO Showratings4(showid) VALUES(%s)", (x,))
conn.commit()