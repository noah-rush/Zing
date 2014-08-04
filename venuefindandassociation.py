
import psycopg2
import psycopg2.extras
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import connectionBoiler

conn=connectionBoiler.get_conn()

def associate(a,s):
    c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    c.execute("SELECT venueid from Fringeshows where id = %s", (a,))
    results = c.fetchall()[0]
    venueid = results['venueid']
    if venueid is None:
        driver4 = webdriver.Firefox()
        driver4.get(s)
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
            results = c.fetchall()
            if results == [] and len(venueName)>3:
                c.execute("INSERT INTO Fringevenues(name, address) VALUES(%s, %s)", (venueName, addtext))
                conn.commit()
                c.execute("SELECT id from Fringevenues where name = %s", (venueName,))
                results = c.fetchall()
                venueid = results[0]['id']
                c.execute("UPDATE Fringeshows SET venueid = %s where id = %s", (venueid, a))
                conn.commit()
            elif len(venueName)>3: 
                venueid = results[0]['id']
                c.execute("UPDATE Fringeshows SET venueid = %s where id = %s", (venueid, a))
                conn.commit



        	print venueName
        	print addtext
        	
        	
		





def main():
	c = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	c.execute("SELECT ticketlink, showid from Fringedates GROUP BY showid, ticketlink ORDER BY showid !asc")
	results = c.fetchall()
	for result in results:
		showid = result['showid']
		ticketlink = result['ticketlink']
		associate(showid, ticketlink)


if __name__ == '__main__':
	main()
