#connection boilerplate


Database_URL = "postgres://rnrbbyzitetmsb:jmRnF-H43hThjBRjU81IOvyKhN@ec2-54-197-250-40.compute-1.amazonaws.com:5432/dn2eee7k8ndak"

def get_cursor():
	import os
	import psycopg2
	import urlparse
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(Database_URL)

	conn = psycopg2.connect(
      database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
  	)
	return conn.cursor()

def get_conn():
	import os
	import psycopg2
	import urlparse
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(Database_URL)

	conn = psycopg2.connect(
      database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
  	)
	return conn