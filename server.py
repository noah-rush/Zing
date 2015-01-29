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

### convenience function for converting date strings to postgres readable dates, not currently in use 

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

### convenience function for converting avgs in 1-5 to 0-100%
def convert_to_percent(stars):
    percent = stars/5
    percent = percent*100
    percent = str(percent)
    return percent


##function for sorting arrays by rating average
def sort_array(s):
    for i in range(1, len(s)):
        val = s[i]
        j = i - 1
        while (j >= 0) and (s[j]['avg'] < val['avg']):
            s[j+1] = s[j]
            j = j - 1
        s[j+1] = val
    return s


@app.route('/loaderio-83465c8b2028a6a6aa7cc879d3d87461/')
def loaderio():
  return render_template("loaderio-83465c8b2028a6a6aa7cc879d3d87461.txt")

### index, checks for user, and checks admin privileges
@app.route('/', methods=['GET', 'POST'])
def index():
    fromEmail = False
    if 'email' in session:
      fromEmail = True
      session.pop('email', None)
    if 'username' in session:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT first from ZINGUSERS where id = %s", (session['username'],))
        name = c.fetchall()[0]['first']
        c.execute("SELECT id from ZINGADMIN where userid = %s",(session['username'],));
        adminID = c.fetchall();
        if len(adminID)>0:
              return render_template('layout.html', fromEmail = fromEmail, useron=name, adminPrivileges=True)
        return render_template('layout.html', useron=name, fromEmail = fromEmail, adminPrivileges=False)
    return render_template('layout.html', useron = 'none',fromEmail = fromEmail, adminPrivileges=False)


@app.route('/home', methods=['GET', 'POST'])
def home():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT PhillyVenues.* FROM PhillyVenues, ZINGSHOWS WHERE ZINGSHOWS.venueid = PhillyVenues.id GROUP BY PhillyVenues.id ORDER BY PhillyVenues.id ASC")
  venues = c.fetchall()
  for venue in venues:
    venue['name'] = Markup(venue['name'])
  c.execute("SELECT ZINGShows.* FROM ZINGSHOWS ORDER BY id ASC")
  shows = c.fetchall()
  c.execute("SELECT showid, COUNT(rating), SUM(rating) FROM ZINGRATINGS GROUP BY showid")
  ratings = c.fetchall()
  c.execute("SELECT ZINGOUTSIDECONTENT.*, ZINGOUTSIDESHOWTAGS.* FROM ZINGOUTSIDECONTENT, ZINGOUTSIDESHOWTAGS where ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id")
  outsideContent = c.fetchall()
  for show in shows:
    show['name'] = Markup(show['name'])
    for rating in ratings:
      if rating['showid'] == show['id']:
        avg = float(rating['sum'])/float(rating['count'])
        show['rating'] = convert_to_percent(avg)
    show['reviews'] = []
    for oc in outsideContent:
      if oc['showid'] == show['id']:
        show['reviews'].append([oc['title'], oc['link']])
  c.execute("SELECT ZINGOUTSIDECONTENT.*, ZINGOUTSIDESHOWTAGS.showID FROM ZINGOUTSIDECONTENT, ZINGOUTSIDESHOWTAGS where ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id GROUP BY ZingoutsideContent.id, ZINGOUTSIDESHOWTAGS.showID ORDER BY ZINGOUTSIDECONTENT.id DESC")
  results = c.fetchall()
  bsr = []
  phindie = []
  pw = []
  citypaper = []
  shapiro = []
  inq = []
  for review in results:
    c.execute("SELECT name from ZINGSHOWS WHERE id = %s", (review['showid'],))
    showname = c.fetchall()[0]
    review['showname'] = showname['name']
    if review['publication'] == "http://bsr2.dev/index.php":
      bsr.append(review)
    if review['publication'] == 'http://citypaper.net':
      citypaper.append(review)
    if review['publication'] == 'http://www.philadelphiaweekly.com/arts-and-culture':
      pw.append(review)
    if review['publication'] == 'http://www.newsworks.org/':
      shapiro.append(review)
    if review['publication'] == 'http://phindie.com':
      phindie.append(review)     
    if review['publication'] == 'http://www.philly.com/r?19=960&32=3796&7=989523&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fblogs%2Fphillystage%2F':
      inq.append(review)
  print results
  c.execute("SELECT * from ZINGPOSTS ORDER BY id DESC")
  blog = c.fetchall()
  for post in blog:
    post['descript'] = Markup(post['descript'])
  c.execute("SELECT * from ZINGPOSTS ORDER BY id DESC LIMIT 1")
  article = c.fetchall()

  template_vars = {"outsideContent": outsideContent, 
                        "shows": shows,
                        "inq":inq, 
                        "venues": venues,
                        "phindie": phindie,
                        "shapiro": shapiro, 
                        "pw": pw, 
                        "citypaper": citypaper, 
                        "bsr": bsr, 
                        "reviews": results, 
                        "blog": blog, 
                        "firstparagraph": "",
                        "article": []
                       }
  if len(article) > 0:
    article = article[0]
    c.execute("""SELECT ZINGSHOWS.name, ZINGSHOWS.id, ZINGSHOWS.venueid FROM ZINGSHOWS, ZINGARTICLESHOWTAGS 
                 WHERE ZINGSHOWS.id = ZINGARTICLESHOWTAGS.showid
                 AND ZINGARTICLESHOWTAGS.articleid = %s""", (article['id'],))
    tags = c.fetchall()
    for tag in tags:
      c.execute("SELECT name from PhillyVenues where id = %s", (tag['venueid'],))
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
    template_vars['article'] = article
    template_vars['firstparagraph'] = firstparagraph
  return render_template("reviewlist.html", **template_vars )


