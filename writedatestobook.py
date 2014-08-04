import connectionBoiler
conn = connectionBoiler.get_conn()

from tempfile import TemporaryFile
from xlwt import Workbook
book = Workbook()
sheet1 = book.add_sheet('Dates')
sheet1.write(0,0,'id')
sheet1.write(0,1,'showid')
sheet1.write(0,2,'datetime')
sheet1.write(0,3,'link')
c = conn.cursor()
c.execute("SELECT * from fringedates")
a = c.fetchall()
for data in a:
	sheet1.write(data[0],0,data[0])
	sheet1.write(data[0],1,data[1])
	sheet1.write(data[0],2,data[2])
	sheet1.write(data[0],3,data[3])
	sheet1.write(data[0],4,data[4])
	print data
	

book.save('dates.xls')
book.save(TemporaryFile())