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

  c.execute("CREATE TABLE venueInfo(id serial PRIMARY KEY, venueid int,  phone VARCHAR(500), email VARCHAR(500), website VARCHAR(200), tickets VARCHAR(200))")

  conn.commit()


if __name__ == '__main__':
  main()

