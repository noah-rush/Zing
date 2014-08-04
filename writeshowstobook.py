import connectionBoiler
conn = connectionBoiler.get_conn()

from tempfile import TemporaryFile
from xlwt import Workbook
book = Workbook()
sheet1 = book.add_sheet('Shows')
sheet1.write(0,0,'id')
sheet1.write(0,1,'name')
sheet1.write(0,2,'address')
sheet1.write(0,3,'extra info')
c = conn.cursor()
c.execute("SELECT * from fringeshows")
a = c.fetchall()
for data in a:
	sheet1.write(data[0],0,data[0])
	sheet1.write(data[0],1,data[1])
	sheet1.write(data[0],2,data[2])
	sheet1.write(data[0],3,data[3])
	sheet1.write(data[0],4,data[4])
	sheet1.write(data[0],5,data[5])
	

book.save('shows.xls')
book.save(TemporaryFile())