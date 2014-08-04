import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  wb = open_workbook('zingTheaterMarketingDirectory.xlsx')
  import connectionBoiler
  connectionBoiler.connect()

  c=connectionBoiler.connect()
  c.execute("DELETE FROM Karlcasting")
  #c.execute("CREATE TABLE Karlcasting(id serial PRIMARY KEY, actorID int, showID int, role VARCHAR(100))")
  sheet = wb.sheet_by_index(2) 
  for row in range(sheet.nrows):
      values = []
      for col in range(sheet.ncols):
          values.append(sheet.cell_value(row,col))
      c.execute("SELECT id from Karlactors where actorName = %s", (values[2],))
      actorID = c.fetchall()
      c.execute("SELECT id from Karlshows2 where name = %s", (values[1],))
      showID = c.fetchall()
      if len(actorID)>0 and len(showID)>0:
        actorID = actorID[0]
        showID = showID[0]
        print showID
        print actorID
        c.execute("INSERT INTO Karlcasting(actorID, showID, role) VALUES(%s, %s, %s)", (actorID, showID, values[3]))
  
  c.execute("SELECT * from Karlcasting")
  test_results = c.fetchall()
  print test_results
  c.close()

  conn.commit()


if __name__ == '__main__':
  main()

