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
  c.execute("DELETE from Karlactors")
  #c.execute("CREATE TABLE Karlactors(id serial PRIMARY KEY, actorName VARCHAR(100), bio VARCHAR(1000), pic VARCHAR(100))")
  sheet = wb.sheet_by_index(1) 
  for row in range(sheet.nrows):
      values = []
      for col in range(sheet.ncols):
          values.append(sheet.cell_value(row,col))
      c.execute("INSERT INTO Karlactors(actorName, bio, pic) VALUES(%s,%s,%s)", (values[1],values[2], values[3]))
  

  c.execute("SELECT * from Karlactors") 
  test_results = c.fetchall()
  print test_results
  c.close()

  conn.commit()


if __name__ == '__main__':
  main()

