import os
import psycopg2
import psycopg2.extras
import urlparse
from flask import render_template, jsonify, Flask
from flask import request, escape, session, url_for, redirect, Markup
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


import connectionBoiler
conn = connectionBoiler.get_conn()

app = Flask(__name__)

####HOMEPAGE - checks for username in session
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT first from KarlUsers2 where id = %s", (session['username'],))
        name = c.fetchall()[0]['first']
        print name
        return render_template('homepage.html', useron=name)
    print 'kkkkk'
    return render_template('homepage.html', useron = 'none')

@app.route('/home', methods=['GET', 'POST'])
def home():
  return render_template("todayscontent.html")
###returns text for username not found


@app.route('/usernameNotFound', methods=['GET', 'POST'])
def usernameNotFound():
    return "UserName not found."

###returns text for bad password
@app.route('/passwordNotFound', methods=['GET', 'POST'])
def passwordNotFound():
    return "Password not found."

### zing sign in without facebook    
@app.route('/signin')
def signin():
  email = request.args.get('email')
  password = request.args.get('password')
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT first,id, passhash FROM KarlUsers2 where email=%s", (email,))
  data = c.fetchall()
  if data != []:
    realkey = data[0]['passhash']
    userid = data[0]['id']
  else:
    return "Email not found"
  if security.check_password_hash(realkey, password):
    session['username'] = userid
    return render_template("todayscontent.html", useron = data[0]['first'])
  return "Incorrect Password"

#### this takes automatic facebook login and uses it to automatically log the user into zing session
@app.route('/login', methods=['GET', 'POST'])
def login():
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    email = request.args.get('email')
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT first,id, passhash FROM KarlUsers2 where email=%s", (email,))
    data = c.fetchall()
    if len(data) > 0:
      realkey = data[0]['passhash']
      userid = data[0]['id']
    else:
        return render_template("zingsignin.html", email = email)
    print data
    session['username'] = userid
    return "logged in"

###logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

### response to a facebook sign in, either logs existing user in or prompts them to create an account with email and password
@app.route('/facebookcreateform', methods=['GET', 'POST'])
def fbcreateform():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  email = str(request.args.get('email'))
  firstname = str(request.args.get('firstname'))
  c.execute("SELECT * from KarlUsers2 where email = %s",(email,))
  testemail = c.fetchall()
  print testemail
  if testemail != []:
    userid = testemail[0]['id']
    session['username'] = userid
    return render_template("todayscontent.html", useron = firstname)
  lastname = str(request.args.get('lastname'))
  template_vars = {"email": email,
                   "first": firstname,
                   "last": lastname}
  return render_template("zingsignin.html", **template_vars)

#### creates account
@app.route('/facebookcreate', methods=['GET', 'POST'])
def fbcreate():
    c = conn.cursor()
    firstname = str(request.args.get('firstname'))
    lastname = str(request.args.get('lastname'))
    email = str(request.args.get('email'))
    password = request.args.get('password')
    c.execute("SELECT * from KarlUsers2 where email = %s", (email,))
    testemail = c.fetchall()
    if testemail != []:
        return "We already have an account for that email."
    fullname = firstname + lastname
    you = User(fullname, password)
    passhash = you.pw_hash
    c.execute("""INSERT INTO KarlUsers2(first, last, email, passhash)
                    VALUES (%s, %s, %s, %s)""",
                  (firstname, lastname, email, passhash))
    conn.commit()
    c.execute("SELECT id FROM KarlUsers2 ORDER BY id DESC LIMIT 1")
    userid = c.fetchall()[0][0]
    username = firstname + str(userid)
    session['username'] = userid
    return render_template('usersurvey.html', firstname=firstname)


@app.route('/newUser', methods=['GET', 'POST'])
def newUser():
    return render_template('newUser.html', useron='none')


@app.route('/usercreate', methods=['GET', 'POST'])
def usercreate():
    c = conn.cursor()
    firstname = str(request.args.get('firstname'))
    lastname = str(request.args.get('lastname'))
    email = str(request.args.get('email'))
    password = request.args.get('password')
    passwordConfirm = request.args.get('passwordConfirm')
    month = str(request.args.get('month'))
    day = str(request.args.get('day'))
    year = str(request.args.get('year'))
    birthday = month + " " + day + " " + year
    c.execute("SELECT * from KarlUsers2 where email = %s", (email,))
    testemail = c.fetchall()
    if testemail != []:
        return "We already have an account for that email."
    if password == passwordConfirm:
        fullname = firstname + lastname
        you = User(fullname, password)
        passhash = you.pw_hash
        c.execute("""INSERT INTO KarlUsers2(first, last, email, passhash, dob)
                    VALUES (%s, %s, %s, %s, %s)""",
                  (firstname, lastname, email, passhash, birthday))
        conn.commit()
        c.execute("SELECT id FROM KarlUsers2 ORDER BY id DESC LIMIT 1")
        userid = c.fetchall()[0][0]
        username = firstname + str(userid)
        session['username'] = userid
        return render_template('usersurvey.html', firstname=firstname)
    else:
        return "Passwords do not match."


