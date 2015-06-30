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
	workbook = xlrd.open_workbook('zingvenues.xlsx')
	worksheet = workbook.sheet_by_name('PhillyVenues')
	num_rows = worksheet.nrows - 1
	num_cells = worksheet.ncols - 1
	curr_row = 0
	while curr_row < num_rows:
		curr_row += 1
		row = worksheet.row(curr_row)
		print 'Row:', curr_row
		curr_cell = -1
		venuename = worksheet.cell_value(curr_row, 0)
		img = worksheet.cell_value(curr_row, 1)
		descript = worksheet.cell_value(curr_row, 2)
		address = worksheet.cell_value(curr_row, 3)
		phone = worksheet.cell_value(curr_row, 4)
		email = worksheet.cell_value(curr_row, 5)
		site = worksheet.cell_value(curr_row, 6)
		fb = worksheet.cell_value(curr_row, 7)
		tw = worksheet.cell_value(curr_row, 8)
		tix = worksheet.cell_value(curr_row, 9)
		c.execute("SELECT * FROM Theatres WHERE NAME = %s", (venuename,))
		testResults = c.fetchall()
		if len(testResults) == 0:
			print venuename
			c.execute("""INSERT INTO THEATRES(name, address, descript,
						 site, phone, email, fb, tw, tix) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
					     (venuename, address, descript, site, phone, email, fb, tw, tix))
			conn.commit()
			c.execute("SELECT id from THEATRES WHERE name = %s", (venuename,))
			venueid = c.fetchall()[0]['id']
			urllib.urlretrieve(img, "static/ZingVenueImages/" + str(venueid) + ".png")


run()