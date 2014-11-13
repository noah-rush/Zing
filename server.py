import os
import psycopg2
import psycopg2.extras
import urlparse
from flask import render_template, jsonify, Flask
from flask.ext.mail import Mail
from flask.ext.mail import Message
from flask import request, escape, session, url_for, redirect, Markup, Response
import sys
from werkzeug.security import generate_password_hash, \
    check_password_hash
from werkzeug import security
import json
from twitter import *
from itsdangerous import URLSafeTimedSerializer
ts = URLSafeTimedSerializer("""\xd6'\xdf@V\xfc\xc9\\\x05\xac
                 \x02P\xda\xa8r-\xee\xac*\xcdH\xc3\xef\x1d""")


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

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'noah@codearium.com',
    MAIL_PASSWORD = 'tomato777',
))

mail = Mail(app)

####HOMEPAGE - checks for username in session

def convertDate(date):
        strlength = len(date)
        print date
        day = date[:date.find("y")+1]
        month = date[date.find("ber")-6:strlength-6]
        numday = date[strlength-6: strlength-4]
        year = date[ strlength-4:]
        if  numday.find("0") == 0:
          numday = numday[1:]
      

        playingdate = day + ", " + month + " " + numday +" " + year
        print playingdate
        return playingdate

@app.route('/', methods=['GET', 'POST'])
def index():
 
    if 'username' in session:
        
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT first from ZINGUSERS where id = %s", (session['username'],))
        name = c.fetchall()[0]['first']
        print name
       
        c.execute("SELECT id from ZINGADMIN where userid = %s",(session['username'],));
        adminID = c.fetchall();
        if len(adminID)>0:
              return render_template('layout.html', useron=name, adminPrivileges=True)
        return render_template('layout.html', useron=name, adminPrivileges=False)
    print 'kkkkk'
    return render_template('layout.html', useron = 'none', adminPrivileges=False)

@app.route('/home', methods=['GET', 'POST'])
def home():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT * from ZINGPOSTS ORDER BY id DESC")
  blog = c.fetchall()
  
  for post in blog:
    post['descript'] = Markup(post['descript'])
    c.execute("""SELECT ZINGSHOWS.name, ZINGSHOWS.id FROM ZINGSHOWS, ZINGARTICLESHOWTAGS 
                 WHERE ZINGSHOWS.id = ZINGARTICLESHOWTAGS.showid
                 AND ZINGARTICLESHOWTAGS.articleid = %s""", (post['id'],))
    tags = c.fetchall()
    post['tags'] = tags
   
  print blog
  return render_template("newHomepage.html", blog = blog)
###returns text for username not found

@app.route('/post', methods=['GET', 'POST'])
def post():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  articleid = request.args.get('id')
  c.execute("SELECT * from ZINGPOSTS where id = %s", (articleid,))
  article = c.fetchall()
  print article
  article = article[0]
  c.execute("""SELECT ZINGSHOWS.name, ZINGSHOWS.id, ZINGSHOWS.venueid FROM ZINGSHOWS, ZINGARTICLESHOWTAGS 
                 WHERE ZINGSHOWS.id = ZINGARTICLESHOWTAGS.showid
                 AND ZINGARTICLESHOWTAGS.articleid = %s""", (article['id'],))
  tags = c.fetchall()
  for tag in tags:
    c.execute("SELECT name from ZINGVENUES where id = %s", (tag['venueid'],))
    venue = c.fetchall()[0]['name']
    tag['venue'] = venue
  article['tags'] = tags
  
  filename = article['article']
  text = open('static/Posts/'+filename, 'r')
  a = text.read()
  
  article['article'] = Markup(a)
  firstparagraph = article['article'][:article['article'].find("</p>")+4]
  firstparagraph = Markup(firstparagraph)
  article['article'] = article['article'][article['article'].find("</p>")+4:]
  article['article'] = Markup(article['article'])
  text.close()
  print article
  return render_template("post.html", article = article, firstparagraph = firstparagraph)
###returns text for username not found

@app.route('/edit', methods=['GET', 'POST'])
def edit():
  return render_template("editor.html")


@app.route('/about', methods=['GET', 'POST'])
def about():
  return render_template("about.html")

