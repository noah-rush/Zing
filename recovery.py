import os
import psycopg2
import psycopg2.extras
import urlparse
from flask import render_template, jsonify, Flask
from flask import request, escape, session, url_for, redirect, Markup, Response
import sys
from werkzeug.security import generate_password_hash, \
    check_password_hash
from werkzeug import security
import json


import connectionBoiler
conn = connectionBoiler.get_conn()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        
        c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        c.execute("SELECT first from KarlUsers2 where id = %s", (session['username'],))
        name = c.fetchall()[0]['first']
        print name
        return render_template('layout.html', useron=name)
    print 'kkkkk'
    return render_template('layout.html', useron = 'none')

@app.route('/home', methods=['GET', 'POST'])
def home():
  c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
  featuredids = [876,877,878,879,880,881,882,883,884,885,886,887]
  c.execute("SELECT name,id from Fringeshows where id>875 and id <888")
  featured = c.fetchall()
  print featured
  return render_template("todayscontent.html", featured = featured)

  
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
      c.execute("""SELECT Fringeshows.name, playing, ticketlink,to_char(playingdate,'Day'), Fringeshows.id from Fringeshows, Fringedates2 where Fringedates2.showid = Fringeshows.id and playingdate = CURRENT_DATE + %s""", (iterator,))
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
              result.append("none")
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
 

if __name__ == "__main__":
    app.run(debug=True)