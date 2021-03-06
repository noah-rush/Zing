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



def fullScheduleTemplate(results, title):
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    months = {"01": "January",
              "02": "February",
              "03": "March",
              "04": "April",
              "05": "May ",
              "06": "June ",
              "07": "July ", 
              "08": "August ",
              "09": "September ", 
              "10": "October ", 
              "11": "November ", 
              "12": "December "}
    for result in results:
      result['descript'] = Markup(result['descript'])
      c.execute("""SELECT SUM(rating), COUNT(rating)  FROM ZINGRATINGS
                    WHERE showid = %s""", (result['id'],))
      for a in c.fetchall():
        if a['sum'] != None:
          result['rating'] = convert_to_percent(float(a['sum'])/float(a['count']))
      c.execute("SELECT name FROM Theatres WHERE id = %s", (result['venueid'],))
      venueResult = c.fetchall()
      if len(venueResult)>0:
        venuename = venueResult[0]['name']
      else:
        venuename = ""
      result['venuename'] = Markup(venuename)
      result['name'] = Markup(result['name'])
      result['start'] = str(result['start'])
      result['enddate'] = str(result['enddate'])
      # monthfirst = result['start'].find("-")
      # monthlast = result['start'].rfind("-")
      # month = result['start'][monthfirst+1:monthlast]
      # day = result['start'][monthlast+1:]
      # year = result['start'][:4]
      # if day[0] == "0":
      #   day = day[1:]
      # result['start'] = months[month] + day 
      # monthfirst = result['enddate'].find("-")
      # monthlast = result['enddate'].rfind("-")
      # month = result['enddate'][monthfirst+1:monthlast]
      # day = result['enddate'][monthlast+1:]
      # if day[0] == "0":
      #   day = day[1:]
      # year = result['enddate'][:4]
      # result['enddate'] = months[month] + day + ", " +  year
    results = resort(results)
    totalCountMod = len(results)%3
    return render_template('fullschedule.html', title = title, results=results,totalCountMod = totalCountMod, count1 = int(len(results)/3), count2 = int(len(results)*2/3))


### convenience function for converting date strings to postgres readable dates, not currently in use 
def resort(infoList):
  newList = []
  newList1 = []
  newList2 = []
  newList3 = []
  for i in enumerate(infoList):
    if i[0]%3 == 0:
      newList1.append(i[1])
    if i[0]%3 == 1:
      newList2.append(i[1])
    if i[0]%3 == 2:
      newList3.append(i[1])
  newList = newList1 + newList2 + newList3
  return newList




def convertDate(date):
        strlength = len(date)
        day = date[:date.find("y")+1]
        month = date[date.find("ber")-6:strlength-6]
        numday = date[strlength-6: strlength-4]
        year = date[ strlength-4:]
        if  numday.find("0") == 0:
          numday = numday[1:]
        playingdate = day + ", " + month + " " + numday +" " + year
        return playingdate

### convenience function for converting avgs in 1-5 to 0-100%
def convert_to_percent(stars):
    percent = stars/5
    percent = percent*100
    percent = percent
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
    temp = {"avg": int(convert_to_percent(avg)), "name": result['name'], 'count': count, 'id': result['id']}
    sortedResults.append(temp)
  return sortedResults

def toprated():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT ZINGSHOWS.name,ZINGSHOWS.id, SUM(rating), COUNT(rating) 
    from ZINGRatings, ZINGSHOWS WHERE ZINGSHOWS.id = ZINGRATINGS.showid
    GROUP BY ZINGSHOWS.id,ZINGSHOWS.name""")
  results = c.fetchall()
  sortedResults = []
  for result in results:
    result['name'] = Markup(result['name'])
    avg = float(result['sum'])/float(result['count'])
    temp = {"avg": avg, "name": result['name'], "id": result['id']}
    sortedResults.append(temp)
  sortedResults = sort_array(sortedResults)
  for tops in sortedResults:
    tops['avg'] = int(convert_to_percent(tops['avg']))
  return sortedResults

def comingsoon():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT name, id, venueid
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
        rating = int(convert_to_percent(rating))
      result["rating"] = rating
      c.execute("SELECT address, name FROM THEATRES WHERE id = %s",(result['venueid'], ))
      venuedata = c.fetchall()[0]
      result['name'] = Markup(result['name'])
      result["address"] = venuedata['address'] 
      result["venue"] = Markup(venuedata['name']) 
    return results

def allposts():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT * from BLOGPOSTS ORDER BY id DESC")
  blog = c.fetchall()
  for post in blog:
    post['descript'] = Markup(post['descript'])
    post['content'] = Markup(post['content'])
  return blog

def venueMenu():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT Theatres.* FROM Theatres, ZINGSHOWS WHERE ZINGSHOWS.venueid = Theatres.id GROUP BY Theatres.id ORDER BY THEATRES.id ASC LIMIT 10")
  venues = c.fetchall()
  for venue in venues:
    venue['name'] = Markup(venue['name'])
  return venues

def reviewMenu():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT ZINGOUTSIDECONTENT.*, ZINGOUTSIDESHOWTAGS.showID 
               FROM ZINGOUTSIDECONTENT, ZINGOUTSIDESHOWTAGS 
               where ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id 
               GROUP BY ZingoutsideContent.id, ZINGOUTSIDESHOWTAGS.showID 
               ORDER BY ZINGOUTSIDECONTENT.id DESC
               LIMIT 10""")
  results = c.fetchall()
  return results

@app.route('/forgot', methods=['GET','POST'])
def forgot():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  email = request.args.get('email')
  c.execute("SELECT * FROM USERS WHERE email = %s", (email,))
  user = c.fetchall()
  if len(user) > 0: 
    token = ts.dumps(email, salt='pass-reset-key')
    confirm_url = url_for(
            'reset_pass',
            token=token,
            _external=True)
    html = render_template(
            'email/resetpass.html',
            confirm_url=confirm_url)
    msg = Message("Reset your password",
                  sender="info@phillyzing.com",
                  recipients=[email])
    msg.html = html
    mail.send(msg)

  return ""

@app.route('/loaderio-83465c8b2028a6a6aa7cc879d3d87461/')
def loaderio():
  return render_template("loaderio-83465c8b2028a6a6aa7cc879d3d87461.txt")

### index, checks for user, and checks admin privileges
@app.route('/', methods=['GET', 'POST'])
def index():
    fromEmail = False
    trendingResults = trending()
    topResults = toprated()
    thisweek = comingsoon()
    blog = allposts()
    venues = venueMenu()
    reviews = reviewMenu()
    template_vars = {"toprated": topResults, 
                        "trending": trendingResults,
                        "thisweek":thisweek, 
                        "blog": blog,
                        "adminPrivileges": False,
                        "fromEmail": False,
                        "password": False,
                        "theatres": venues,
                        "reviews":reviews,
                        "useron": 'none',
                        "useron2": 'none'
                       }
    if 'email' in session:
      template_vars['fromEmail'] = True
      session.pop('email', None)
    if 'password' in session: 
      template_vars['password'] = True
      session.pop('password', None)
    if 'username' in session:
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT first from USERS where id = %s", (session['username'],))
        name = c.fetchall()[0]['first']
        c.execute("SELECT id from ZINGADMIN where userid = %s",(session['username'],));
        adminID = c.fetchall();
        c.execute("SELECT first, last, emailconfirm from USERS where id = %s", (session['username'],))
        userinfo = c.fetchall()[0]
        name = userinfo['first'] + " " +userinfo['last']
        template_vars['useron2'] = name
        emailconfirm = userinfo['emailconfirm']
        if emailconfirm:
          template_vars['useron'] = name
        else:
          template_vars['useron'] = "confirm email"
        if len(adminID)>0:
          template_vars['adminPrivileges'] = True
          return render_template('index-alt.html',**template_vars)
        return render_template('index-alt.html',**template_vars)
   
    return render_template('index-alt.html',**template_vars)



