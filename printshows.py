import connectionBoiler
conn = connectionBoiler.get_conn()
c = conn.cursor()
c.execute("SELECT id, name from Fringeshows ORDER BY name")
results = c.fetchall()
for line in results:
	print line 