@app.route('/photo', methods=[ 'POST'])
def photo():
    try:
       
        files = request.files
        print files

        uploaded_files = _handleUpload(files)

        return jsonify({'files': uploaded_files})
    except:
        raise
        return jsonify({'status': 'error'})

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
  extension = filename[filename.find('.')+1:]
  print extension
  allowed = False
  for exts in ALLOWED_EXTENSIONS:
    if extension == exts:
      allowed = True
  return allowed


def _handleUpload(files):
    if not files:
       return None
    filenames = []
    saved_files_urls = []
    for key, file in files.iteritems():
        if file and allowed_file(file.filename):
            filename = file.filename
            print os.path.join(UPLOAD_FOLDER, filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filenames.append("%s" % (file.filename))
            

    return filenames

### zing sign in without facebook    
@app.route('/signin')
def signin():
  email = request.args.get('email')
  password = request.args.get('password')
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT first,id, passhash FROM ZINGUSERS where email=%s", (email,))
  data = c.fetchall()
  if data != []:
    realkey = data[0]['passhash']
    userid = data[0]['id']
  else:
    return "Email not found"
  if realkey == None:
    return "Please Login with Facebook"
  else:
    if security.check_password_hash(realkey, password):
      session['username'] = userid
      return "USER LOGIN" + testemail[0]['first']
  return "Incorrect Password"

@app.route('/contentPost')
def contentPost():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  title = request.args.get('title')
  author = request.args.get('author')
  article = request.args.get('article')
  tags = json.loads(request.args.get('tags'))
  descript = request.args.get('descript')
  photo = request.args.get('photo')
  filepath = str(title)+str(author)+'.txt'
  newReview = open('static/Posts/' + filepath, 'w')
  newReview.write(article)
  newReview.close()
  c.execute("""INSERT INTO ZINGPOSTS(author, userid,title,article,pic, descript, date) 
            VALUES(%s,%s,%s,%s,%s, %s, CURRENT_DATE) RETURNING id""", (author, session['username'], title, filepath, photo, descript))
  articleid = c.fetchall()[0]['id'];
  conn.commit()
  for tag in tags:
    c.execute("SELECT id from ZINGSHOWS where name = %s", (tag,))
    showid = c.fetchall()[0]['id']
    c.execute("INSERT INTO ZINGARTICLESHOWTAGS(articleid, showid) VALUES(%s,%s)", (articleid, showid))
  conn.commit()
  return "aok"






#### this takes automatic facebook login and uses it to automatically log the user into zing session

###logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/facebookcreateform', methods=['GET', 'POST'])
def fbcreateform():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  email = str(request.args.get('email'))
  firstname = str(request.args.get('firstname'))
  lastname = str(request.args.get('lastname'))
  c.execute("SELECT * from ZINGUSERS where email = %s",(email,))
  testemail = c.fetchall()
  print testemail
  if testemail != []:
    userid = testemail[0]['id']
    session['username'] = testemail[0]['id']
    return "USER LOGIN" + testemail[0]['first']
  lastname = str(request.args.get('lastname'))
  c.execute("""INSERT INTO ZINGUSERS(first, last, email)
                    VALUES (%s, %s, %s)""",
                  (firstname, lastname, email))
  conn.commit()
  return "NEW USER CREATED" + firstname


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)
    
    print email
    print "quackquack"
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("UPDATE ZINGUSERS SET emailconfirm = True WHERE email = %s", (email,))
    conn.commit()
    c.execute("SELECT id FROM ZINGUSERS WHERE email = %s", (email,))
    userid = c.fetchall()[0]['id']
    print userid
    session['username'] = userid
    return redirect(url_for('index'))


