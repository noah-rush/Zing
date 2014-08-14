#!/usr/bin/env python

from xlrd import open_workbook
import urllib2  # the lib that handles the url stuff

from tempfile import TemporaryFile
from xlwt import Workbook
book = Workbook()
sheet1 = book.add_sheet('Venues')
sheet1.write(0,0,'id')
sheet1.write(0,1,'name')
sheet1.write(0,2,'address')



target_url = "http://www.livearts-fringe.org/festival/index.cfm"
data = urllib2.urlopen(target_url) # it's a file like object and works just like a file

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import connectionBoiler

conn=connectionBoiler.get_conn()

def findVenue(str):
    c = conn.cursor()
    url = str
    driver4 = webdriver.Firefox()
    driver4.get(url)
    try:
        element = WebDriverWait(driver4, 10).until(EC.presence_of_element_located((By.ID, "GAVenueName")))
	
    finally:
        venue = driver4.find_element_by_id('GAVenueName')
        address = driver4.find_element_by_id('GAVenueDetail')
        ventext = element.get_attribute("innerHTML")
        addtext = address.text
        ventext = ventext.encode('ascii','ignore')
        addtext = addtext.encode('ascii', 'ignore')
        addtext = addtext.strip()
        venueName = ventext[ventext.find(":")+2:]
        driver4.quit()
        c.execute("SELECT * from Fringevenues where name = %s", (venueName,))
        if c.fetchall() == [] and len(venueName)>3:
            c.execute("INSERT INTO Fringevenues(name, address) VALUES(%s, %s)", (venueName, addtext))
            conn.commit()
        print venueName
        print addtext
        c.execute("SELECT id from Fringevenues where name = %s", (venueName,))
        venueid = c.fetchall()[0]
        return venueid
        

	
	
def findData(str):
    c = conn.cursor()
    url = str
    venueFound = False
    driver = webdriver.Firefox()
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "DetailsOfEvent")))
    finally:
        data = driver.find_element_by_id('DetailsOfEvent')
        instance = driver.find_elements_by_class_name('instanceName')
        elem = data.text
        counter = 0
        producer = ""
        description = ""
        title = ""
        linkOne =""
        for text in iter(elem.splitlines()):
            if counter == 0:
        	   title = text
            if counter == 1:
                producer = text
            if counter == 2:
                description =text
            counter = counter +1
        src =""
        try: 
            img = data.find_element_by_tag_name("img")
            src = img.get_attribute("src")
            # print src
        except Exception:
            pass
        title = title.encode('ascii','ignore')
        src = src.encode('ascii','ignore')
        producer = producer.encode('ascii','ignore')
        description = description.encode('ascii','ignore')
        linkOne = linkOne.encode('ascii', 'ignore')
        if len(title) > 3:
            c.execute("SELECT * FROM Fringeshows where name = %s", (title,))
            if c.fetchall() == []:
                c.execute("INSERT INTO Fringeshows(name, producer, description, pic) VALUES(%s, %s, %s,%s)", (title, producer, description,src))
                c.execute("SELECT id from Fringeshows where name = %s", (title,))
                showid = c.fetchall()[0][0]
                for date in instance:
                    elem2 = date.text
                    link = date.get_attribute("href")
                    if(not(link is None)):
                        elem2 = elem2.encode('ascii','ignore')
                        link = link.encode('ascii','ignore')
                        print link
                        print elem2
                        last =elem2.rfind(",")
                        first = elem2.find(".")
                        if first ==-1:
                            first = elem2.rfind("t")
                        if last < elem2.find("."):
                            last = elem2.rfind("-")-1
                        date = elem2[first+2:last]
                        date = "September " + date +", 2014"
                        c.execute("INSERT INTO Fringedates(showid, playing, ticketlink, playingdate) VALUES(%s, %s, %s, %s)", (showid, elem2, link, date))
                        if(not(venueFound)):
                            linkOne = link
                            venueid = findVenue(linkOne)
                            c.execute("UPDATE Fringeshows SET venueid = %s where id = %s", (venueid, showid))
                            venueFound = True
        conn.commit()
        driver.quit()
        # print producer
        # print description
        # #print src




def main():
    counter = 0
    for line in data:
        if "Comedy" in line:
            test = ""
            while(not("<div id=\"footer\">" in test)):
                test = data.next()
                if("a href" in test):
                    counter = counter + 1
                    first = test.find("\"")+1
                    last = test.find("\">")
                    link = test[first:last]
                    findData(link)
     #            linkOne = lotsadata[0][0]
     #            print lotsadata
     #            #findVenue(linkOne)
    print counter



				






	