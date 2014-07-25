import os
import psycopg2
import urlparse



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

	c.execute("CREATE TABLE gigs (id int PRIMARY KEY,  city VARCHAR(100), venue VARCHAR(500), date DATE)")
	c.execute("INSERT INTO gigs VALUES(1, 'Philadelphia', 'The Happy Snail', '9/24/12' )")
	c.execute("INSERT INTO gigs VALUES(2, 'Trenton',  'Lous', '12/12/14')")
	c.execute("INSERT INTO gigs VALUES(3, 'Wilmington', 'Nevermind', '6/14/13')")
	c.execute("INSERT INTO gigs VALUES(4, 'New York', 'Happy Jones', '9/9/11')")
	c.close()

	conn.commit()


if __name__ == '__main__':
	main()