@app.route('/zingnewuser', methods=['GET', 'POST'])
def zingnewuser():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  email = str(request.args.get('email'))
  firstname = str(request.args.get('firstname'))
  lastname = str(request.args.get('lastname'))
  password = str(request.args.get('password'))
  c.execute("SELECT * from ZINGUSERS where email = %s",(email,))
  testemail = c.fetchall()
  if testemail != []:
    userid = testemail[0]['id']
    session['username'] = testemail[0]['id']
    return "EMAIL FOUND" + testemail[0]['first']
  fullname = firstname + lastname
  you = User(fullname, password)
  passhash = you.pw_hash
  c.execute("""INSERT INTO ZINGUSERS(first, last, email, passhash)
                VALUES (%s, %s, %s, %s)""",
                (firstname, lastname, email, passhash))
  conn.commit()
  token = ts.dumps(email, salt='email-confirm-key')
  confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True)
  html = render_template(
            'email/activate.html',
            confirm_url=confirm_url)
  msg = Message("Welcome to Zing",
                  sender="noah@codearium.com",
                  recipients=[email])
  msg.html = html
  mail.send(msg)

  
  return "NEW USER CREATED" + firstname






# def trending(list):
#   newList = []
#   for x in list:
#     temp = x[0]
#     if temp > top:


@app.route('/zingDescript')
def zingDescript():
  return render_template('zingdescription.html')

@app.route('/nowPlaying')
def nowPlaying():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # c.execute("""SELECT Karlshows2.name, SUM(rating), COUNT(rating)
    #              from Karlshows2, ShowRatings4
    #              WHERE (CURRENT_DATE, CURRENT_DATE)
    #              OVERLAPS (start_date, end_date)
    #              and ShowRatings4.showid = Karlshows2.id
    #              GROUP BY Karlshows2.name""")
    c.execute("""SELECT ZINGSHOWS.id,ZINGSHOWS.name, SUM(rating), COUNT(rating)
                 from ZINGSHOWS, ZINGRATINGS
                 WHERE ZINGRATINGS.showid = ZINGSHOWS.id
                 GROUP BY ZINGSHOWS.name, ZINGSHOWS.id""")
    showresults = c.fetchall()
    c.execute("SELECT COUNT(*), showid from ZINGRATINGS where CURRENT_TIMESTAMP-time < INTERVAL '24 hours' GROUP BY showid")
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



def sort_array(s):
    for i in range(1, len(s)):
        val = s[i]
        j = i - 1
        while (j >= 0) and (s[j]['avg'] < val['avg']):
            s[j+1] = s[j]
            j = j - 1
        s[j+1] = val
    return s


@app.route('/toprated')
def toprated():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT ZINGSHOWS.name, SUM(rating), COUNT(rating) from ZINGRatings, ZINGSHOWS WHERE ZINGSHOWS.id = ZINGRATINGS.showid GROUP BY ZINGSHOWS.name")
  results = c.fetchall()
  print results
  sortedResults = []
  for result in results:
    avg = float(result['sum'])/float(result['count'])
    print avg
    temp = {"avg": avg, "name": result['name']}
    sortedResults.append(temp)
  
  sortedResults = sort_array(sortedResults)
  for tops in sortedResults:
    tops['avg'] = convert_to_percent(tops['avg'])
  print sortedResults
  return render_template('toprated.html', results = sortedResults)

