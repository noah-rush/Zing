import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  wb = open_workbook('zingTheaterMarketingDirectory.xlsx')
  urlparse.uses_netloc.append("postgres")
  url = urlparse.urlparse(os.environ["DATABASE_URL"])

  conn = psycopg2.connect(
      database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
  )



  c = conn.cursor()

  c.execute("CREATE TABLE Karlshows2(id serial PRIMARY KEY, name VARCHAR(100), venueID int, start_date DATE, end_date DATE)")
  sheet = wb.sheet_by_index(1) 
  for row in range(sheet.nrows):
      values = []
      for col in range(sheet.ncols):
          values.append(sheet.cell_value(row,col))
      c.execute("SELECT id from Karlvenues WHERE name = %s", (values[2],))
      venID = c.fetchall()
      if len(venID)>0:
      	venID =  venID[0][0]
      	c.execute("INSERT INTO Karlshows2(name, venueID, start_date, end_date) VALUES(%s,%s,%s, %s)", (values[1], venID, values[3], values[4]))


  c.close()
  conn.commit()
  
  


if __name__ == '__main__':
  main()