# @app.route('/home', methods=['GET', 'POST'])
# def home():
#   c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#   c.execute("SELECT Theatres.* FROM Theatres, ZINGSHOWS WHERE ZINGSHOWS.venueid = Theatres.id GROUP BY Theatres.id ORDER BY Theatres.id ASC")
#   venues = c.fetchall()
#   for venue in venues:
#     venue['name'] = Markup(venue['name'])
#   c.execute("SELECT ZINGShows.* FROM ZINGSHOWS ORDER BY id ASC")
#   shows = c.fetchall()
#   c.execute("SELECT showid, COUNT(rating), SUM(rating) FROM ZINGRATINGS GROUP BY showid")
#   ratings = c.fetchall()
#   c.execute("SELECT ZINGOUTSIDECONTENT.*, ZINGOUTSIDESHOWTAGS.* FROM ZINGOUTSIDECONTENT, ZINGOUTSIDESHOWTAGS where ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id")
#   outsideContent = c.fetchall()
#   for show in shows:
#     show['name'] = Markup(show['name'])
#     for rating in ratings:
#       if rating['showid'] == show['id']:
#         avg = float(rating['sum'])/float(rating['count'])
#         show['rating'] = convert_to_percent(avg)
#     show['reviews'] = []
#     for oc in outsideContent:
#       if oc['showid'] == show['id']:
#         show['reviews'].append([oc['title'], oc['link']])
#   c.execute("SELECT ZINGOUTSIDECONTENT.*, ZINGOUTSIDESHOWTAGS.showID FROM ZINGOUTSIDECONTENT, ZINGOUTSIDESHOWTAGS where ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id GROUP BY ZingoutsideContent.id, ZINGOUTSIDESHOWTAGS.showID ORDER BY ZINGOUTSIDECONTENT.id DESC")
#   results = c.fetchall()
#   bsr = []
#   phindie = []
#   pw = []
#   citypaper = []
#   shapiro = []
#   inq = []
#   for review in results:
#     c.execute("SELECT name from ZINGSHOWS WHERE id = %s", (review['showid'],))
#     showname = c.fetchall()[0]
#     review['showname'] = showname['name']
#     if review['publication'] == "http://bsr2.dev/index.php":
#       bsr.append(review)
#     if review['publication'] == 'http://citypaper.net':
#       citypaper.append(review)
#     if review['publication'] == 'http://www.philadelphiaweekly.com/arts-and-culture':
#       pw.append(review)
#     if review['publication'] == 'http://www.newsworks.org/':
#       shapiro.append(review)
#     if review['publication'] == 'http://phindie.com':
#       phindie.append(review)     
#     if review['publication'] == 'http://www.philly.com/r?19=960&32=3796&7=989523&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fblogs%2Fphillystage%2F':
#       inq.append(review)
#   c.execute("SELECT * from ALLPOSTS ORDER BY id DESC")
#   blog = c.fetchall()
#   for post in blog:
#     post['descript'] = Markup(post['descript'])
#   c.execute("SELECT * from ALLPOSTS ORDER BY id DESC LIMIT 1")
#   article = c.fetchall()

#   template_vars = {"outsideContent": outsideContent, 
#                         "shows": shows,
#                         "inq":inq, 
#                         "venues": venues,
#                         "phindie": phindie,
#                         "shapiro": shapiro, 
#                         "pw": pw, 
#                         "citypaper": citypaper, 
#                         "bsr": bsr, 
#                         "reviews": results, 
#                         "blog": blog, 
#                         "firstparagraph": "",
#                         "article": []
#                        }
#   if len(article) > 0:
#     article = article[0]
#     c.execute("""SELECT ZINGSHOWS.name, ZINGSHOWS.id, ZINGSHOWS.venueid FROM ZINGSHOWS, ZINGARTICLESHOWTAGS 
#                  WHERE ZINGSHOWS.id = ZINGARTICLESHOWTAGS.showid
#                  AND ZINGARTICLESHOWTAGS.articleid = %s""", (article['id'],))
#     tags = c.fetchall()
#     for tag in tags:
#       c.execute("SELECT name from Theatres where id = %s", (tag['venueid'],))
#       venue = c.fetchall()[0]['name']
#       tag['venue'] = venue
#     article['tags'] = tags
#     filename = article['article']
#     text = open('static/Posts/'+filename, 'r')
#     a = text.read()
#     article['article'] = Markup(a)
#     firstparagraph = article['article'][:article['article'].find("</p>")+4]
#     firstparagraph = Markup(firstparagraph)
#     article['article'] = article['article'][article['article'].find("</p>")+4:]
#     article['article'] = Markup(article['article'])
#     text.close()
#     template_vars['article'] = article
#     template_vars['firstparagraph'] = firstparagraph
#   return render_template("reviewlist.html", **template_vars )


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
@app.route('/blog', methods=['GET', 'POST'])
def blog():
  blog = allposts()
  return render_template('blog-all.html',blog = blog)



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
  previd = int(articleid) - 1 
  nextid = int(articleid) + 1 
  c.execute("SELECT * from BLOGPOSTS where id = %s", (articleid,))
  article = c.fetchall()
  article = article[0]
  c.execute("SELECT * FROM BLOGPOSTS where id = %s",(previd,))
  prevarticle = c.fetchall()
  if len(prevarticle) > 0:
    prevarticle = prevarticle[0]
  else:
    prevarticle = "none"

  c.execute("SELECT * FROM BLOGPOSTS where id = %s",(nextid,))
  nextarticle = c.fetchall()

  if len(nextarticle) > 0:
    nextarticle = nextarticle[0]
  else:
    nextarticle = "none"
  

  # c.execute("""SELECT ZINGSHOWS.name, ZINGSHOWS.id, ZINGSHOWS.venueid FROM ZINGSHOWS, ZINGARTICLESHOWTAGS 
  #                WHERE ZINGSHOWS.id = ZINGARTICLESHOWTAGS.showid
  #                AND ZINGARTICLESHOWTAGS.articleid = %s""", (article['id'],))
  # tags = c.fetchall()
  # for tag in tags:
  #   c.execute("SELECT name from Theatres where id = %s", (tag['venueid'],))
  #   venue = c.fetchall()[0]['name']
  #   tag['venue'] = venue
  # article['tags'] = tags
  # filename = article['article']
  # text = open('static/Posts/'+filename, 'r')
  # a = text.read()
  # article['article'] = Markup(a)
  firstparagraph = article['content'][:article['content'].find("</p>")+4]
  firstparagraph = Markup(firstparagraph)
  article['content'] = article['content'][article['content'].find("</p>")+4:]
  article['content'] = Markup(article['content'])
  # text.close()
  c.execute("SELECT * from BLOGPOSTS ORDER BY id DESC")
  blog = c.fetchall()
  c.execute("""SELECT * FROM ZINGARTICLESHOWTAGS, ZINGSHOWS 
                WHERE articleid =%s and 
                 ZINGARTICLESHOWTAGS.showid = ZINGSHOWS.id""",
                  (articleid,))
  showtags = c.fetchall()
  return render_template("post.html", article = article, 
                          nextarticle = nextarticle,
                          prevarticle = prevarticle,
                          firstparagraph = firstparagraph, 
                          blog = blog,
                          showtags = showtags)


###route for uploading photos in editor
@app.route('/photo', methods=[ 'POST'])
def photo():
    try:
        files = request.files
        uploaded_files = _handleUpload(files)
        return jsonify({'files': uploaded_files})
    except:
        raise
        return jsonify({'status': 'error'})
UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


@app.route('/showPhoto', methods=[ 'POST'])
def showPhoto():
    try:
        files = request.files
        uploaded_files = _handleShowUpload(files)
        return jsonify({'files': uploaded_files})
    except:
        raise
        return jsonify({'status': 'error'})
UPLOAD_FOLDER = 'static/Zingimages/'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

#### functions for photo uploading
def allowed_file(filename):
  extension = filename[filename.find('.')+1:]
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
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filenames.append("%s" % (file.filename))
    return filenames

def _handleShowUpload(files):
    if not files:
       return None
    filenames = []
    saved_files_urls = []
    for key, file in files.iteritems():
        if file and allowed_file(file.filename):
            filename = file.filename
            filename = str(session['showid']) + '.jpg'
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filenames.append("%s" % (file.filename))
    return filenames


### zing sign in without facebook    
@app.route('/signin',  methods=[ 'POST'])
def signin():
  email = str(request.form['email']).lower()
  password = request.form['hidden']
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT first,id, passhash FROM USERS where email=%s", (email,))
  data = c.fetchall()
  if len(data) > 0:
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
  # filepath = str(title)+str(author)+'.txt'
  # newReview = open('static/Posts/' + filepath, 'w')
  # newReview.write(article)
  # newReview.close()
  c.execute("""INSERT INTO BLOGPOSTS(author, userid,title,content,photo, descript, date) 
            VALUES(%s,%s,%s,%s,%s, %s, CURRENT_DATE) RETURNING id""", (author, session['username'], title, article, photo, descript))
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
  c.execute("SELECT * from USERS where email = %s",(email,))
  testemail = c.fetchall()
  if testemail != []:
    userid = testemail[0]['id']
    session['username'] = testemail[0]['id']
    return "USER LOGIN" + testemail[0]['first']
  lastname = str(request.args.get('lastname'))
  c.execute("""INSERT INTO USERS(first, last, email)
                    VALUES (%s, %s, %s)""",
                  (firstname, lastname, email))
  conn.commit()
  c.execute("UPDATE USERS SET emailconfirm = True WHERE email = %s", (email,))
  # token = ts.dumps(email, salt='email-confirm-key')
  # confirm_url = url_for(
  #           'confirm_email',
  #           token=token,
  #           _external=True)
  # html = render_template(
  #           'email/activate.html',
  #           confirm_url=confirm_url)
  # msg = Message("Welcome to Zing",
  #                 sender="info@phillyzing.com",
  #                 recipients=[email])
  # msg.html = html
  # mail.send(msg)
  return "AEW USER CREATED" + firstname