@app.route('/comingsoon')
def comingsoon():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT name, id
                 from ZINGSHOWS
                 WHERE (start,enddate)
                 OVERLAPS (CURRENT_DATE, CURRENT_DATE)
               """)
    results = c.fetchall()
    

   

    for result in results:
      showid = result['id']
      c.execute("SELECT SUM(rating), COUNT(rating), showid FROM ZINGRATINGS WHERE showid = %s GROUP BY showid", (showid,))
      ratings = c.fetchall()
      rating = ''
      if len(ratings) > 0:
        rating = float(ratings[0]['sum'])/float(ratings[0]['count'])
        rating = convert_to_percent(rating)
      result["rating"] = rating

    # while showcount < 10:
    #   c.execute("""SELECT ZINGSHOWS.name, playing, ticketlink,to_char(playingdate,'Day'), ZINGSHOWS.id from ZINGSHOWS, Fringedates2 where Fringedates2.showid = ZINGSHOWS.id and playingdate = CURRENT_DATE + %s""", (iterator,))
    #   showresults = c.fetchall()
    #   doubles = False
    #   nilreturn = False
    #   if showresults == []:
    #     nilreturn = True

    #   for x in range(len(showresults)):
    #      if len(results) < 10:
    #        result = []
    #        playing = showresults[x]['playing']
    #        pm = playing.rfind(" ") 
    #        playing = playing[pm:]
    #        result.append(playing)
    #        result.append(showresults[x]['name'])
    #        c.execute("SELECT SUM(rating), COUNT(rating) from ShowRatings4 where showid = %s", (showresults[x]['id'],))
    #        ratingResults = c.fetchall()
    #        if ratingResults[0]['sum'] != None:
    #           averageRating = float(ratingResults[0]['sum'])/float(ratingResults[0]['count'])
    #           result.append(convert_to_percent(averageRating))
    #        else:
    #           result.append("none")
    #        result.append(showresults[x]['to_char'])
    #        result.append(showresults[x]['ticketlink'])
    #        already =False
    #        for y in results:
    #           if showresults[x]['name'] in y:
    #             already = True
    #        if already:
    #           pass
    #           doubles = True
    #        else:
    #           results.append(result)
    #   iterator = iterator +1
    #   showcount = len(results)


    # dates = []
    # for x in results:
    #     date = x[3]
    #     print x[2]
    #     if date in dates:
    #       pass
    #     else:
    #       dates.append(date)
  
    # alldates = []
    # print results
 

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
    return render_template('comingsoon.html', results=results)

      
        



    # return render_template('comingsoon.html', results=results, dates = dates, alldates = alldates)
 
@app.route('/fullschedule')
def fullschedule():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # c.execute("""SELECT Karlshows2.name, SUM(rating), COUNT(rating)
    #              from Karlshows2, ShowRatings4
    #              WHERE (CURRENT_DATE, CURRENT_DATE)
    #              OVERLAPS (start_date, end_date)
    #              and ShowRatings4.showid = Karlshows2.id
    #              GROUP BY Karlshows2.name""")
    c.execute("SELECT * FROM ZINGSHOWS ORDER BY start")
    results = c.fetchall()
    print results
    months = {"01": "January ",
              "02": "February ",
              "03": "March ",
              "04": "April ",
              "05": "May ",
              "06": "June ",
              "07": "July ", 
              "08": "August ",
              "09": "September ", 
              "10": "October ", 
              "11": "November ", 
              "12": "December "}
    for result in results:
      result['name'] = Markup(result['name'])
      result['start'] = str(result['start'])
      result['enddate'] = str(result['enddate'])
      monthfirst = result['start'].find("-")
      monthlast = result['start'].rfind("-")
      month = result['start'][monthfirst+1:monthlast]
      day = result['start'][monthlast+1:]
      year = result['start'][:4]
      if day[0] == "0":
        day = day[1:]
      result['start'] = months[month] + day 
      monthfirst = result['enddate'].find("-")
      monthlast = result['enddate'].rfind("-")
      month = result['enddate'][monthfirst+1:monthlast]
      day = result['enddate'][monthlast+1:]
      if day[0] == "0":
        day = day[1:]
      year = result['enddate'][:4]
      result['enddate'] = months[month] + day + ", " +  year
 
    return render_template('fullschedule.html', results=results)


@app.route('/yelp')
def yelp():
  from geopy.geocoders import GoogleV3
  geolocator = GoogleV3()

  lat = request.args.get('lat')
  lng = request.args.get('lng')
  latlng = lat + ","+lng
  import yelp
  response = yelp.main(lat,lng)
  businesses = response[0]['businesses']
  print businesses
  results = []
  for business in businesses:
    result = []
    print business['name']
    result.append(business['name'])
    location =  business['location']
    if 'coordinate' in location.keys():
      print location['coordinate']
      result.append(location['coordinate']['latitude'])
      result.append(location['coordinate']['longitude'])
    else:
      if len(location['display_address'])>2:
        displayAddress = location['display_address'][0] + " " + location['display_address'][2]  
      else: 
        displayAddress = location['display_address'][0] 
      address, (latitude, longitude) = geolocator.geocode(displayAddress)
      result.append(latitude)
      result.append(longitude)
    results.append(result)
  results= json.dumps(results)
  print results
  return results




