import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  import connectionBoiler
  connectionBoiler.connect()

  c=connectionBoiler.connect()
  c.execute("CREATE TABLE UserReviews2(id serial PRIMARY KEY, userid int, reviewtext VARCHAR(100), showID int, time timestamp )")
  c.execute("SELECT * from UserReviews2")
  a = c.fetchall()
  print a
  c.close()

  conn.commit()


if __name__ == '__main__':
  main()