# ##home, returns content from posts 
# @app.route('/home', methods=['GET', 'POST'])
# def home():
#   c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#   c.execute("SELECT * from ZINGPOSTS ORDER BY id DESC")
#   blog = c.fetchall()
  
#   for post in blog:
#     post['descript'] = Markup(post['descript'])
#     c.execute("""SELECT ZINGSHOWS.name, ZINGSHOWS.id FROM ZINGSHOWS, ZINGARTICLESHOWTAGS 
#                  WHERE ZINGSHOWS.id = ZINGARTICLESHOWTAGS.showid
#                  AND ZINGARTICLESHOWTAGS.articleid = %s""", (post['id'],))
#     tags = c.fetchall()
#     post['tags'] = tags
   
#   print blog
#   return render_template("newHomepage.html", blog = blog)

@app.route('/updateArticles', methods=['GET', 'POST'])
def update():
  import outsidecontentscraper
  outsidecontentscraper.update()
  return "Update Sucessful"


#### returns a post page, generated by post id/
@app.route('/post', methods=['GET', 'POST'])
def post():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  articleid = request.args.get('id')
  c.execute("SELECT * from ZINGPOSTS where id = %s", (articleid,))
  article = c.fetchall()
  article = article[0]
  c.execute("""SELECT ZINGSHOWS.name, ZINGSHOWS.id, ZINGSHOWS.venueid FROM ZINGSHOWS, ZINGARTICLESHOWTAGS 
                 WHERE ZINGSHOWS.id = ZINGARTICLESHOWTAGS.showid
                 AND ZINGARTICLESHOWTAGS.articleid = %s""", (article['id'],))
  tags = c.fetchall()
  for tag in tags:
    c.execute("SELECT name from PhillyVenues where id = %s", (tag['venueid'],))
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
  c.execute("SELECT * from ZINGPOSTS ORDER BY id DESC")
  blog = c.fetchall()
  return render_template("post.html", article = article, firstparagraph = firstparagraph, blog = blog)


###route for uploading photos in editor
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

#### functions for photo uploading
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
    return "F"
  if realkey == None:
    return "Please Login with Facebook"
  else:
    if security.check_password_hash(realkey, password):
      session['username'] = userid
      return "USER LOGIN" + data[0]['first']
  return "Incorrect Password"

###ajax route for creating an original content post
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


####create a zing user from a facebook login 
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


###email confirmation for new users 
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("UPDATE ZINGUSERS SET emailconfirm = True WHERE email = %s", (email,))
    conn.commit()
    c.execute("SELECT id, first FROM ZINGUSERS WHERE email = %s", (email,))
    results = c.fetchall()[0]
    userid = results['id']
    name = results['first']
    session['username'] = userid
    session['email'] = True
    return redirect(url_for('index'))


### CREATES A NEW USER OF TYPE ZINg (NOT FACEBOOK)// ZING USERS MUST CONFIRM BY EMAIL
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
    print "here"
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


###obsoletecode for now playing box on right of screen // show navigation has moved to the left of screen 
##// inited by the coming soon func// right side of screen is now zingdescript

