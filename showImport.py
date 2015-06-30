import xlrd
import connectionBoiler
import psycopg2
import psycopg2.extras
import urllib2 
from urllib import urlretrieve
import urllib
import os
import sys
def run():
	conn = connectionBoiler.get_conn()
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	workbook = xlrd.open_workbook('zingshows.xlsx')
	worksheet = workbook.sheet_by_name('Zingshows')
	num_rows = worksheet.nrows - 1
	num_cells = worksheet.ncols - 1
	curr_row = 0
	while curr_row < num_rows:
		curr_row += 1
		row = worksheet.row(curr_row)
		print 'Row:', curr_row
		curr_cell = -1
		img = worksheet.cell_value(curr_row, 0)
		showname = worksheet.cell_value(curr_row, 1)
		start_cell_type = worksheet.cell_type(curr_row, 2)
		end_cell_type = worksheet.cell_type(curr_row, 3)
		if start_cell_type == 1:
			start = worksheet.cell_value(curr_row, 2)
		else:
			start = xlrd.xldate.xldate_as_datetime(worksheet.cell_value(curr_row, 2), workbook.datemode)
		if end_cell_type == 1:
			enddate = worksheet.cell_value(curr_row, 3)
		else:
			enddate = xlrd.xldate.xldate_as_datetime(worksheet.cell_value(curr_row, 3), workbook.datemode)
		venue = worksheet.cell_value(curr_row, 4)
		producer = worksheet.cell_value(curr_row, 5)
		descript = worksheet.cell_value(curr_row, 6)
		c.execute("SELECT * FROM Zingshows WHERE NAME = %s", (showname,))
		testResults = c.fetchall()
		if len(testResults) == 0:
			print showname
			c.execute("SELECT id FROM THEATRES WHERE name = %s", (venue,))
			venueid = c.fetchall()[0]['id']
			print venueid
			c.execute("""INSERT INTO ZINGSHOWS( name, descript, producer,  start, enddate, venueid) 
                         VALUES(%s,%s,%s,%s,%s,%s)""", ( showname, descript, producer, start, enddate, venueid))
			conn.commit()
			c.execute("SELECT id from Zingshows WHERE name = %s", (showname,))
			showid = c.fetchall()[0]['id']
			urllib.urlretrieve(img, "static/Zingimages/" + str(showid) + ".jpg")


run()