###email confirmation for new users 
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("UPDATE USERS SET emailconfirm = True WHERE email = %s", (email,))
    conn.commit()
    c.execute("SELECT id, first FROM USERS WHERE email = %s", (email,))
    results = c.fetchall()[0]
    userid = results['id']
    name = results['first']
    session['username'] = userid
    session['email'] = True
    return redirect(url_for('index'))

@app.route('/reset/<token>')
def reset_pass(token):
    try:
        email = ts.loads(token, salt="pass-reset-key", max_age=86400)
    except:
        abort(404)
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT id, first FROM USERS WHERE email = %s", (email,))
    results = c.fetchall()[0]
    userid = results['id']
    name = results['first']
    session['username'] = userid
    session['password'] = True
    return render_template('resetpassword.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset_password():
    reset1 = str(request.form['reset1'])
    reset2 = str(request.form['reset2'])
    if reset1 ==reset2:
      c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      c.execute("SELECT * FROM USERS WHERE id =%s", (session['username'],))
      userData = c.fetchall()[0]
      fullname = userData['first'] + userData['last']
      you = User(fullname, reset1)
      passhash = you.pw_hash
      c.execute("""UPDATE USERS SET passhash = %s
                    WHERE id = %s""", (passhash, session['username']))
      conn.commit()
      session['password'] = True
    else:
      return "passwords do not match"
    return redirect(url_for('index'))




### CREATES A NEW USER OF TYPE ZINg (NOT FACEBOOK)// ZING USERS MUST CONFIRM BY EMAIL
@app.route('/zingnewuser', methods=['GET', 'POST'])
def zingnewuser():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  email = str(request.form['email']).lower()
  firstname = str(request.form['firstname'])
  lastname = str(request.form['lastname'])
  password = str(request.form['password'])
  c.execute("SELECT * from USERS where email = %s",(email,))
  testemail = c.fetchall()
  if testemail != []:
    userid = testemail[0]['id']
    return "EMAIL FOUND" + testemail[0]['first']
  fullname = firstname + lastname
  you = User(fullname, password)
  passhash = you.pw_hash
  c.execute("""INSERT INTO USERS(first, last, email, passhash)
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
                  sender="info@phillyzing.com",
                  recipients=[email])
  msg.html = html
  mail.send(msg)
  c.execute("SELECT id from USERS WHERE email = %s", (email,))
  userid = c.fetchall()[0]['id']
  session['username'] = userid
  conn.commit()
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




##returns the top rated shows
# @app.route('/toprated')
# def toprated():
#   c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#   c.execute("SELECT ZINGSHOWS.name,ZINGSHOWS.id, SUM(rating), COUNT(rating) from ZINGRatings, ZINGSHOWS WHERE ZINGSHOWS.id = ZINGRATINGS.showid GROUP BY ZINGSHOWS.id,ZINGSHOWS.name")
#   results = c.fetchall()
#   sortedResults = []
#   for result in results:
#     result['name'] = Markup(result['name'])
#     avg = float(result['sum'])/float(result['count'])
#     temp = {"avg": avg, "name": result['name'], "id": result['id']}
#     sortedResults.append(temp)
#   sortedResults = sort_array(sortedResults)
#   for tops in sortedResults:
#     tops['avg'] = convert_to_percent(tops['avg'])
#   return render_template('toprated.html', results = sortedResults)


###returns currently playing shows// init states // coming soon is a misnomer
# @app.route('/comingsoon')
# def comingsoon():
#     c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     c.execute("""SELECT name, id
#                  from ZINGSHOWS
#                  WHERE (start,enddate)
#                  OVERLAPS (CURRENT_DATE, CURRENT_DATE)
#                """)
#     results = c.fetchall()
#     for result in results:
#       showid = result['id']
#       result['name'] = Markup(result['name'])
#       c.execute("SELECT SUM(rating), COUNT(rating), showid FROM ZINGRATINGS WHERE showid = %s GROUP BY showid", (showid,))
#       ratings = c.fetchall()
#       rating = ''
#       if len(ratings) > 0:
#         rating = float(ratings[0]['sum'])/float(ratings[0]['count'])
#         rating = convert_to_percent(rating)
#       result["rating"] = rating
#     return render_template('comingsoon.html', results=results)

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
 
@app.route('/source')
def source():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    pub = request.args.get('pub')
    publication = ""
    img = ""
    if pub == "inq":
      publication = "http://www.philly.com/r?19=960&32=3796&7=989523&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fblogs%2Fphillystage%2F"
      title = "Inquirer Theater Blog"
      img = "inq.png"
    if pub == "how-shap":
      publication = "http://www.newsworks.org/"
      title = "Howard Shapiro's Theater Blog"
      img = "shapiro.jpg"
    if pub == "bsr":
      title = "Broad Street Review"
      publication = "http://bsr2.dev/index.php"
      img = "bsr.png"
    if pub == "city-paper":
      publication = "http://citypaper.net"
      title = "City Paper"
      img = "citypaper.png"
    if pub == "phin":
      publication = "http://phindie.com"
      title = "Phindie"
      img = "phindie.png"
    if pub == "phil-week":
      publication = "http://www.philadelphiaweekly.com/arts-and-culture"
      title = "Philadelphia Weekly"
      img = "pw.jpg"
    if pub == "philcom":
      publication = "http://www.philly.com/r?19=960&32=3796&7=195487&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fentertainment%2Farts"
      title = "Philly.com"
      img = "phillydotcom.png"
    c.execute("""SELECT ZINGOUTSIDECONTENT.*
                FROM ZingoutsideContent, ZINGOUTSIDESHOWTAGS
                WHERE ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id
                AND ZINGOUTSIDECONTENT.publication = %s
                GROUP BY ZINGOUTSIDECONTENT.id, ZINGOUTSIDESHOWTAGS.articleid
                ORDER BY ZINGOUTSIDECONTENT.id DESC""",
                (publication,))
    results = c.fetchall()
    for result in results:
      result['pub-go'] = pub
      result['pub-image'] = img
      result['author'] = Markup(result['author'])
      result['descript'] = Markup(result['descript'])
      c.execute("""SELECT ZINGOUTSIDESHOWTAGS.showid,
                  ZINGShows.*
                  FROM ZINGOUTSIDESHOWTAGS , ZINGSHOWS
                  WHERE articleid = %s
                  AND Zingshows.id = ZINGOUTSIDESHOWTAGS.showid""", (result['id'],))
      showtags = []
      showTagResults = c.fetchall()
      for tag in showTagResults:
        if [tag['name'], tag['id']] in showtags:
          pass
        else:
          showtags.append([tag['name'], tag['id']])
      for tag in showtags:
        tag[0] = Markup(tag[0])
      result['showtags'] = showtags
    results = resort(results)
    return render_template('fullreviews.html', results=results, title = title, image =img, count1 = int(len(results)/3), count2 = int(len(results)*2/3))



@app.route('/fullreviews')
def fullreviews():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT ZINGOUTSIDECONTENT.*
                FROM ZingoutsideContent, ZINGOUTSIDESHOWTAGS
                WHERE ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id
                GROUP BY ZINGOUTSIDECONTENT.id, ZINGOUTSIDESHOWTAGS.articleid
                ORDER BY ZINGOUTSIDECONTENT.id DESC""")
    results = c.fetchall()
    for result in results:
      result['descript'] = Markup(result['descript'])
      result['author'] = Markup(result['author'])
      # soup = BeautifulSoup(Markup(result['descript']))
      # result['descript'] = soup.get_text()
      c.execute("""SELECT ZINGOUTSIDESHOWTAGS.showid,
                  ZINGShows.*
                  FROM ZINGOUTSIDESHOWTAGS , ZINGSHOWS
                  WHERE articleid = %s
                  AND Zingshows.id = ZINGOUTSIDESHOWTAGS.showid""", (result['id'],))
      showtags = []
      showTagResults = c.fetchall()
      for tag in showTagResults:
        if [tag['name'], tag['id']] in showtags:
          pass
        else:
          showtags.append([tag['name'], tag['id']])
      for tag in showtags:
        tag[0] = Markup(tag[0])
      result['showtags'] = showtags
      if result['publication'] == "http://www.philly.com/r?19=960&32=3796&7=195487&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fentertainment%2Farts":
        result['pub-image'] = "phillydotcom.png"
        result['pub-go'] = "philcom"
      if result['publication'] == "http://www.philly.com/r?19=960&32=3796&7=989523&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fblogs%2Fphillystage%2F":
        result['pub-image'] = "inq.png"
        result['pub-go'] = "inq"
      if result['publication'] == "http://www.newsworks.org/":
        result['pub-image'] = "shapiro.jpg"
        result['pub-go'] = "how-shap"
      if result['publication'] == "http://bsr2.dev/index.php":
        result['pub-image'] = "bsr.png"
        result['pub-go'] = "bsr"
      if result['publication'] == "http://citypaper.net":
        result['pub-image'] = "citypaper.png"
        result['pub-go'] = "city-paper"
      if result['publication'] == "http://phindie.com":
        result['pub-image'] = "phindie.png"
        result['pub-go'] = "phin"
      if result['publication'] == "http://www.philadelphiaweekly.com/arts-and-culture":
        result['pub-image'] = "pw.jpg"
        result['pub-go'] = "phil-week"
    results = resort(results)
    return render_template('fullreviews.html', results=results, title = "All Reviews", image = "none", count1 = int(len(results)/3), count2 = int(len(results)*2/3))

@app.route('/reviewsbyshow')
def reviewsbyshow():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT ZINGOUTSIDESHOWTAGS.showid, ZINGOUTSIDESHOWTAGS.articleid
                FROM ZingoutsideContent, ZINGOUTSIDESHOWTAGS
                WHERE ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id
                GROUP BY ZINGOUTSIDESHOWTAGS.showid, ZINGOUTSIDESHOWTAGS.articleid
                ORDER BY ZINGOUTSIDESHOWTAGS.showid ASC""")
    results = c.fetchall()
    byshowresults = []
    showTags = []

    for result in results:
      if result['showid'] in showTags:
        for x in byshowresults:
          if x['showid'] == result['showid']:
            x['articleids'].append(result['articleid'])
      else:
        showTags.append(result['showid'])
        c.execute("SELECT * from ZINGSHOWS where id = %s", (result['showid'],))
        name = c.fetchall()
        if len(name) >0:
          name = Markup(name[0]['name'])
          temp = {"showid" : result['showid'], "articleids": [result['articleid']], "name":name }
        else:
          temp = {"showid" : result['showid'], "articleids": [result['articleid']] }
        byshowresults.append(temp)
    for byshow in byshowresults:
      byshow['headlines'] = []
      byshow['links'] = []
      for article in byshow['articleids']:
        c.execute("""SELECT * FROM ZINGOUTSIDECONTENT
                    WHERE id = %s""", (article,))
        headlineData = c.fetchall()
        if len(headlineData) > 0:
          byshow['headlines'].append([Markup(headlineData[0]['title']), headlineData[0]['link']])
        



    #   result['descript'] = Markup(result['descript'])
    #   result['author'] = Markup(result['author'])
    #   # soup = BeautifulSoup(Markup(result['descript']))
    #   # result['descript'] = soup.get_text()
    #   print result['descript']
    #   c.execute("""SELECT ZINGOUTSIDESHOWTAGS.showid,
    #               ZINGShows.*
    #               FROM ZINGOUTSIDESHOWTAGS , ZINGSHOWS
    #               WHERE articleid = %s
    #               AND Zingshows.id = ZINGOUTSIDESHOWTAGS.showid""", (result['id'],))
    #   showtags = []
    #   showTagResults = c.fetchall()
    #   for tag in showTagResults:
    #     if [tag['name'], tag['id']] in showtags:
    #       pass
    #     else:
    #       showtags.append([tag['name'], tag['id']])
    #   for tag in showtags:
    #     tag[0] = Markup(tag[0])
    #   result['showtags'] = showtags
    #   if result['publication'] == "http://www.philly.com/r?19=960&32=3796&7=195487&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fentertainment%2Farts":
    #     result['pub-image'] = "phillydotcom.png"
    #     result['pub-go'] = "philcom"
    #   if result['publication'] == "http://www.philly.com/r?19=960&32=3796&7=989523&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fblogs%2Fphillystage%2F":
    #     result['pub-image'] = "inq.png"
    #     result['pub-go'] = "inq"
    #   if result['publication'] == "http://www.newsworks.org/":
    #     result['pub-image'] = "shapiro.jpg"
    #     result['pub-go'] = "how-shap"
    #   if result['publication'] == "http://bsr2.dev/index.php":
    #     result['pub-image'] = "bsr.png"
    #     result['pub-go'] = "bsr"
    #   if result['publication'] == "http://citypaper.net":
    #     result['pub-image'] = "citypaper.png"
    #     result['pub-go'] = "city-paper"
    #   if result['publication'] == "http://phindie.com":
    #     result['pub-image'] = "phindie.png"
    #     result['pub-go'] = "phin"
    #   if result['publication'] == "http://www.philadelphiaweekly.com/arts-and-culture":
    #     result['pub-image'] = "pw.jpg"
    #     result['pub-go'] = "phil-week"
    # print len(results)*2/3
    results = resort(byshowresults)
    return render_template('byshow.html', results=byshowresults, title = "All Reviews", image = "none", count1 = int(len(results)/3), count2 = int(len(results)*2/3))

@app.route('/reviewsbyreviewer')
def reviewsbyreviewer():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT ZingoutsideContent.*
                FROM ZingoutsideContent, ZINGOUTSIDESHOWTAGS
                WHERE ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id""")
    results = c.fetchall()
    byshowresults = []
    showTags = []
    articles = []

    for result in results:
      result['author'] = result['author'].strip()
      result['author'] = result['author'].replace("  ", " ")
      if result['author'] in showTags:
        for x in byshowresults:
          if x['showid'] == result['author']:
            if result['title'] in articles:
              pass
            else:
              x['headlines'].append([result['title'], result['link']])
              articles.append(result['title'])

      else:
        showTags.append(result['author'])
        temp = {"showid" : result['author'], "headlines": [[result['title'], result['link']]], "name" :  result['author']}
        byshowresults.append(temp)
    # for byshow in byshowresults:
    #   byshow['headlines'] = []
    #   byshow['links'] = []
    #   for article in byshow['articleids']:
    #     c.execute("""SELECT * FROM ZINGOUTSIDECONTENT
    #                 WHERE id = %s""", (article,))
    #     headlineData = c.fetchall()
    #     if len(headlineData) > 0:
    #       byshow['headlines'].append([Markup(headlineData[0]['title']), headlineData[0]['link']])
        



    #   result['descript'] = Markup(result['descript'])
    #   result['author'] = Markup(result['author'])
    #   # soup = BeautifulSoup(Markup(result['descript']))
    #   # result['descript'] = soup.get_text()
    #   print result['descript']
    #   c.execute("""SELECT ZINGOUTSIDESHOWTAGS.showid,
    #               ZINGShows.*
    #               FROM ZINGOUTSIDESHOWTAGS , ZINGSHOWS
    #               WHERE articleid = %s
    #               AND Zingshows.id = ZINGOUTSIDESHOWTAGS.showid""", (result['id'],))
    #   showtags = []
    #   showTagResults = c.fetchall()
    #   for tag in showTagResults:
    #     if [tag['name'], tag['id']] in showtags:
    #       pass
    #     else:
    #       showtags.append([tag['name'], tag['id']])
    #   for tag in showtags:
    #     tag[0] = Markup(tag[0])
    #   result['showtags'] = showtags
    #   if result['publication'] == "http://www.philly.com/r?19=960&32=3796&7=195487&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fentertainment%2Farts":
    #     result['pub-image'] = "phillydotcom.png"
    #     result['pub-go'] = "philcom"
    #   if result['publication'] == "http://www.philly.com/r?19=960&32=3796&7=989523&40=http%3A%2F%2Fwww.philly.com%2Fphilly%2Fblogs%2Fphillystage%2F":
    #     result['pub-image'] = "inq.png"
    #     result['pub-go'] = "inq"
    #   if result['publication'] == "http://www.newsworks.org/":
    #     result['pub-image'] = "shapiro.jpg"
    #     result['pub-go'] = "how-shap"
    #   if result['publication'] == "http://bsr2.dev/index.php":
    #     result['pub-image'] = "bsr.png"
    #     result['pub-go'] = "bsr"
    #   if result['publication'] == "http://citypaper.net":
    #     result['pub-image'] = "citypaper.png"
    #     result['pub-go'] = "city-paper"
    #   if result['publication'] == "http://phindie.com":
    #     result['pub-image'] = "phindie.png"
    #     result['pub-go'] = "phin"
    #   if result['publication'] == "http://www.philadelphiaweekly.com/arts-and-culture":
    #     result['pub-image'] = "pw.jpg"
    #     result['pub-go'] = "phil-week"
    # print len(results)*2/3
    results = resort(byshowresults)
    return render_template('byshow.html', results=byshowresults, title = "All Reviews", image = "none", count1 = int(len(results)/3), count2 = int(len(results)*2/3))

@app.route('/reviewsbyusers')
def reviewsbyusers():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT count(ZINGUSERREVIEWS.userid), userid
                from ZINGUSERREVIEWS
                GROUP BY userid
                ORDER BY count(ZINGUSERREVIEWS.userid) DESC
                """)
    topUsers = c.fetchall()
    byshowresults = []
    for x in topUsers:
      c.execute("""SELECT ZINGUSERREVIEWS.*, to_char(ZINGRATINGS.time, 'MMDDYYYY'), rating 
                  FROM ZINGUSERREVIEWS,ZingRatings 
                  where ZingRatings.showid = ZINGUSERREVIEWS.showID
                  and ZingRatings.userid = ZINGUSERREVIEWS.userid
                  and ZINGUSERREVIEWS.userid =%s""", (x['userid'],))
      reviews = c.fetchall()
      for review in reviews:
        c.execute("SELECT name from ZINGSHOWS WHERE id =%s", (review['showid'],))
        showname = c.fetchall()[0]['name']
        review['showname'] = showname
        review['rating'] = convert_to_percent(float(review['rating']))
      c.execute("SELECT * FROM USERS where id = %s", (x['userid'],))
      user =c.fetchall()[0]
      byshowresults.append([reviews,user])
    results = resort(byshowresults)
    return render_template("topUserReviews.html", results = results,title = "Top User Reviews", count1 = int(len(results)/3), count2 = int(len(results)*2/3) )





@app.route('/fulltheater')
def fulltheater():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # c.execute("""SELECT Karlshows2.name, SUM(rating), COUNT(rating)
    #              from Karlshows2, ShowRatings4
    #              WHERE (CURRENT_DATE, CURRENT_DATE)
    #              OVERLAPS (start_date, end_date)
    #              and ShowRatings4.showid = Karlshows2.id
    #              GROUP BY Karlshows2.name""")
    c.execute("SELECT * FROM Theatres ")
    results = c.fetchall()
    for result in results:
      result['description'] = Markup(result['description'])
      # c.execute("SELECT name FROM Theatres WHERE id = %s", (result['venueid'],))
      # venueResult = c.fetchall()
      # if len(venueResult)>0:
      #   venuename = venueResult[0]['name']
      # else:
      #   venuename = ""
      # result['venuename'] = Markup(venuename)
      result['name'] = Markup(result['name'])
      # result['start'] = str(result['start'])
      # result['enddate'] = str(result['enddate'])
      # monthfirst = result['start'].find("-")
      # monthlast = result['start'].rfind("-")
      # month = result['start'][monthfirst+1:monthlast]
      # day = result['start'][monthlast+1:]
      # year = result['start'][:4]
      # if day[0] == "0":
      #   day = day[1:]
      # result['start'] = months[month] + day 
      # monthfirst = result['enddate'].find("-")
      # monthlast = result['enddate'].rfind("-")
      # month = result['enddate'][monthfirst+1:monthlast]
      # day = result['enddate'][monthlast+1:]
      # if day[0] == "0":
      #   day = day[1:]
      # year = result['enddate'][:4]
      # result['enddate'] = months[month] + day + ", " +  year
 
    return render_template('fulltheatre.html', results=results, count = int(len(results)/2))


@app.route('/pastshows')
def pastshows():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # c.execute("""SELECT Karlshows2.name, SUM(rating), COUNT(rating)
    #              from Karlshows2, ShowRatings4
    #              WHERE (CURRENT_DATE, CURRENT_DATE)
    #              OVERLAPS (start_date, end_date)
    #              and ShowRatings4.showid = Karlshows2.id
    #              GROUP BY Karlshows2.name""")
    c.execute("SELECT * FROM ZINGSHOWS WHERE enddate < now() ORDER BY start ASC")
    results = c.fetchall()
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
      result['descript'] = Markup(result['descript'])
      c.execute("""SELECT SUM(rating), COUNT(rating)  FROM ZINGRATINGS
                    WHERE showid = %s""", (result['id'],))
      for a in c.fetchall():
        if a['sum'] != None:
          result['rating'] = convert_to_percent(float(a['sum'])/float(a['count']))
      c.execute("SELECT name FROM Theatres WHERE id = %s", (result['venueid'],))
      venueResult = c.fetchall()
      if len(venueResult)>0:
        venuename = venueResult[0]['name']
      else:
        venuename = ""
      result['venuename'] = Markup(venuename)
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
    results = resort(results)
    totalCountMod = len(results)%3
    return render_template('fullschedule.html', title = "Past Shows", results=results,totalCountMod = totalCountMod, count1 = int(len(results)/3), count2 = int(len(results)*2/3))

 ###returns a fullschedule of shows
@app.route('/tonight')
def tonight():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT ZINGSHOWS.* FROM ZINGSHOWS, SHOWDAYS WHERE SHOWDAYS.showid = ZINGSHOWS.id and SHOWDAYS.date = current_date GROUP BY Zingshows.id ORDER BY start ASC")
    results = c.fetchall()
    title = "Playing Tonight" 
    return fullScheduleTemplate(results, title)

@app.route('/weekend')
def weekend():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT ZINGSHOWS.* FROM ZINGSHOWS, SHOWDAYS 
                WHERE SHOWDAYS.showid = ZINGSHOWS.id 
                AND (SHOWDAYS.date, SHOWDAYS.date)
                OVERLAPS (current_date , current_date + interval '1 week')
                GROUP BY Zingshows.id ORDER BY start ASC""")
    results = c.fetchall()
    weekendResults = []
    for result in results:
      c.execute("""SELECT to_char(date, 'Day') from SHOWDAYS
                  WHERE SHOWDAYS.showid = %s
                  AND (SHOWDAYS.date, SHOWDAYS.date)
                  OVERLAPS (current_date , current_date + interval '1 week')""", (result['id'],))
      daysOfTheWeek = c.fetchall()
      weekend = False
      for day in daysOfTheWeek:
        if day['to_char'].strip() == "Friday" or day['to_char'].strip() == "Saturday" or day['to_char'].strip() == "Sunday":
          weekend = True
      if weekend:
        weekendResults.append(result)
    title = "Playing This Weekend" 
    return fullScheduleTemplate(weekendResults, title)



@app.route('/comedy')
def comedy():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT ZINGSHOWS.* FROM ZINGSHOWS, COMEDY WHERE COMEDY.showid = ZINGSHOWS.id GROUP BY Zingshows.id ORDER BY start ASC")
    results = c.fetchall()
    title = "Comedies" 
    return fullScheduleTemplate(results, title)

@app.route('/fringe')
def fringe():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT ZINGSHOWS.* FROM ZINGSHOWS, Fringe WHERE FRINGE.showid = ZINGSHOWS.id GROUP BY Zingshows.id ORDER BY start ASC")
    results = c.fetchall()
    title = "Fringe Festival" 
    return fullScheduleTemplate(results, title)

@app.route('/music')
def music():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT ZINGSHOWS.* FROM ZINGSHOWS, Musicals WHERE Musicals.showid = ZINGSHOWS.id GROUP BY Zingshows.id ORDER BY start ASC")
    results = c.fetchall()
    title = "Musicals" 
    return fullScheduleTemplate(results, title)

@app.route('/classics')
def classics():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT ZINGSHOWS.* FROM ZINGSHOWS, CLASSICS WHERE CLASSICS.showid = ZINGSHOWS.id GROUP BY Zingshows.id ORDER BY start ASC")
    results = c.fetchall()
    title = "Classics" 
    return fullScheduleTemplate(results, title)

@app.route('/drama')
def drama():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT ZINGSHOWS.* FROM ZINGSHOWS, DRAMA WHERE DRAMA.showid = ZINGSHOWS.id GROUP BY Zingshows.id ORDER BY start ASC")
    results = c.fetchall()
    title = "Dramas" 
    return fullScheduleTemplate(results, title)

@app.route('/experimen')
def experimen():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT ZINGSHOWS.* FROM ZINGSHOWS, Experimental WHERE EXPERIMENTAL.showid = ZINGSHOWS.id GROUP BY Zingshows.id ORDER BY start ASC")
    results = c.fetchall()
    title = "Experimental" 
    return fullScheduleTemplate(results, title)

@app.route('/emailList')
def emailList():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    email = request.args.get('email')
    c.execute("INSERT INTO emailList(email) VALUES(%s)", (email,))
    conn.commit()
    return ""

@app.route('/fullschedule')
def fullschedule():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # c.execute("""SELECT Karlshows2.name, SUM(rating), COUNT(rating)
    #              from Karlshows2, ShowRatings4
    #              WHERE (CURRENT_DATE, CURRENT_DATE)
    #              OVERLAPS (start_date, end_date)
    #              and ShowRatings4.showid = Karlshows2.id
    #              GROUP BY Karlshows2.name""")
    c.execute("SELECT * FROM ZINGSHOWS WHERE enddate > now() ORDER BY start ASC")
    results = c.fetchall()
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
      result['descript'] = Markup(result['descript'])
      c.execute("""SELECT SUM(rating), COUNT(rating)  FROM ZINGRATINGS
                    WHERE showid = %s""", (result['id'],))
      for a in c.fetchall():
        if a['sum'] != None:
          result['rating'] = convert_to_percent(float(a['sum'])/float(a['count']))
      c.execute("SELECT name FROM Theatres WHERE id = %s", (result['venueid'],))
      venueResult = c.fetchall()
      if len(venueResult)>0:
        venuename = venueResult[0]['name']
      else:
        venuename = ""
      result['venuename'] = Markup(venuename)
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
    results = resort(results)
    totalCountMod = len(results)%3
    return render_template('fullschedule.html', title = "Full Schedule", results=results,totalCountMod = totalCountMod, count1 = int(len(results)/3), count2 = int(len(results)*2/3))


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
    t = Twitter(
    auth=OAuth('2290030034-qZlpLizAAp8FqA21jumX3sWKmKc2VVAHAPw9nUZ', 'I7B4ALWQQLTNYQKzu37tKahle36JL9NsWT3RkCYCKWx2i', '8ddlpAyOG5fq2qCHoJcxQ', 'tbjoqSMYMOxKyJgeqpZ1EexqCxoOsm4OYwiizshtZY4'))
    venue = request.args.get('venue')
    # tweets = t.search.tweets(q="#"+showdata[0]['name'])
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT * from Theatres where id = %s", (venue,))
    results = c.fetchall()
    results = results[0]
    results['name'] = Markup(results['name'])
    twitterHandle = results['tw']
    twitterHandle = twitterHandle[twitterHandle.rfind("/")+1:]
    tweetsList = []
    if twitterHandle != "":
      tweets = t.statuses.user_timeline(screen_name=twitterHandle)
      tweetsList = []
      for tweet in tweets:
        tw = {}
        tw['created_at'] = tweet['created_at']
        if len(tweet['entities']['urls']) > 0:
          tw['links'] = []
          for x in tweet['entities']['urls']:
            tw['links'].append(x['url'])
        if 'media' in tweet['entities'].keys():
          tw['media'] = tweet['entities']['media'][0]['media_url']
        else:
          tw['media'] = ""
        tweetText = tweet['text']
        testText = tweetText
        http = tweetText[tweetText.find("http"):]
        http = http[:http.find(" ")]
        tweetText = tweetText.replace(http, "")
        tw['text'] = tweetText
        tweetsList.append(tw)
      tweetsList = resort(tweetsList)
    else:
      tweets = []
      
      # while testText.find("http")>0:
      #   truncatenum = testText.find("http")
      #   link = testText[truncatenum:]
      #   truncatenum = truncatenum + link.find(" ")
      #   link = link[:link.find(" ")]
      #   print link
      #   testText = testText[truncatenum:]
      #   print testText

   
    results['descript'] = Markup(results['descript'])
    c.execute("SELECT * from Karlstaff where theatre = %s", (results['name'],))
    employees = c.fetchall()
    c.execute("""SELECT * from ZINGSHOWS
                 where venueid = %s """, (venue,))
    shows = c.fetchall()
    articles = []
    for show in shows:
      show['name'] = Markup(show['name'])
      show['descript'] = Markup(show['descript'])
      c.execute("""SELECT SUM(rating), COUNT(rating)  FROM ZINGRATINGS
                    WHERE showid = %s""", (show['id'],))
      for a in c.fetchall():
        if a['sum'] != None:
          show['rating'] = convert_to_percent(float(a['sum'])/float(a['count']))


    return render_template('blog-post-venue.html', venuedata=results,
                           staff=employees, useron='none',
                           showdata=shows, articles = articles,
                           tweets = tweetsList, tweetCount1 = int(len(tweets) /3)
                           , tweetCount2 = int(len(tweets)*2 / 3))

# To A SHOW -- TAKES AN ID, right now connects to twitter but am doing nothing with it 
@app.route('/show', methods=['GET', 'POST'])
def show():
    t = Twitter(
    auth=OAuth('2290030034-qZlpLizAAp8FqA21jumX3sWKmKc2VVAHAPw9nUZ', 'I7B4ALWQQLTNYQKzu37tKahle36JL9NsWT3RkCYCKWx2i', '8ddlpAyOG5fq2qCHoJcxQ', 'tbjoqSMYMOxKyJgeqpZ1EexqCxoOsm4OYwiizshtZY4'))
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    show = request.args.get('show')
    c.execute("SELECT * from ZINGSHOWS where id = %s", (show,))
    showdata = c.fetchall()
    c.execute("SELECT to_char(date, 'Day: Month, DD YYYY HH:MI') from SHOWDAYS where showid = %s",(show,))
    days = c.fetchall()
    for day in days:
      tempDay = day['to_char']
      if tempDay.find("12:00") >0:
        tempDay = tempDay.replace("12:00", "")
        day['to_char'] = tempDay
    c.execute("SELECT * FROM ZINGSHOWS where id = %s AND enddate>= now() AND start <= now() ", (show,))
    nowplaying =c.fetchall()
    if len(nowplaying)>0:
      showdata[0]['nowplaying'] ="yes"
    c.execute("SELECT * FROM ZINGSHOWS where id = %s AND start > now() ", (show,))
    futureshow =c.fetchall()
    if len(futureshow)>0:
      showdata[0]['nowplaying'] ="future"
    c.execute("SELECT * FROM ZINGSHOWS where id = %s AND enddate < now() ", (show,))
    pastshow =c.fetchall()
    if len(pastshow)>0:
      showdata[0]['nowplaying'] ="past"
    tweets = t.search.tweets(q="#"+showdata[0]['name'])
    # print tweets['search_metadata']
    # for tweet in tweets['statuses']:
    #   print "/n"
    #   print tweet['text']
    #   print tweet['source']
    if len(showdata)>0:
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
      for result in showdata:
      
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
      # c.execute("""SELECT Karlactors.actorName, Karlcasting.role
      #           from Karlactors, Karlcasting
      #           where showID = %s and Karlactors.id = Karlcasting.actorID""",
      #           (showdata[0]['id'],))
      casting = c.fetchall()
      c.execute("SELECT * FROM ZINGSHOWS where venueid =%s", (showdata[0]['venueid'],))
      venueShows = c.fetchall()
      for venueshow in venueShows:
        venueshow['name'] = Markup(venueshow['name'])
        venueshow['descript'] = Markup(venueshow['descript'])
        venueshow['start'] = str(venueshow['start'])
        venueshow['enddate'] = str(venueshow['enddate'])
        monthfirst = venueshow['start'].find("-")
        monthlast = venueshow['start'].rfind("-")
        month = venueshow['start'][monthfirst+1:monthlast]
        day = venueshow['start'][monthlast+1:]
        year = venueshow['start'][:4]
        if day[0] == "0":
          day = day[1:]
        venueshow['start'] = months[month] + day 
        monthfirst = venueshow['enddate'].find("-")
        monthlast = venueshow['enddate'].rfind("-")
        month = venueshow['enddate'][monthfirst+1:monthlast]
        day = venueshow['enddate'][monthlast+1:]
        if day[0] == "0":
          day = day[1:]
        year = venueshow['enddate'][:4]
        venueshow['enddate'] = months[month] + day + ", " +  year
      c.execute("""SELECT * from Theatres
                where id = %s""", (showdata[0]['venueid'],))

      venue = c.fetchall()
      venue[0]['name'] = Markup(venue[0]['name'])
      venue[0]['descript'] = Markup(venue[0]['descript'])
      #and ZINGUSERREVIEWS.private = %s
      c.execute("""SELECT reviewText, ZINGUSERREVIEWS.userid, 
                rating, to_char(ZINGRATINGS.time, 'MMDDYYYY')
                from ZINGRATINGS, ZINGUSERREVIEWS
                where ZINGUSERREVIEWS.showid = %s 
                and ZINGRATINGS.showid = %s
                and ZINGUSERREVIEWS.private = %s
                and ZINGUSERREVIEWS.userid = ZINGRATINGS.userid""", (showdata[0]['id'],showdata[0]['id'], "no"))
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
      outsideArticles = []
      outsideArticleIDs = []
      for article in articleids:
        if article['articleid'] in outsideArticleIDs:
          pass
        else:
          outsideArticles.append(article)
          outsideArticleIDs.append(article['articleid'])
      
      numReviews = len(results)
      averageRating = 0
      yourRating = 0
      reviewtexts = []
      for review in userreviews:
        data = []
        text = review['reviewtext']
        rating = review['rating']
        c.execute("""SELECT first, last 
                    from USERS where id = %s""", 
                    (review['userid'],))
        username = c.fetchall()
       
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
      c.execute("""SELECT COUNT(*) 
                FROM SHOWCOUNT
                WHERE showid = %s""", (show,))
      count = str(c.fetchall()[0]['count'])
      template_vars = {"showdata": showdata[0],
                        "days": days,
                      "producer": producer,
                       "description": description,
                       "headerDescription": headerDescription,
                       "useron": 'none',
                       "count": count,
                       "ratingCount": int(results[0]['count']),
                       "cast": casting, "venue": venue,
                       "userreviews": reviewtexts,
                       "rating": averageRating,
                       "yourRating": yourRating,
                       "goodadjectives": goodadjectives,
                       "badadjectives": badadjectives,
                       "articles": outsideArticles,
                       "twitterurl":twitterurl,
                       "venueShows": venueShows
                       }
      if 'username' in session:
          # c.execute("""SELECT rating
          #           from ZINGRATINGS, USERS
          #           where ZINGRATINGS.userid = ZINGRATINGS.id
          #           and USERS.id = %s
          #           and ZINGRATINGS.showID = %s""",
          #           (session['username'], showdata[0]['id']))
          # yourRating = c.fetchall()
          # if len(yourRating) == 1:
          #     yourRating = yourRating[0]['rating']
          #     yourRating = convert_to_percent(yourRating)

          c.execute("SELECT first, last, emailconfirm from USERS where id = %s", (session['username'],))
          userinfo = c.fetchall()[0]
          name = userinfo['first'] + " " +userinfo['last']
          emailconfirm = userinfo['emailconfirm']
          if emailconfirm:
            template_vars['useron'] = name
          else:
            template_vars['useron'] = "confirm email"
      return render_template("blog-post.html", **template_vars)
    return render_template("error.html")

@app.route('/profile')
def profile():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    username = session['username']
    c.execute("SELECT * from Users where id = %s", (username,))
    userdata = c.fetchall()[0]
    c.execute("""SELECT USERS.first, reviewText, rating,
              to_char(ZINGRATINGS.time, 'HHMIA.M.DayMonthDDYYY')
              from ZINGUSERREVIEWS, ZINGRATINGS, ZINGSHOWS, USERS
              where ZINGUSERREVIEWS.userid = ZINGRATINGS.userid
              and ZINGRATINGS.userid =%s
              and ZINGSHOWS.id = ZINGRATINGS.showid
              and ZINGSHOWS.id = ZINGUSERREVIEWS.showid""",
              (username,))
    results = c.fetchall()
    c.execute("""SELECT * FROM ZINGSURVEY
                WHERE userid = %s""", (session['username'],) )
    surveydata = c.fetchall()
    likes = [None]*5
    if len(surveydata) > 0:
      surveydata = surveydata[0]
      likes[surveydata['comedy'] -1 ] = "Comedy"
      likes[surveydata['musicals'] -1 ] = "Musicals"
      likes[surveydata['experimental'] -1 ] = "Experimental"
      likes[surveydata['drama'] -1 ] = "Drama"
      likes[surveydata['classics'] -1 ] = "Classics"

    c.execute("""SELECT * FROM COMMITMENT
                WHERE USERID = %s""", (session['username'],))
    commitment = c.fetchall()
    if len(commitment) > 0:
      commitment = commitment[0]
    c.execute("""SELECT reviewText, ZINGUSERREVIEWS.userid, 
                rating, to_char(ZINGRATINGS.time, 'MMDDYYYY'), ZINGRATINGS.showid,
                ZINGSHOWS.name
                from ZINGRATINGS, ZINGUSERREVIEWS, ZINGSHOWS
                where ZINGUSERREVIEWS.userid = %s
                and ZINGUSERREVIEWS.userid = ZINGRATINGS.userid
                and ZINGUSERREVIEWS.showid = ZINGRATINGS.showid
                and ZINGUSERREVIEWS.showid = ZINGSHOWS.id""", (session['username'],))
    userreviews = c.fetchall()
    for review in userreviews:
      c.execute("""SELECT *
                from ZINGGOODADJECTIVES 
                where userid = %s
                and showid = %s
                GROUP BY showid, id
                """, (session['username'],review['showid']))
      review['goods'] = c.fetchall()
      c.execute("""SELECT *
                from ZINGBADADJECTIVES 
                where userid = %s
                and showid = %s
                GROUP BY showid, id
                """, (session['username'],review['showid']))
      review['bads'] = c.fetchall()
      review['rating'] = convert_to_percent(float(review['rating']))
      date = review['to_char']
      review['to_char'] = date[1:2] + "/" + date[2:4] + "/" + date[4:]
    c.execute("""SELECT * FROM SHOWCOUNT, ZINGSHOWS
                  WHERE userid = %s
                  AND SHOWCOUNT.showid = ZINGSHOWS.id""", (session['username'],))
    sawthis = c.fetchall()
    return render_template('userprofile.html',
                           commitment = commitment,
                           username=username,
                           userdata=userdata,
                           survey=surveydata,
                           useron=username,
                           userreviews=userreviews,
                           sawthis=sawthis,
                           results=results,
                           likes = likes,
                            count = int(len(userreviews)/2))

###ajax route for search box autocomplete
@app.route('/autocomplete/allshows', methods=['GET', 'POST'] )
def autocomplete():
  query = request.args.get('query')
  query = '%' + query.lower() + '%'
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT name, id from ZINGSHOWS
            where lower(name) LIKE %s""", (query,))
  results = c.fetchall()
  c.execute("""SELECT name, id from Theatres
            where lower(name) LIKE %s""", (query,))
  results2 = c.fetchall()
  jsonresults = []
  for result in results:
     d = {'value': Markup(result['name']), 'data': result['id'], 'type':"show"}
     jsonresults.append(d)
  for result2 in results2:
     d = {'value': Markup(result2['name']), 'data': result2['id'], "type":"venue"}
     jsonresults.append(d)

  return jsonify(query = "Unit", suggestions = jsonresults)

###ajax route for search review autocomplete
@app.route('/autocomplete/justshows', methods=['GET', 'POST'] )
def autocompletejustshows():
  query = request.args.get('query')
  query = '%' + query.lower() + '%'
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("""SELECT name, id from ZINGSHOWS
            where lower(name) LIKE %s""", (query,))
  results = c.fetchall()
  jsonresults = []
  for result in results:
     d = {'value': result['name'], 'data': result['id'], 'type':"show"}
     jsonresults.append(d)
  return jsonify(query = "Unit", suggestions = jsonresults)




@app.route('/sawthis', methods=['GET', 'POST'])
def sawthis():
    showID = int(request.args.get('id'))
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if 'username' in session:
      userid = session['username']
      c.execute("""DELETE FROM SHOWCOUNT 
                WHERE userid = %s
                AND showid = %s""", (userid, showID))
      c.execute("""INSERT INTO SHOWCOUNT(userid, showid) 

                VALUES(%s, %s)""", (userid, showID))
    c.execute("""SELECT COUNT(*) 
                  FROM SHOWCOUNT
                  WHERE showid = %s""", (showID,))
    count = str(c.fetchall()[0]['count'])
    conn.commit()
    return count

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
    private = request.args.get('checkPrivate')
  
    userid = session['username']
    c.execute("""DELETE from ZINGUSERREVIEWS
              where userid = %s and showid = %s""",
              (userid, showID))
    if rating != None:
      c.execute("SET TIME ZONE 'America/New_York'")
      c.execute("""INSERT INTO ZINGUSERREVIEWS(userid, showID, reviewText, private)
              VALUES(%s, %s, %s, %s)""", (userid, showID, review, private))
      c.execute("""DELETE from ZINGRATINGS
              where userid = %s and showid = %s""",
              (userid, showID))
      c.execute("""INSERT INTO ZINGRATINGS(userid, rating, showID, time)
              VALUES(%s, %s, %s, CURRENT_TIMESTAMP)""",
              (userid, rating, showID))
    c.execute("""DELETE FROM ZINGGOODADJECTIVES
                    WHERE userid= %s and showid = %s""", (userid,showID))
    c.execute("""DELETE FROM ZINGBADADJECTIVES
                    WHERE userid= %s and showid = %s""", (userid, showID))
    for good in goods:
      
      c.execute("""INSERT INTO ZINGGOODADJECTIVES(showid, adjective, userid)
                VALUES(%s,%s,%s)""",
                (showID, good, userid))
    for bad in bads:
      c.execute("""INSERT INTO ZINGBADADJECTIVES(showid, adjective, userid)
                VALUES(%s,%s,%s)""",
                (showID, bad, userid))
    conn.commit()
    c.execute("SELECT email, first FROM USERS WHERE id = %s", (session['username'],))
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
@app.route('/fblogin', methods=['GET','POST'])
def fblogin():
  email = request.form['email']
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT ID, emailconfirm FROM USERS WHERE EMAIL = %s", (email,))
  results = c.fetchall()

  if results[0]['emailconfirm']:
    session['username'] = results[0]['id']
    return redirect(url_for('index'))
  else:
    return "<h3> A confirmation email has been sent. Please check your email and click the link to verify your account. </h3>"

@app.route('/login', methods=['GET', 'POST'])
def login():
  email = request.form['email']
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT ID, emailconfirm FROM USERS WHERE EMAIL = %s", (email,))
  results = c.fetchall()
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

@app.route('/removeBulkOutReview', methods = ['GET', 'POST'])
def removeBulkOutReview():
   c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
   articleids = json.loads(request.args.get('articleids'))
   for this in articleids:
      c.execute("""DELETE FROM ZINGOUTSIDECONTENT WHERE 
              id = %s""", (this,))
      c.execute("""DELETE FROM ZINGOUTSIDESHOWTAGS WHERE 
              articleid = %s""", (this,))
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

@app.route('/addtag', methods = ['GET', 'POST'])
def addtag():
   c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
   articleid = request.args.get('reviewid')
   showid = request.args.get('showid')
   c.execute("""INSERT INTO ZINGOUTSIDESHOWTAGS(articleid, showid)
              VALUES(%s, %s)""", (articleid,showid))
   conn.commit()
   return "did it"

@app.route('/manageGenre', methods =['GET', 'POST'])
def manageGenre():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT * FROM ZINGSHOWS")
  shows = c.fetchall()
  for show in shows:
    show['name'] = Markup(show['name'])
  return render_template("manageGenre.html", shows = shows)

@app.route('/addshow', methods =['GET', 'POST'])
def addshow():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT * FROM THEATRES")
  theatres = c.fetchall()
  for theatre in theatres:
    theatre['name'] = Markup(theatre['name'])
  return render_template("addShows.html", theatres = theatres)


@app.route('/publishShow', methods =['GET', 'POST'])
def pubShow():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  prod = request.args.get('producer')
  title = request.args.get('title')
  start = request.args.get('start')
  end = request.args.get('end')
  descript = request.args.get('descript')
  venue = request.args.get('venue')
  genre = request.args.get('genre')
  c.execute("""INSERT INTO ZINGSHOWS
                (name, descript, producer, venueid,
                  start, enddate) VALUES(
                  %s,%s,%s,%s,%s,%s)""",
              (title, descript, prod, venue, start, end))
  conn.commit()
  c.execute("""SELECT id from ZINGSHOWS
                WHERE name = %s""",
                (title,))
  showid = c.fetchall()[0]['id']
  if genre == "Comedy":
    c.execute("INSERT INTO Comedy(showid) values(%s)", (showid,))
  if genre == "Fringe":
    c.execute("INSERT INTO Fringe(showid) values(%s)", (showid,))
  if genre == "Experimental":
    c.execute("INSERT INTO Experimental(showid) values(%s)", (showid,))
  if genre == "Classics":
    c.execute("INSERT INTO Classics(showid) values(%s)", (showid,))
  if genre == "Drama":
    c.execute("INSERT INTO Drama(showid) values(%s)", (showid,))
  if genre == "Musical":
    c.execute("INSERT INTO Musicals(showid) values(%s)", (showid,))
  conn.commit()
  session['showid'] = showid
  return str(showid)


@app.route('/genreSubmit', methods =['GET', 'POST'])
def genreSubmit():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  showid = str(request.args.get('show'))
  genre = request.args.get('genre')

  if genre == "Comedy":
    c.execute("INSERT INTO Comedy(showid) values(%s)", (showid,))
  if genre == "Fringe":
    c.execute("INSERT INTO Fringe(showid) values(%s)", (showid,))
  if genre == "Experimental":
    c.execute("INSERT INTO Experimental(showid) values(%s)", (showid,))
  if genre == "Classics":
    c.execute("INSERT INTO Classics(showid) values(%s)", (showid,))
  if genre == "Drama":
    c.execute("INSERT INTO Drama(showid) values(%s)", (showid,))
  if genre == "Musical":
    c.execute("INSERT INTO Musicals(showid) values(%s)", (showid,))
  conn.commit()
  return ""


@app.route('/manageOutReviews', methods=['GET', 'POST'])
def manageOutReviews():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  c.execute("SELECT ZINGOUTSIDECONTENT.*, ZINGOUTSIDESHOWTAGS.showID FROM ZINGOUTSIDECONTENT, ZINGOUTSIDESHOWTAGS where ZINGOUTSIDESHOWTAGS.articleid = ZINGOUTSIDECONTENT.id GROUP BY ZingoutsideContent.id, ZINGOUTSIDESHOWTAGS.showID ORDER BY ZINGOUTSIDECONTENT.id DESC")
  results = c.fetchall()
  for review in results:
    c.execute("SELECT name from ZINGSHOWS WHERE id = %s", (review['showid'],))
    showname = c.fetchall()
    if len(showname)>0:
      review['showname'] = showname
    else:
      review['showname'] = "No tag"
    c.execute("SELECT * from SNIPPETS WHERE articleid = %s", (review['id'],))
    snippets = c.fetchall()      
    review['snippets'] = snippets
  return render_template("manageOutsideReviews.html", results = results, count1 = int(len(results)/3), count2 = int(len(results)*2/3))


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
        text = review['reviewtext']
        rating = review['rating']
        c.execute("""SELECT first, last, id 
                    from USERS where id = %s""", 
                    (review['userid'],))
        username = c.fetchall()
     
        data.append(text)
        rating = convert_to_percent(float(rating))
        data.append(rating)
        data.append(username)
        date = review['to_char']
        date = date[1:2] + "/" + date[2:4] + "/" + date[4:]
        data.append(date)
        
        data.append(review['id'])
        data.append(review['showid'])
        c.execute("""SELECT ZINGSHOWS.name FROM ZINGSHOWS
                  WHERE id = %s""", (review['showid'],))
        showname = c.fetchall()
        if len(showname) > 0:
          data.append(Markup(showname[0]['name']))
        reviewtexts.append(data)
  return render_template("manageReviews.html", userreviews = reviewtexts, count1 = int(len(reviewtexts)/3), count2 = int(len(reviewtexts)*2/3))



###return a description of Zing
@app.route('/topPanel')
def topPanel():
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("""SELECT name, id
                 from ZINGSHOWS
                 WHERE (start,enddate)
                 OVERLAPS (CURRENT_DATE, CURRENT_DATE)
               """)
    results = c.fetchall()
    return render_template('ads.html', results=results)



@app.route('/zingDescript')
def zingDescript():
  return render_template('zingdescription.html')

@app.route('/getsurvey')
def getsurvey():
  return render_template('usersurvey.html')

@app.route('/donesurvey')
def donesurvey():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  yes = request.args.get('yes')
  no = request.args.get('no')
  prefs = request.args.get('prefs')
  prefs  = json.loads(prefs)
  commitment = request.args.get('commitment')
  worksin = False
  if yes =="true":
    worksin = True
  drama = prefs['drama']
  comedy = prefs['comedy']
  musicals = prefs['musicals']
  classics = prefs['classics']
  experimental = prefs['experimental']
  c.execute("""SELECT * FROM ZINGSURVEY
              WHERE userid = %s""", (session['username'],))
  if len(c.fetchall()) > 0:
    c.execute("DELETE FROM ZINGSURVEY WHERE userid = %s", (session['username'], ))
  c.execute("""SELECT * FROM COMMITMENT
              WHERE userid = %s""", (session['username'],))
  if len(c.fetchall()) > 0:
    c.execute("DELETE FROM COMMITMENT WHERE userid = %s", (session['username'], ))
  c.execute("""INSERT INTO ZINGSURVEY(userid, comedy, drama, 
            experimental, classics, musicals, worksin) 
            VALUES(%s,%s,%s,%s, %s, %s,%s)""",
            [session['username'], comedy, drama, 
            experimental, classics, musicals, worksin])
  c.execute("""INSERT into COMMITMENT(userid, commitment)
            VALUES(%s,%s)""", (session['username'], commitment))
  conn.commit()
  return "survey complete"

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