# @app.route('/nowPlaying')
# def nowPlaying():
#     c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     # c.execute("""SELECT Karlshows2.name, SUM(rating), COUNT(rating)
#     #              from Karlshows2, ShowRatings4
#     #              WHERE (CURRENT_DATE, CURRENT_DATE)
#     #              OVERLAPS (start_date, end_date)
#     #              and ShowRatings4.showid = Karlshows2.id
#     #              GROUP BY Karlshows2.name""")
#     c.execute("""SELECT ZINGSHOWS.id,ZINGSHOWS.name, SUM(rating), COUNT(rating)
#                  from ZINGSHOWS, ZINGRATINGS
#                  WHERE ZINGRATINGS.showid = ZINGSHOWS.id
#                  GROUP BY ZINGSHOWS.name, ZINGSHOWS.id""")
#     showresults = c.fetchall()
#     c.execute("SELECT COUNT(*), showid from ZINGRATINGS where CURRENT_TIMESTAMP-time < INTERVAL '24 hours' GROUP BY showid")
#     recentresults = c.fetchall()
   
    
#     results = []
#     for x in range(len(showresults)):
#         result = []
#         recentAction = False
#         for y in recentresults:
#           if showresults[x]['id'] == y['showid']:
#             result.append(y['count'])
#             recentAction = True
#         if not(recentAction):
#           result.append(0)
          
        
#         result.append(showresults[x]['name'])
        
#         averageRating = float(showresults[x]['sum'])/float(showresults[x]['count'])
#         print convert_to_percent(averageRating)
#         result.append(convert_to_percent(averageRating))
        
#         results.append(result)
        
#     print results


#     return render_template('nowPlaying.html', results=results)



##function for returning editor's picks// not sure how this will work // right now returns all shows 
##that have been tagged in our original content
@app.route('/picks')
def picks():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT ZINGSHOWS.name,Zingshows.id from ZINGSHOWS, ZINGARTICLESHOWTAGS
                WHERE ZINGSHOWS.id = ZINGARTICLESHOWTAGS.showid
                GROUP BY ZINGSHOWS.name, ZINGSHOWS.id """)
  results = c.fetchall()
  sortedResults = []
  print results
  for result in results:
      result['name'] = Markup(result['name'])
      showid = result['id']
      c.execute("SELECT SUM(rating), COUNT(rating), showid FROM ZINGRATINGS WHERE showid = %s GROUP BY showid", (showid,))
      ratings = c.fetchall()
      rating = ''
      if len(ratings) > 0:
        rating = float(ratings[0]['sum'])/float(ratings[0]['count'])
        rating = convert_to_percent(rating)
      result["rating"] = rating
  return render_template('picks.html', results = results)


##returns shows with most user reviews
@app.route('/trending')
def trending():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT ZINGSHOWS.name,Zingshows.id, SUM(rating), COUNT(rating) from ZINGRATINGS, ZINGSHOWS
                WHERE ZINGSHOWS.id = ZINGRATINGS.showid GROUP BY ZINGSHOWS.name, ZINGSHOWS.id ORDER BY COUNT DESC""")
  results = c.fetchall()
  sortedResults = []
  for result in results:
    result['name'] = Markup(result['name'])
    count = int(result['count'])
    avg = float(result['sum'])/float(result['count'])
    temp = {"avg": convert_to_percent(avg), "name": result['name'], 'count': count, 'id': result['id']}
    sortedResults.append(temp)
  return render_template('trending.html', results = sortedResults)


##returns the top rated shows
@app.route('/toprated')
def toprated():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT ZINGSHOWS.name,ZINGSHOWS.id, SUM(rating), COUNT(rating) from ZINGRatings, ZINGSHOWS WHERE ZINGSHOWS.id = ZINGRATINGS.showid GROUP BY ZINGSHOWS.id,ZINGSHOWS.name")
  results = c.fetchall()
  sortedResults = []
  for result in results:
    result['name'] = Markup(result['name'])
    avg = float(result['sum'])/float(result['count'])
    temp = {"avg": avg, "name": result['name'], "id": result['id']}
    sortedResults.append(temp)
  sortedResults = sort_array(sortedResults)
  for tops in sortedResults:
    tops['avg'] = convert_to_percent(tops['avg'])
  return render_template('toprated.html', results = sortedResults)


