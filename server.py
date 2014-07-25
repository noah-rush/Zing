import os
import psycopg2, psycopg2.extras
import urlparse
from flask import render_template,jsonify, Flask, request, escape, session, url_for, redirect
import sys
from werkzeug.security import generate_password_hash, \
     check_password_hash
from werkzeug import security

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)




reload(sys)
sys.setdefaultencoding("utf-8")


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
)

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
	if 'username' in session:
		return render_template('layout.html', useron = session['username'])
	return render_template('layout.html', useron = 'none')

@app.route('/usernameNotFound', methods = ['GET', 'POST'])
def usernameNotFound():
	return "UserName not found."

@app.route('/passwordNotFound', methods = ['GET', 'POST'])
def passwordNotFound():
	return "Password not found."



@app.route('/loggedin', methods=['GET', 'POST'])
def loggedin():
	
		username = request.args.get('username')
		password = request.args.get('password')
		print username
		print password
		c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		c.execute("SELECT passhash FROM KarlUsers where username = %s", (username,))
		realkey = c.fetchall()
		if len(realkey) == 1:
			realkey = realkey[0]['passhash']
		else: 
			return "Username not found."
		if security.check_password_hash(realkey, password):
			session['username'] = username
			return "Login successful. %s" %(username)
		return "Incorrect Password"

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/newUser', methods=['GET', 'POST'])
def newUser():
	return render_template('newUser.html', useron = 'none')
	
	
@app.route('/usercreate', methods=['GET', 'POST'])
def usercreate():
	username = request.form['username']
	password = request.form['password']
	passwordConfirm = request.form['passwordConfirm']
	if password == passwordConfirm:
		c = conn.cursor()
		you = User(username, password)
		passhash = you.pw_hash
		c.execute("INSERT INTO KarlUsers(username, passhash) VALUES (%s, %s)", (username, passhash))
		session['username'] = username
		conn.commit()
		return redirect(url_for('index'))
	else: 
		return "Passwords do not match."
	

@app.route('/venues')
def venues():
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	c.execute("SELECT name from Karlvenues")
	results = c.fetchall()
	newResults =[]
	print results
	# newResults = []
	# for result in results:
		
	#     newResult = list(result)
	#     newResult[3] = str(newResult[3])
	#     newResults.append(newResult)
	
	return render_template('all_venues.html', results = results)


@app.route('/nowPlaying')
def nowPlaying():
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	c.execute("SELECT Karlshows2.name from Karlshows2 WHERE (CURRENT_DATE, CURRENT_DATE) OVERLAPS (start_date, end_date)")
	showresults = c.fetchall()
	c.execute("SELECT Karlvenues.name from Karlshows2, Karlvenues WHERE (CURRENT_DATE, CURRENT_DATE) OVERLAPS (start_date, end_date) and Karlvenues.id = Karlshows2.venueID")
	venueresults = c.fetchall()
	print showresults
	print venueresults
	results = []
	for x in range(len(showresults)):
		result = []
		result.append(showresults[x]['name'])
		result.append(venueresults[x]['name'])
		results.append(result)


	# newResults = []
	# for result in results:
		
	#     newResult = list(result)
	#     newResult[3] = str(newResult[3])
	#     newResults.append(newResult)
	
	return render_template('nowPlaying.html', results = results)


@app.route('/venue/<venue>', methods =['GET','POST'])
def venue(venue):
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	c.execute("SELECT * from Karlvenues where name = %s", (venue,))
	results = c.fetchall()
	results = results[0]
	c.execute("SELECT * from Karlstaff where theatre = %s", (venue,))
	employees = c.fetchall()
	c.execute("SELECT Karlshows2.* from Karlshows2, Karlvenues where Karlvenues.name = %s and Karlvenues.id = Karlshows2.venueID", (venue,))
	shows = c.fetchall()
	print shows
	if 'username' in session:
		return render_template('venue.html', venuedata = results, staff = employees, useron = session['username'], showdata =shows  )
	return render_template('venue.html', venuedata = results, staff = employees, useron = 'none', showdata = shows )
	
	
@app.route('/show/<show>', methods =['GET','POST'])
def show(show):
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	c.execute("SELECT * from Karlshows2 where name = %s", (show,))
	showdata = c.fetchall()
	c.execute("SELECT Karlactors.actorName, Karlcasting.role from Karlactors, Karlcasting where showID = %s and Karlactors.id = Karlcasting.actorID", (showdata[0]['id'],))
	casting = c.fetchall()
	c.execute("SELECT name from Karlvenues where id = %s", (showdata[0]['venueid'],))
	venue = c.fetchall()
	c.execute("SELECT journalist, reviewtext, publication from Karlreviews where showid = %s", (showdata[0]['id'],))
	reviews = c.fetchall()
	c.execute("SELECT reviewText from UserReviews2 where showid = %s",(showdata[0]['id'],))
	userreviews = c.fetchall()
	c.execute("SELECT rating from ShowRatings4 where showID = %s", (showdata[0]['id'],))
	results = c.fetchall()
	totalstars = 0
	for stars in results:
		totalstars = totalstars + stars['rating']
	numReviews = len(results)
	averageRating = 0
	if(numReviews) !=0:
		averageRating = float(totalstars)/float(numReviews)
		print averageRating
		averageRating = averageRating/5
		averageRating = averageRating*100
		averageRating = str(averageRating)

	if 'username' in session:
		c.execute("SELECT rating from ShowRatings4, KarlUsers where ShowRatings4.userid = KarlUsers.id and KarlUsers.username = %s and ShowRatings4.showID = %s", (session['username'],showdata[0]['id']))
		yourRating = c.fetchall()
		if len(yourRating) ==1:
			yourRating = yourRating[0]['rating']
			print yourRating
			yourRating = float(yourRating)/float(5)
			yourRating = yourRating*100
			yourRating = str(yourRating)
			return render_template('show.html', showdata = showdata,  useron = session['username'], cast = casting, venue = venue, reviews = reviews, userreviews = userreviews, rating = averageRating, yourRating = yourRating)
		return render_template('show.html', showdata = showdata,  useron = session['username'], cast = casting, venue = venue, reviews = reviews, rating = averageRating, userreviews = userreviews)
	return render_template('show.html', showdata = showdata,  useron = 'none', cast = casting, venue = venue, reviews = reviews, rating = averageRating, Userreviews = Userreviews)
	
