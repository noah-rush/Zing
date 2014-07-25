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
  c.execute("DELETE from Karlreviews")
  #c.execute("CREATE TABLE Karlreviews(id serial PRIMARY KEY, journalist VARCHAR(100), showID int, reviewtext VARCHAR(100), publication VARCHAR(100))")
  sheet = wb.sheet_by_index(4) 
  for row in range(sheet.nrows):
      values = []
      for col in range(sheet.ncols):
          values.append(sheet.cell_value(row,col))
      c.execute("SELECT id from Karlshows2 where name = %s", (values[2],))
      showID = c.fetchall()
      if len(showID)>0:
          
          showID = showID[0]
          print showID
          c.execute("INSERT INTO Karlreviews(journalist, showID, reviewtext, publication) VALUES(%s, %s, %s, %s)", (values[1], showID, values[3], values[4]))
      print values
  
  c.execute("SELECT * from Karlreviews")
  test_results = c.fetchall()
  print test_results
  c.close()

  conn.commit()


if __name__ == '__main__':
  main()