###returns currently playing shows// init states // coming soon is a misnomer
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
      result['name'] = Markup(result['name'])
      c.execute("SELECT SUM(rating), COUNT(rating), showid FROM ZINGRATINGS WHERE showid = %s GROUP BY showid", (showid,))
      ratings = c.fetchall()
      rating = ''
      if len(ratings) > 0:
        rating = float(ratings[0]['sum'])/float(ratings[0]['count'])
        rating = convert_to_percent(rating)
      result["rating"] = rating
    return render_template('comingsoon.html', results=results)

    ### OLD CODE FOR FRINGE 2014 WHERE SHOWS HAD SPECIFIC DATES IN A DATE DATABASE

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
    # return render_template('comingsoon.html', results=results, dates = dates, alldates = alldates)
 


 ###returns a fullschedule of shows--duh
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


### api call to yelp from ajax call, gets business data
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
  results = []
  for business in businesses:
    result = []
    result.append(business['name'])
    location =  business['location']
    if 'coordinate' in location.keys():
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
    result.append(business['rating'])
    result.append(business['rating_img_url'])
    result.append(business['url'])
    results.append(result)
  results= json.dumps(results)
  return results

## to venue page - TAKES AN ID
@app.route('/venue', methods=['GET', 'POST'])
def venue():
    venue = request.args.get('venue')
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * from PhillyVenues where id = %s", (venue,))
    results = c.fetchall()
    results = results[0]
    results['name'] = Markup(results['name'])
    c.execute("SELECT * from Karlstaff where theatre = %s", (results['name'],))
    employees = c.fetchall()
    c.execute("""SELECT name, id from ZINGSHOWS
                 where venueid = %s """, (venue,))
    shows = c.fetchall()
    articles = []
    for show in shows:
      show['name'] = Markup(show['name'])
      c.execute("""SELECT ZINGOUTSIDECONTENT.* FROM ZINGOUTSIDECONTENT, ZINGOUTSIDESHOWTAGS
                    WHERE ZINGOUTSIDECONTENT.id = ZINGOUTSIDESHOWTAGS.articleid
                    AND ZINGOUTSIDESHOWTAGS.showid = %s""", (show['id'],))
      for a in c.fetchall():
        articles.append(a)
    return render_template('venue.html', venuedata=results,
                           staff=employees, useron='none',
                           showdata=shows, articles = articles)

# To A SHOW -- TAKES AN ID, right now connects to twitter but am doing nothing with it 
@app.route('/show', methods=['GET', 'POST'])
def show():
    t = Twitter(
    auth=OAuth('2290030034-qZlpLizAAp8FqA21jumX3sWKmKc2VVAHAPw9nUZ', 'I7B4ALWQQLTNYQKzu37tKahle36JL9NsWT3RkCYCKWx2i', '8ddlpAyOG5fq2qCHoJcxQ', 'tbjoqSMYMOxKyJgeqpZ1EexqCxoOsm4OYwiizshtZY4'))
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    show = request.args.get('show')
    c.execute("SELECT * from ZINGSHOWS where id = %s", (show,))
    showdata = c.fetchall()
    tweets = t.search.tweets(q="#"+showdata[0]['name'])
    # print tweets['search_metadata']
    # for tweet in tweets['statuses']:
    #   print "/n"
    #   print tweet['text']
    #   print tweet['source']
    if len(showdata)>0:
      # c.execute("""SELECT Karlactors.actorName, Karlcasting.role
      #           from Karlactors, Karlcasting
      #           where showID = %s and Karlactors.id = Karlcasting.actorID""",
      #           (showdata[0]['id'],))
      casting = c.fetchall()
      c.execute("""SELECT name from PhillyVenues
                where id = %s""", (showdata[0]['venueid'],))
      venue = c.fetchall()
      venue[0]['name'] = Markup(venue[0]['name'])
      c.execute("""SELECT reviewText, ZINGUSERREVIEWS.userid, 
                rating, to_char(ZINGRATINGS.time, 'MMDDYYYY')
                from ZINGRATINGS, ZINGUSERREVIEWS
                where ZINGUSERREVIEWS.showid = %s 
                and ZINGRATINGS.showid = %s
                and ZINGUSERREVIEWS.userid = ZINGRATINGS.userid""", (showdata[0]['id'],showdata[0]['id']))
      userreviews = c.fetchall()
      c.execute("""SELECT SUM(rating), COUNT(rating) 
                from ZINGRATINGS
                where showID = %s""", (showdata[0]['id'],))
      results = c.fetchall()
      # c.execute("""SELECT to_char(playingdate, 'DayMonthDDYYYY'), timeOfShow, ticketlink from Fringedates2 
      #           where showid = %s""", (showdata[0]['id'],))
      # dates= c.fetchall()
      c.execute("""SELECT adjective,COUNT(userid) 
                from ZINGGOODADJECTIVES 
                where showid = %s
                GROUP BY adjective""", (showdata[0]['id'],))
      goodadjectives= c.fetchall()
      c.execute("""SELECT adjective,COUNT(userid) 
                from ZINGBADADJECTIVES
                where showid = %s
                GROUP BY adjective""", (showdata[0]['id'],))
      badadjectives= c.fetchall()
      c.execute("""SELECT * 
                from ZINGOUTSIDESHOWTAGS, ZINGOUTSIDECONTENT 
                where ZINGOUTSIDESHOWTAGS.showid = %s
                and ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id""", 
                (showdata[0]['id'],))
      articleids = c.fetchall()
      
      numReviews = len(results)
      averageRating = 0
      yourRating = 0
      reviewtexts = []
      for review in userreviews:
        data = []
        reviewtext = review['reviewtext']
        rating = review['rating']
        c.execute("""SELECT first, last 
                    from ZINGUSERS where id = %s""", 
                    (review['userid'],))
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

