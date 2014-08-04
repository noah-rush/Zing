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
  c.execute("DROP TABLE Fringedates")
  c.execute("CREATE TABLE Fringedates(id serial PRIMARY KEY, showID int, playing VARCHAR(200), playingdate date, ticketlink VARCHAR(400))")


  c.close()
  conn.commit()
  
  


if __name__ == '__main__':
  main()