@app.route('/venues')
def venues():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT name from Fringevenues")
    results = c.fetchall()
    newResults = []
    print results
    return render_template('all_venues.html', results=results)

# def trending(list):
#   newList = []
#   for x in list:
#     temp = x[0]
#     if temp > top:



@app.route('/nowPlaying')
def nowPlaying():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # c.execute("""SELECT Karlshows2.name, SUM(rating), COUNT(rating)
    #              from Karlshows2, ShowRatings4
    #              WHERE (CURRENT_DATE, CURRENT_DATE)
    #              OVERLAPS (start_date, end_date)
    #              and ShowRatings4.showid = Karlshows2.id
    #              GROUP BY Karlshows2.name""")
    c.execute("""SELECT Fringeshows.id,Fringeshows.name, SUM(rating), COUNT(rating)
                 from Fringeshows, ShowRatings4
                 WHERE ShowRatings4.showid = Fringeshows.id
                 GROUP BY Fringeshows.name, Fringeshows.id""")
    showresults = c.fetchall()
    c.execute("SELECT COUNT(*), showid from ShowRatings4 where CURRENT_TIMESTAMP-time < INTERVAL '24 hours' GROUP BY showid")
    recentresults = c.fetchall()
   
    
    results = []
    for x in range(len(showresults)):
        result = []
        recentAction = False
        for y in recentresults:
          if showresults[x]['id'] == y['showid']:
            result.append(y['count'])
            recentAction = True
        if not(recentAction):
          result.append(0)
          
        
        result.append(showresults[x]['name'])
        
        averageRating = float(showresults[x]['sum'])/float(showresults[x]['count'])
        print convert_to_percent(averageRating)
        result.append(convert_to_percent(averageRating))
        
        results.append(result)
        
    print results


    return render_template('nowPlaying.html', results=results)




@app.route('/comingsoon')
def comingsoon():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # c.execute("""SELECT Karlshows2.name, SUM(rating), COUNT(rating)
    #              from Karlshows2, ShowRatings4
    #              WHERE (CURRENT_DATE, CURRENT_DATE)
    #              OVERLAPS (start_date, end_date)
    #              and ShowRatings4.showid = Karlshows2.id
    #              GROUP BY Karlshows2.name""")
    showcount = 0 
    iterator = 0
    results = []
    while showcount < 10:
      c.execute("""SELECT Fringeshows.name, playing, ticketlink,to_char(playingdate,'Day'), Fringeshows.id from Fringeshows, Fringedates where Fringedates.showid = Fringeshows.id and playingdate = CURRENT_DATE + %s""", (iterator,))
      showresults = c.fetchall()
      doubles = False
      nilreturn = False
      if showresults == []:
        nilreturn = True

      for x in range(len(showresults)):
         if len(results) < 10:
           result = []
           playing = showresults[x]['playing']
           pm = playing.rfind(" ") 
           playing = playing[pm:]
           result.append(playing)
           result.append(showresults[x]['name'])
           c.execute("SELECT SUM(rating), COUNT(rating) from ShowRatings4 where showid = %s", (showresults[x]['id'],))
           ratingResults = c.fetchall()
           if ratingResults[0]['sum'] != None:
              averageRating = float(ratingResults[0]['sum'])/float(ratingResults[0]['count'])
              result.append(convert_to_percent(averageRating))
           else:
              result.append("50.0")
           result.append(showresults[x]['to_char'])
           result.append(showresults[x]['ticketlink'])
           already =False
           for y in results:
              if showresults[x]['name'] in y:
                already = True
           if already:
              pass
              doubles = True
           else:
              results.append(result)
      iterator = iterator +1
      showcount = len(results)


    dates = []
    for x in results:
        date = x[3]
        print x[2]
        if date in dates:
          pass
        else:
          dates.append(date)
  
    alldates = []
    print results
 

    # datedata = {}
    # for x in dates: 
    #   daydata = []
    #   for y in results:
    #     if len(y) == 4:
    #       date = y[3]
    #     else: 
    #       date = y[2]
    #     if date == x:
    #       daydata.append(y)
    #   datedata[x] = daydata
    # print datedata


      
        



    return render_template('comingsoon.html', results=results, dates = dates, alldates = alldates)
 


