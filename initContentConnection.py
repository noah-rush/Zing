import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  import connectionBoiler
  conn = connectionBoiler.get_conn()

  c=conn.cursor()



  c.execute("CREATE TABLE contentconnection(id serial PRIMARY KEY, articleid int, showid int)")
  
 

  conn.commit()


if __name__ == '__main__':
  main()

