import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  wb = open_workbook('zingTheaterMarketingDirectory.xlsx')
  import connectionBoiler
  conn = connectionBoiler.get_conn()

  c=conn.cursor()
  
  c.execute("CREATE TABLE goodAdjectives(id serial PRIMARY KEY, showID int, adjective VARCHAR(100), userid int)")
  c.execute("CREATE TABLE badAdjectives(id serial PRIMARY KEY, showID int, adjective VARCHAR(100), userid int)")


  


  conn.commit()


if __name__ == '__main__':
  main()

