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

  c.execute("CREATE TABLE Karlvenues(id serial PRIMARY KEY, name VARCHAR(100), address VARCHAR(500), phone VARCHAR(500), email VARCHAR(500), website VARCHAR(200), tickets VARCHAR(200))")
  sheet = wb.sheet_by_index(1) 
  for row in range(sheet.nrows):
      values = []
      for col in range(sheet.ncols):
          values.append(sheet.cell_value(row,col))
      c.execute("INSERT INTO Karlvenues(name, address,phone,email,website, tickets) VALUES(%s, %s, %s, %s,%s,%s)", (values[0], values[1], values[2], values[3], values[4], values[5]))
 
  c.close()

  conn.commit()


if __name__ == '__main__':
  main()