@app.route('/venue', methods=['GET', 'POST'])
def venue():
    venue = request.args.get('venue')
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * from ZINGVENUES where id = %s", (venue,))
    results = c.fetchall()
    results = results[0]
    c.execute("SELECT * from Karlstaff where theatre = %s", (results['name'],))
    employees = c.fetchall()
    c.execute("""SELECT name from ZINGSHOWS
                 where venueid = %s """, (venue,))
    shows = c.fetchall()
    if 'username' in session:
      c.execute("SELECT first from ZINGUSERS where id = %s", (session['username'],))
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


@app.route('/show', methods=['GET', 'POST'])
def show():
    
    t = Twitter(
    auth=OAuth('2290030034-qZlpLizAAp8FqA21jumX3sWKmKc2VVAHAPw9nUZ', 'I7B4ALWQQLTNYQKzu37tKahle36JL9NsWT3RkCYCKWx2i', '8ddlpAyOG5fq2qCHoJcxQ', 'tbjoqSMYMOxKyJgeqpZ1EexqCxoOsm4OYwiizshtZY4'))
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    show = request.args.get('show')
    c.execute("SELECT * from ZINGSHOWS where id = %s", (show,))
    showdata = c.fetchall()
    tweets = t.search.tweets(q="#"+showdata[0]['name'])
    print tweets['search_metadata']
    for tweet in tweets['statuses']:
      print "/n"
      print tweet['text']
    if len(showdata)>0:
      # c.execute("""SELECT Karlactors.actorName, Karlcasting.role
      #           from Karlactors, Karlcasting
      #           where showID = %s and Karlactors.id = Karlcasting.actorID""",
      #           (showdata[0]['id'],))
      casting = c.fetchall()
      c.execute("""SELECT name from ZINGVENUES
                where id = %s""", (showdata[0]['venueid'],))
      venue = c.fetchall()
      c.execute("""SELECT reviewText, ZINGUSERREVIEWS.userid, rating, to_char(ZINGRATINGS.time, 'MMDDYYYY')
                from ZINGRATINGS, ZINGUSERREVIEWS
                where ZINGUSERREVIEWS.showid = %s 
                and ZINGRATINGS.showid = %s
                and ZINGUSERREVIEWS.userid = ZINGRATINGS.userid""", (showdata[0]['id'],showdata[0]['id']))
      userreviews = c.fetchall()
      c.execute("""SELECT SUM(rating), COUNT(rating) from ZINGRATINGS
                where showID = %s""", (showdata[0]['id'],))
      results = c.fetchall()
      # c.execute("""SELECT to_char(playingdate, 'DayMonthDDYYYY'), timeOfShow, ticketlink from Fringedates2 
      #           where showid = %s""", (showdata[0]['id'],))
      # dates= c.fetchall()
      c.execute("""SELECT adjective,COUNT(userid) from ZINGGOODADJECTIVES 
                where showid = %s
                GROUP BY adjective""", (showdata[0]['id'],))
      goodadjectives= c.fetchall()
      c.execute("""SELECT adjective,COUNT(userid) from ZINGBADADJECTIVES
                where showid = %s
                GROUP BY adjective""", (showdata[0]['id'],))
      badadjectives= c.fetchall()
      c.execute("""SELECT * from ZINGOUTSIDESHOWTAGS, ZINGOUTSIDECONTENT where ZINGOUTSIDESHOWTAGS.showid = %s
                and ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id""", (showdata[0]['id'],))
      articleids = c.fetchall()
      
      numReviews = len(results)
      averageRating = 0
      yourRating = 0
      reviewtexts = []
      for review in userreviews:
        data = []
        reviewtext = review['reviewtext']
        rating = review['rating']
        
        c.execute("SELECT first, last from ZINGUSERS where id = %s", (review['userid'],))
        username = c.fetchall()
        
        reviewtext = "static/reviews/" + reviewtext
        f = open(reviewtext, 'r')
        text = f.read()
        f.close()
        data.append(text)
        rating = convert_to_percent(float(rating))
        data.append(rating)
        data.append(username)
        date = review['to_char']
        date = date[1:2] + "/" + date[2:4] + "/" + date[4:]
        data.append(date)
        reviewtexts.append(data)
      
      # showdates = []
      # for x in dates:
      #   date = {}
      #   date['timeofshow'] = x['timeofshow']
      #   date['ticketlink'] = x['ticketlink']
       
      #   strlength = len(x['to_char'])
      #   day = x['to_char'][:x['to_char'].find("y")+1]
      #   month = x['to_char'][x['to_char'].find("ber")-6:strlength-6]
      #   numday = x['to_char'][strlength-6: strlength-4]
      #   year = x['to_char'][ strlength-4:]
      #   if  numday.find("0") == 0:
      #     numday = numday[1:]
      

      #   playingdate = day + ", " + month + " " + numday +" " + year
      #   print playingdate
      #   date['playingdate'] = playingdate
      #   showdates.append(date)

      description = showdata[0]['descript']
      headerDescription = description[:description.find("<br><br>")]
      description = description[description.find("<br><br>"):]
      barry = description.find('<a href="/barry')
      description = description[:barry]
      producer = showdata[0]['producer']
      producer = Markup(producer)

      if results[0]['sum'] != None:
        averageRating = convert_to_percent(float(results[0]['sum'])/float(results[0]['count']))
      description = Markup(description)
      headerDescription = Markup(headerDescription)
      showdata[0]['name'] = Markup(showdata[0]['name'])
      twitter = showdata[0]['name'].split(' ')
      twitterurl = twitter[0]
      for twit in range(1, len(twitter)):
        twitterurl = "%20" + twitter[twit]

      template_vars = {"showdata": showdata[0],
                      "producer": producer,
                       "description": description,
                       "headerDescription": headerDescription,
                       "useron": 'none',
                       "cast": casting, "venue": venue,
                       "userreviews": reviewtexts,
                       "rating": averageRating,
                       "yourRating": yourRating,
                       "goodadjectives": goodadjectives,
                       "badadjectives": badadjectives,
                       "articles": articleids,
                       "twitterurl":twitterurl
                       }
      if 'username' in session:
          c.execute("""SELECT rating
                    from ZINGRATINGS, ZINGUSERS
                    where ZINGRATINGS.userid = ZINGRATINGS.id
                    and ZINGUSERS.id = %s
                    and ZINGRATINGS.showID = %s""",
                    (session['username'], showdata[0]['id']))
          yourRating = c.fetchall()
          if len(yourRating) == 1:
              yourRating = yourRating[0]['rating']
              yourRating = convert_to_percent(yourRating)
          c.execute("SELECT first from ZINGUSERS where id = %s", (session['username'],))
          name = c.fetchall()[0]['first']
         
          template_vars['useron'] = name    
      return render_template("show.html", **template_vars)
    return render_template("error.html")