@app.route('/venue', methods=['GET', 'POST'])
def venue():
    venue = request.args.get('venue')
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * from Fringevenues where name = %s", (venue,))
    results = c.fetchall()
    results = results[0]
    c.execute("SELECT * from Karlstaff where theatre = %s", (venue,))
    employees = c.fetchall()
    c.execute("""SELECT name from Fringeshows
                 where venueid = %s """, (results['id'],))
    shows = c.fetchall()
   
    if 'username' in session:
      c.execute("SELECT first from KarlUsers2 where id = %s", (session['username'],))
      name = c.fetchall()[0]['first']
      return render_template('venue.html', venuedata=results,
                               staff=employees, useron=name,
                               showdata=shows)
    return render_template('venue.html', venuedata=results,
                           staff=employees, useron='none',
                           showdata=shows)

def convert_to_percent(stars):
    percent = stars/5
    percent = percent*100
    percent = str(percent)
    return percent


@app.route('/show/Antigone Sr./Twenty Looks or Paris is Burning at the Judson Church (L)', methods=['GET', 'POST'])
def antigone():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    show = "Antigone Sr./Twenty Looks or Paris is Burning at the Judson Church (L)"
    if show == "What Good Has Come Out of Camden":
      show = show + "?"
    c.execute("SELECT * from Fringeshows where name = %s", (show,))
    showdata = c.fetchall()
    print showdata
    if len(showdata)>0:
      c.execute("""SELECT Karlactors.actorName, Karlcasting.role
                from Karlactors, Karlcasting
                where showID = %s and Karlactors.id = Karlcasting.actorID""",
                (showdata[0]['id'],))
      casting = c.fetchall()
      c.execute("""SELECT name from Fringevenues
                where id = %s""", (showdata[0]['venueid'],))
      venue = c.fetchall()
      c.execute("""SELECT journalist, reviewtext, publication
                from Karlreviews
                where showid = %s""", (showdata[0]['id'],))
      reviews = c.fetchall()
      c.execute("""SELECT reviewText from UserReviews2
                where showid = %s""", (showdata[0]['id'],))
      userreviews = c.fetchall()
      c.execute("""SELECT rating from ShowRatings4
                where showID = %s""", (showdata[0]['id'],))
      results = c.fetchall()
      c.execute("""SELECT * from Fringedates 
                where showid = %s""", (showdata[0]['id'],))
      dates= c.fetchall()
      print dates
      totalstars = sum([stars['rating'] for stars in results])
      numReviews = len(results)
      averageRating = 0
      yourRating = 0
      description = showdata[0]['description']
      if "<p>" in description:
        description = Markup(description)
      template_vars = {"showdata": showdata[0],
                       "description": description,
                       "useron": 'none',
                       "cast": casting, "venue": venue,
                       "reviews": reviews,
                       "userreviews": userreviews,
                       "rating": averageRating,
                       "yourRating": yourRating,
                       "dates": dates
                       }
      if(numReviews) != 0:
          averageRating = float(totalstars)/float(numReviews)
          template_vars['rating'] = convert_to_percent(averageRating)
      if 'username' in session:
          c.execute("""SELECT rating
                    from ShowRatings4, KarlUsers2
                    where ShowRatings4.userid = KarlUsers2.id
                    and KarlUsers2.id = %s
                    and ShowRatings4.showID = %s""",
                    (session['username'], showdata[0]['id']))
          yourRating = c.fetchall()
          if len(yourRating) == 1:
              yourRating = yourRating[0]['rating']
              yourRating = convert_to_percent(yourRating)
          c.execute("SELECT first from KarlUsers2 where id = %s", (session['username'],))
          name = c.fetchall()[0]['first']
          print name
          template_vars['useron'] = name    
      return render_template("nellie.html", **template_vars)
    return render_template("error.html")

