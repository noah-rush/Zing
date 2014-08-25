import connectionBoiler

conn = connectionBoiler.get_conn()
c = conn.cursor()
c.execute("SELECT * From Fringevenues")
results = c.fetchall()




for result in results:
    if 'ADA' in result[2]:
            last = result[2].find('ADA')
            newAddress = result[2][:last]
            print newAddress
            c.execute("UPDATE Fringevenues SET address = %s where id = %s", (newAddress, result[0]))

conn.commit()

c.execute("SELECT * From Fringevenues")
results = c.fetchall()

for result in results:
	print result