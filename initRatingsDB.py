import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
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
  c.execute("CREATE TABLE UserReviews2(id serial PRIMARY KEY, userid int, reviewtext VARCHAR(100), showID int, time timestamp )")
  c.execute("SELECT * from UserReviews2")
  a = c.fetchall()
  print a
  c.close()

  conn.commit()


if __name__ == '__main__':
  main()