@app.route('/show/Nellie/Nellie', methods=['GET', 'POST'])
def nellie():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    show = "Nellie/Nellie"
    if show == "What Good Has Come Out of Camden":
      show = show + "?"
    c.execute("SELECT * from Fringeshows where name = %s", (show,))
    showdata = c.fetchall()
    print showdata
    if len(showdata)>0:
      c.execute("""SELECT Karlactors.actorName, Karlcasting.role
                from Karlactors, Karlcasting
                where showID = %s and Karlactors.id = Karlcasting.actorID""",
                (showdata[0]['id'],))
      casting = c.fetchall()
      c.execute("""SELECT name from Fringevenues
                where id = %s""", (showdata[0]['venueid'],))
      venue = c.fetchall()
      c.execute("""SELECT journalist, reviewtext, publication
                from Karlreviews
                where showid = %s""", (showdata[0]['id'],))
      reviews = c.fetchall()
      c.execute("""SELECT reviewText from UserReviews2
                where showid = %s""", (showdata[0]['id'],))
      userreviews = c.fetchall()
      c.execute("""SELECT rating from ShowRatings4
                where showID = %s""", (showdata[0]['id'],))
      results = c.fetchall()
      c.execute("""SELECT * from Fringedates 
                where showid = %s""", (showdata[0]['id'],))
      dates= c.fetchall()
      print dates
      totalstars = sum([stars['rating'] for stars in results])
      numReviews = len(results)
      averageRating = 0
      yourRating = 0
      description = showdata[0]['description']
      if "<p>" in description:
        description = Markup(description)
      template_vars = {"showdata": showdata[0],
                       "description": description,
                       "useron": 'none',
                       "cast": casting, "venue": venue,
                       "reviews": reviews,
                       "userreviews": userreviews,
                       "rating": averageRating,
                       "yourRating": yourRating,
                       "dates": dates
                       }
      if(numReviews) != 0:
          averageRating = float(totalstars)/float(numReviews)
          template_vars['rating'] = convert_to_percent(averageRating)
      if 'username' in session:
          c.execute("""SELECT rating
                    from ShowRatings4, KarlUsers2
                    where ShowRatings4.userid = KarlUsers2.id
                    and KarlUsers2.id = %s
                    and ShowRatings4.showID = %s""",
                    (session['username'], showdata[0]['id']))
          yourRating = c.fetchall()
          if len(yourRating) == 1:
              yourRating = yourRating[0]['rating']
              yourRating = convert_to_percent(yourRating)
          c.execute("SELECT first from KarlUsers2 where id = %s", (session['username'],))
          name = c.fetchall()[0]['first']
          print name
          template_vars['useron'] = name    
      return render_template("nellie.html", **template_vars)
    return render_template("error.html")


@app.route('/show', methods=['GET', 'POST'])
def show():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    show = request.args.get('show')
    if show == "What Good Has Come Out of Camden":
      show = show + "?"
    if show == "The Ray Charles Experience  Live!":
      show = show + " "
    c.execute("SELECT * from Fringeshows where name = %s", (show,))
    showdata = c.fetchall()
    
    if len(showdata)>0:
      c.execute("""SELECT Karlactors.actorName, Karlcasting.role
                from Karlactors, Karlcasting
                where showID = %s and Karlactors.id = Karlcasting.actorID""",
                (showdata[0]['id'],))
      casting = c.fetchall()
      c.execute("""SELECT name from Fringevenues
                where id = %s""", (showdata[0]['venueid'],))
      venue = c.fetchall()
      c.execute("""SELECT journalist, reviewtext, publication
                from Karlreviews
                where showid = %s""", (showdata[0]['id'],))
      reviews = c.fetchall()
      c.execute("""SELECT reviewText from UserReviews2
                where showid = %s""", (showdata[0]['id'],))
      userreviews = c.fetchall()
      c.execute("""SELECT rating from ShowRatings4
                where showID = %s""", (showdata[0]['id'],))
      results = c.fetchall()
      c.execute("""SELECT * from Fringedates 
                where showid = %s""", (showdata[0]['id'],))
      dates= c.fetchall()
      
      totalstars = sum([stars['rating'] for stars in results])
      numReviews = len(results)
      averageRating = 0
      yourRating = 0
      description = showdata[0]['description']
      producer = showdata[0]['producer']
      producer = Markup(producer)
      if "<p>" in description:
        description = Markup(description)
      template_vars = {"showdata": showdata[0],
                      "producer": producer,
                       "description": description,
                       "useron": 'none',
                       "cast": casting, "venue": venue,
                       "reviews": reviews,
                       "userreviews": userreviews,
                       "rating": averageRating,
                       "yourRating": yourRating,
                       "dates": dates
                       }

      if(numReviews) != 0:
          averageRating = float(totalstars)/float(numReviews)
          template_vars['rating'] = convert_to_percent(averageRating)
      if 'username' in session:
          c.execute("""SELECT rating
                    from ShowRatings4, KarlUsers2
                    where ShowRatings4.userid = KarlUsers2.id
                    and KarlUsers2.id = %s
                    and ShowRatings4.showID = %s""",
                    (session['username'], showdata[0]['id']))
          yourRating = c.fetchall()
          if len(yourRating) == 1:
              yourRating = yourRating[0]['rating']
              yourRating = convert_to_percent(yourRating)
          c.execute("SELECT first from KarlUsers2 where id = %s", (session['username'],))
          name = c.fetchall()[0]['first']
         
          template_vars['useron'] = name    
      return render_template("show.html", **template_vars)
    return render_template("error.html")

