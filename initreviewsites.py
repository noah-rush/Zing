import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  wb = open_workbook('critics.xlsx')
  import connectionBoiler

  conn=connectionBoiler.get_conn()
  c = conn.cursor()
  
  sheet = wb.sheet_by_index(1) 
  #c.execute("CREATE TABLE reviewsites(id serial PRIMARY KEY, name VARCHAR(100))")
  for row in range(sheet.nrows):
    name = sheet.cell_value(row,2r)
    print name
    c.execute("INSERT INTO reviewsites(name) VALUES(%s)", (name,))
  conn.commit()
  


if __name__ == '__main__':
  main()