@app.route('/profile')
def profile():
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	username = session['username']
	c.execute("SELECT id from KarlUsers where username = %s", (username,))
	userid = c.fetchall()[0]['id']
	c.execute("SELECT Karlshows2.name, reviewText, rating, to_char(ShowRatings4.time, 'HHMIA.M.DayMonthDDYYY') from UserReviews2, ShowRatings4, Karlshows2 where UserReviews2.userid = ShowRatings4.userid and ShowRatings4.userid =%s and Karlshows2.id = ShowRatings4.showid and Karlshows2.id = UserReviews2.showid", (userid,))
	results = c.fetchall()
	print results
	return render_template('profile.html', username = username, useron = username, results = results)

@app.route('/signupform')
def signupform():
	return render_template('createUser.html')
@app.route('/person/<person>', methods =['GET','POST'])
def person(person):
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	c.execute("SELECT * from Karlactors where actorName = %s", (person,))
	results = c.fetchall()
	c.execute("SELECT Karlshows2.name, Karlcasting.role from Karlshows2, Karlcasting where actorID = %s and Karlshows2.id = Karlcasting.showID", (results[0]['id'],))
	roles = c.fetchall()
	print roles
	print results
	if 'username' in session:
		return render_template('person.html', persondata = results,  useron = session['username'], roles = roles)
	return render_template('person.html', persondata = results,  useron = 'none', roles = roles)
	





@app.route('/show', methods =['GET', 'POST'])
def result():

	c = conn.cursor()


	if request.method == 'POST':
		query = request.form['city']
		print query
		query = str(query)
		c.execute("SELECT * from gigs where city = %s", (query,))
		results = c.fetchall()
		print results
		return render_template('databasetest.html', hardcode = results)
	else:
		c.execute("SELECT * from gigs")
		results = c.fetchall()
		return render_template('databasetest.html', hardcode = results)

@app.route('/submitrating', methods = ['GET', 'POST'])
def submitrating():
	show = request.args.get('show')
	rating = request.args.get('rating')
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

	c.execute("SELECT id from Karlshows2 where name = %s", (show,))
	showID = c.fetchall()
	showID = showID[0]
	showID = showID['id']
	username = session['username']
	c.execute("SELECT id from KarlUsers where username = %s", (username,))
	userid = c.fetchall()
	userid = userid[0]
	userid = userid['id']
	c.execute("DELETE from ShowRatings4 where userid = %s and showid = %s", (userid,showID))
	c.execute("SET TIME ZONE 'America/New_York'")
	c.execute("INSERT INTO ShowRatings4(userid, rating, showID, time) VALUES(%s, %s, %s, CURRENT_TIMESTAMP)", (userid, rating, showID))
	conn.commit()
	
	c.execute("SELECT rating from ShowRatings4 where showID = %s", (showID,))
	results = c.fetchall()
	totalstars = 0
	for stars in results:
		totalstars = totalstars + stars['rating']
	numReviews = len(results)
	averageRating = float(totalstars)/float(numReviews)
	print averageRating
	averageRating = averageRating/5
	averageRating = averageRating*100
	averageRating = str(averageRating)
	return averageRating

@app.route('/submitreview', methods = ['GET', 'POST'])
def submitreview():
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

	show = request.args.get('show')
	review = request.args.get('review')
	c.execute("SELECT id from Karlshows2 where name = %s", (show,))
	showID = c.fetchall()
	showID = showID[0]
	showID = showID['id']
	username = session['username']
	c.execute("SELECT id from KarlUsers where username = %s", (username,))
	userid = c.fetchall()
	userid = userid[0]
	userid = userid['id']
	c.execute("DELETE from UserReviews2 where userid = %s and showid = %s", (userid, showID))
	filepath = str(showID) + str(userid) +'.txt'

	newReview = open('static/reviews/' + filepath , 'w')
	newReview.write(review)
	newReview.close()

	c.execute("INSERT INTO UserReviews2(userid, showID, reviewText) VALUES(%s, %s, %s)", (userid, showID, filepath))
	conn.commit()
	return ""

@app.route('/ajresult')
def ajresult():
	c = conn.cursor()    
	print request.form
	query = request.args['city']
	print query
	query = str(query)
	c.execute("SELECT * from gigs where city = %s", (query,))
	results = c.fetchall()
	print results
	return render_template('table.html', hardcode = results)

app.secret_key = "\xd6'\xdf@V\xfc\xc9\\\x05\xac\x02P\xda\xa8r-\xee\xac*\xcdH\xc3\xef\x1d"

if __name__ == "__main__":
	app.run(debug =True)