@app.route('/profile')
def profile():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    username = session['username']
    c.execute("SELECT id from KarlUsers2 where username = %s", (username,))
    userid = c.fetchall()[0]['id']
    c.execute("""SELECT Karlshows2.name, reviewText, rating,
              to_char(ShowRatings4.time, 'HHMIA.M.DayMonthDDYYY')
              from UserReviews2, ShowRatings4, Karlshows2
              where UserReviews2.userid = ShowRatings4.userid
              and ShowRatings4.userid =%s
              and Karlshows2.id = ShowRatings4.showid
              and Karlshows2.id = UserReviews2.showid""",
              (userid,))
    results = c.fetchall()
    print results
    return render_template('profile.html',
                           username=username,
                           useron=username,
                           results=results)


@app.route('/signupform')
def signupform():
    return render_template('createUser.html')

@app.route('/signinform')
def signinform():
    return render_template('signin.html')


@app.route('/person/<person>', methods=['GET', 'POST'])
def person(person):
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT * from Karlactors
              where actorName = %s""",
              (person,))
    results = c.fetchall()
    c.execute("""SELECT Karlshows2.name, Karlcasting.role
              from Karlshows2, Karlcasting
              where actorID = %s
              and Karlshows2.id = Karlcasting.showID""",
              (results[0]['id'],))
    roles = c.fetchall()
    print roles
    print results
    if 'username' in session:
        return render_template('person.html',
                               persondata=results,
                               useron=session['username'],
                               roles=roles)
    return render_template('person.html',
                           persondata=results,
                           useron='none',
                           roles=roles)


@app.route('/autocomplete/allshows', methods=['GET', 'POST'] )
def autocomplete():
  query = request.args.get('query')
  print query
  query = '%' + query + '%'
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT name from Fringeshows
            where name LIKE %s""", (query,))
  results = c.fetchall()
  print results
  jsonresults = []
  for result in results:
     jsonresults.append(result['name'])
  print jsonresults
  return jsonify(query = "Unit", suggestions = jsonresults)



@app.route('/submitrating', methods=['GET', 'POST'])
def submitrating():
    show = request.args.get('show')
    rating = request.args.get('rating')
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT id from Fringeshows
              where name = %s""", (show,))
    showID = c.fetchall()
    showID = showID[0]
    showID = showID['id']
    userid = session['username']
    c.execute("""DELETE from ShowRatings4
              where userid = %s and showid = %s""",
              (userid, showID))
    c.execute("SET TIME ZONE 'America/New_York'")
    c.execute("""INSERT INTO ShowRatings4(userid, rating, showID, time)
              VALUES(%s, %s, %s, CURRENT_TIMESTAMP)""",
              (userid, rating, showID))
    conn.commit()
    c.execute("""SELECT rating from ShowRatings4
              where showID = %s""", (showID,))
    results = c.fetchall()
    totalstars = 0
    for stars in results:
        totalstars = totalstars + stars['rating']
    numReviews = len(results)
    averageRating = float(totalstars)/float(numReviews)
    averageRating = convert_to_percent(averageRating)
    return averageRating


@app.route('/submitreview', methods=['GET', 'POST'])
def submitreview():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    show = request.args.get('show')
    review = request.args.get('review')
    c.execute("""SELECT id from Fringeshows
              where name = %s""", (show,))
    showID = c.fetchall()
    showID = showID[0]
    showID = showID['id']
    userid = session['username']
    c.execute("""DELETE from UserReviews2
              where userid = %s and showid = %s""",
              (userid, showID))
    if "/" in show:
      slash = show.find("/")
      show = show[:slash]
    filepath = str(showID)+str(userid)+str(show) + str(userid)+'.txt'
    newReview = open('static/reviews/' + filepath, 'w')
    newReview.write(review)
    newReview.close()
    c.execute("""INSERT INTO UserReviews2(userid, showID, reviewText)
              VALUES(%s, %s, %s)""", (userid, showID, filepath))
    conn.commit()
    return ""


app.secret_key = """\xd6'\xdf@V\xfc\xc9\\\x05\xac
                 \x02P\xda\xa8r-\xee\xac*\xcdH\xc3\xef\x1d"""

if __name__ == "__main__":
    app.run(debug=True)
