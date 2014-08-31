import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  wb = open_workbook('critics.xlsx')
  import connectionBoiler

  conn=connectionBoiler.get_conn()
  c = conn.cursor()
  
  sheet = wb.sheet_by_index(0) 

  for row in range(sheet.nrows):
    name = sheet.cell_value(row,1)
    c.execute("INSERT INTO critics(name) VALUES(%s)", (name,))
  conn.commit()
  


if __name__ == '__main__':
  main()