@app.route('/profile')
def profile():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    username = session['username']
    c.execute("SELECT id from ZingUsers where username = %s", (username,))
    userid = c.fetchall()[0]['id']
    c.execute("""SELECT ZINGUSERS.name, reviewText, rating,
              to_char(ZINGRATINGS.time, 'HHMIA.M.DayMonthDDYYY')
              from ZINGUSERREVIEWS, ZINGRATINGS, ZINGSHOWS
              where ZINGUSERREVIEWS.userid = ZINGRATINGS.userid
              and ZINGRATINGS.userid =%s
              and ZINGSHOWS.id = ZINGRATINGS.showid
              and ZINGSHOWS.id = ZINGUSERREVIEWS.showid""",
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



@app.route('/autocomplete/allshows', methods=['GET', 'POST'] )
def autocomplete():
  query = request.args.get('query')
  print query
  query = '%' + query + '%'
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT name, id from ZINGSHOWS
            where name LIKE %s""", (query,))
  results = c.fetchall()
  print results
  jsonresults = []
  for result in results:
     d = {'value': result['name'], 'data': result['id']}
     jsonresults.append(d)
    
  print jsonresults
  return jsonify(query = "Unit", suggestions = jsonresults)



@app.route('/submitrating', methods=['GET', 'POST'])
def submitrating():
    show = request.args.get('show')
    rating = request.args.get('stars')
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT id from ZINGSHOWS
              where name = %s""", (show,))
    showID = c.fetchall()
    showID = showID[0]
    showID = showID['id']
    userid = session['username']
    c.execute("""DELETE from ZINGRATINGS
              where userid = %s and showid = %s""",
              (userid, showID))
    c.execute("SET TIME ZONE 'America/New_York'")
    c.execute("""INSERT INTO ZINGRATINGS(userid, rating, showID, time)
              VALUES(%s, %s, %s, CURRENT_TIMESTAMP)""",
              (userid, rating, showID))
    conn.commit()
    c.execute("""SELECT rating from ZINGRATINGS
              where showID = %s""", (showID,))
    results = c.fetchall()
    totalstars = 0
    for stars in results:
        totalstars = totalstars + stars['rating']
    numReviews = len(results)
    averageRating = float(totalstars)/float(numReviews)
    averageRating = convert_to_percent(averageRating)
    c.execute("SELECT email FROM ZINGUSERS WHERE id = %s", (session['username']))
    email = c.fetchall()[0]['email']
    html = render_template(
            'email/review.html',
            )
    msg = Message("Review Submitted",
                  sender="noah@codearium.com",
                  recipients=[email])
    msg.html = html
    mail.send(msg)


    return averageRating