###ajax route for search box autocomplete
@app.route('/autocomplete/allshows', methods=['GET', 'POST'] )
def autocomplete():
  query = request.args.get('query')
  query = '%' + query + '%'
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT name, id from ZINGSHOWS
            where name LIKE %s""", (query,))
  results = c.fetchall()
  jsonresults = []
  for result in results:
     d = {'value': result['name'], 'data': result['id']}
     jsonresults.append(d)
  return jsonify(query = "Unit", suggestions = jsonresults)


#### handling ratings and reviews, email conf just says number of reviews with no grammar
@app.route('/submitreview', methods=['GET', 'POST'])
def submitreview():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    showID = request.args.get('show')
    review = request.args.get('text')
    rating = request.args.get('stars')
    goods = request.args.get('goods')
    bads = request.args.get('bads')
    goods  = json.loads(goods)
    bads = json.loads(bads)
  
    userid = session['username']
    c.execute("""DELETE from ZINGUSERREVIEWS
              where userid = %s and showid = %s""",
              (userid, showID))
    filepath = str(userid)+str(showID)+'.txt'
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
    c.execute("""SELECT COUNT(*) 
                  FROM ZINGRATINGS 
                  WHERE userid = %s""",
                  (userid,))
    numUserRatings = c.fetchall()[0]['count']
    suffixNum = str(numUserRatings % 10)
    numUserRatings = str(numUserRatings)
    if suffixNum == "0":
      numUserRatings = numUserRatings +"th"
    elif suffixNum == "1": 
        numUserRatings = numUserRatings + "st"
        if numUserRatings == "11st":
          numUserRatings = numUserRatings[:2] +"th"
    elif suffixNum == "2":  
        numUserRatings = numUserRatings + "nd"
        if numUserRatings == "12nd":
          numUserRatings = numUserRatings[:2] +"th"
    elif suffixNum == "3":
        numUserRatings = numUserRatings + "rd"
        if numUserRatings == "13rd":
          numUserRatings = numUserRatings[:2] +"th"
    elif suffixNum == "4": 
        numUserRatings = numUserRatings + "th"
    elif suffixNum == "5":
        numUserRatings = numUserRatings + "th"
    elif suffixNum == "6":
        numUserRatings = numUserRatings + "th"
    elif suffixNum == "7": 
        numUserRatings = numUserRatings + "th"
    elif suffixNum == "8":
        numUserRatings = numUserRatings + "th"
    elif suffixNum == "9": 
        numUserRatings = numUserRatings + "th"


      
  
    print numUserRatings
    c.execute("SELECT name from ZINGSHOWS WHERE id = %s", (showID,))
    show = c.fetchall()[0]['name']
    html = render_template(
            'email/review.html',
            bads = bads,
            goods = goods,
            rating = rating,
            review = review,
            show = show, 
            first = first, 
            userReviewNumber = numUserRatings
            )
    msg = Message("Review Submitted",
                  sender="noah@codearium.com",
                  recipients=[email])
    msg.html = html
    mail.send(msg)
    return ""

####facebook to flask login 
@app.route('/login', methods=['GET', 'POST'])
def login():
  email = request.args.get('email')
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT ID, emailconfirm FROM ZINGUSERS WHERE EMAIL = %s", (email,))
  results = c.fetchall()
  print results
  print results[0]['emailconfirm']
  if results[0]['emailconfirm']:
    session['username'] = results[0]['id']
    return "session logged in Flask"
  else:
    return "<h3> A confirmation email has been sent. Please check your email and click the link to verify your account. </h3>"

@app.route('/insession', methods=['GET', 'POST'])
def insession():
  if 'username' in session:
    return 'true'
  else:
    return 'false'

@app.route('/removeReview', methods = ['GET', 'POST'])
def removeReview():
   c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
   showid = request.args.get('showid')
   userid = request.args.get('userid')
   c.execute("""DELETE FROM ZINGUSERREVIEWS WHERE 
              userid = %s AND showid = %s""", (userid, showid))
   c.execute("""DELETE FROM ZINGRatings WHERE 
              userid = %s AND showid = %s""", (userid, showid))
   c.execute("""DELETE FROM ZINGGOODADJECTIVES WHERE 
              userid = %s AND showid = %s""", (userid, showid))
   c.execute("""DELETE FROM ZINGBADADJECTIVES WHERE 
              userid = %s AND showid = %s""", (userid, showid))
   conn.commit()
   return "did it"

@app.route('/removeOutReview', methods = ['GET', 'POST'])
def removeOutReview():
   c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
   articleid = request.args.get('articleid')
   c.execute("""DELETE FROM ZINGOUTSIDECONTENT WHERE 
              id = %s""", (articleid,))
   c.execute("""DELETE FROM ZINGOUTSIDESHOWTAGS WHERE 
              articleid = %s""", (articleid,))
   conn.commit()
   return "did it"


@app.route('/removeTag', methods = ['GET', 'POST'])
def removeTag():
   c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
   articleid = request.args.get('articleid')
   showid = request.args.get('showid')
   c.execute("""DELETE FROM ZINGOUTSIDESHOWTAGS WHERE 
              articleid = %s and showid = %s""", (articleid,showid))
   conn.commit()
   return "did it"

@app.route('/manageOutReviews', methods=['GET', 'POST'])
def manageOutReviews():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT ZINGOUTSIDECONTENT.*, ZINGOUTSIDESHOWTAGS.showID FROM ZINGOUTSIDECONTENT, ZINGOUTSIDESHOWTAGS where ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id GROUP BY ZingoutsideContent.id, ZINGOUTSIDESHOWTAGS.showID ORDER BY ZINGOUTSIDECONTENT.id DESC")
  results = c.fetchall()
  for review in results:
    c.execute("SELECT name from ZINGSHOWS WHERE id = %s", (review['showid'],))
    showname = c.fetchall()[0]
    review['showname'] = showname['name']
    c.execute("SELECT * from SNIPPETS WHERE articleid = %s", (review['id'],))
    snippets = c.fetchall()
    for snippet in snippets:
      print snippet['snippet']
    review['snippets'] = snippets
  return render_template("manageOutsideReviews.html", results = results)


@app.route('/manageReviews', methods=['GET', 'POST'])
def manageReviews():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT ZINGUSERREVIEWS.id, ZINGRATINGS.id, Zingratings.showid, reviewText, ZINGUSERREVIEWS.userid, 
                rating, to_char(ZINGRATINGS.time, 'MMDDYYYY')
                from ZINGRATINGS, ZINGUSERREVIEWS
                where ZINGUSERREVIEWS.showid = ZINGRATINGS.showid 
                and ZINGUSERREVIEWS.userid = ZINGRATINGS.userid""")
  reviewtexts = []
  results = c.fetchall()
  for review in results:
        data = []
        reviewtext = review['reviewtext']
        rating = review['rating']
        c.execute("""SELECT first, last, id 
                    from ZINGUSERS where id = %s""", 
                    (review['userid'],))
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
        
        data.append(review['id'])
        data.append(review['showid'])
        reviewtexts.append(data)
  print results
  return render_template("manageReviews.html", userreviews = reviewtexts)



###return a description of Zing
@app.route('/zingDescript')
def zingDescript():
  return render_template('zingdescription.html')

###logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

###returns editor window from ajax call
@app.route('/edit', methods=['GET', 'POST'])
def edit():
  return render_template("editor.html")

###returns about window from ajax call
@app.route('/about', methods=['GET', 'POST'])
def about():
  return render_template("about.html")


app.secret_key = """\xd6'\xdf@V\xfc\xc9\\\x05\xac
                 \x02P\xda\xa8r-\xee\xac*\xcdH\xc3\xef\x1d"""

if __name__ == "__main__":
    app.run(debug=True)
