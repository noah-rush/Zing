import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  import connectionBoiler
  connectionBoiler.connect()

  c=connectionBoiler.connect()




  #c.execute("CREATE TABLE KarlUsers(id serial PRIMARY KEY, username VARCHAR(100), passhash VARCHAR(1000))")
  c.execute("SELECT * from KarlUsers")
  a = c.fetchall()
  print a
  c.close()

  conn.commit()


if __name__ == '__main__':
  main()