@app.route('/login', methods=['GET', 'POST'])
def login():
  email = request.args.get('email')
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT ID FROM ZINGUSERS WHERE EMAIL = %s", (email,))
  session['username'] = c.fetchall()[0]['id']
  return "session logged in Flask"


@app.route('/submitreview', methods=['GET', 'POST'])
def submitreview():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    show = request.args.get('show')
    review = request.args.get('text')
    rating = request.args.get('stars')
    goods = request.args.get('goods')
    bads = request.args.get('bads')
    goods  = json.loads(goods)
    bads = json.loads(bads)
    c.execute("""SELECT id from ZINGSHOWS
              where name = %s""", (show,))
    showID = c.fetchall()
    showID = showID[0]
    showID = showID['id']
    userid = session['username']
    c.execute("""DELETE from ZINGUSERREVIEWS
              where userid = %s and showid = %s""",
              (userid, showID))
    if "/" in show:
      slash = show.find("/")
      show = show[:slash]
    filepath = str(userid)+str(show)+'.txt'
    newReview = open('static/reviews/' + filepath, 'w')
    newReview.write(review)
    newReview.close()
    if rating != None:
      c.execute("SET TIME ZONE 'America/New_York'")
      c.execute("""INSERT INTO ZINGUSERREVIEWS(userid, showID, reviewText)
              VALUES(%s, %s, %s)""", (userid, showID, filepath))
      c.execute("""DELETE from ZINGRATINGS
              where userid = %s and showid = %s""",
              (userid, showID))
      c.execute("""INSERT INTO ZINGRATINGS(userid, rating, showID, time)
              VALUES(%s, %s, %s, CURRENT_TIMESTAMP)""",
              (userid, rating, showID))
    for good in goods:
      print good
      c.execute("""INSERT INTO ZINGGOODADJECTIVES(showid, adjective, userid)
                VALUES(%s,%s,%s)""",
                (showID, good, userid))
    for bad in bads:
      print bad
      c.execute("""INSERT INTO ZINGBADADJECTIVES(showid, adjective, userid)
                VALUES(%s,%s,%s)""",
                (showID, bad, userid))
    conn.commit()
    c.execute("SELECT email, first FROM ZINGUSERS WHERE id = %s", (session['username'],))
    results = c.fetchall()
    email = results[0]['email']
    first = results[0]['first']
    rating = convert_to_percent(float(rating))
    html = render_template(
            'email/review.html',
            bads = bads,
            goods = goods,
            rating = rating,
            review = review,
            show = show, 
            first = first
            )
    msg = Message("Review Submitted",
                  sender="noah@codearium.com",
                  recipients=[email])
    msg.html = html
    mail.send(msg)
    return ""


app.secret_key = """\xd6'\xdf@V\xfc\xc9\\\x05\xac
                 \x02P\xda\xa8r-\xee\xac*\xcdH\xc3\xef\x1d"""

if __name__ == "__main__":
    app.run(debug=True)
