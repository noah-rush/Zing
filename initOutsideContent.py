import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  import connectionBoiler
  conn = connectionBoiler.get_conn()

  c=conn.cursor()



  c.execute("DROP TABLE OutsideContent")
  c.execute("CREATE TABLE OutsideContent(id serial PRIMARY KEY, publication text, title text, link text, descript text, author text, published text)")
  
 

  conn.commit()


if __name__ == '__main__':
  main()

