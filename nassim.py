import connectionBoiler
conn = connectionBoiler.get_conn()
c = conn.cursor()


c.execute("""INSERT INTO Fringeshows(Name, Venueid, Description, Pic, Producer) 
	VALUES('White Rabbit Red Rabbit', 92, 
		'In a brilliant paradox, Soleimanpour exerts deliberate and 
		near-total control over an actor and an audience from his own isolation in Tehran.        Nelson Pressley        
         <p>A different actor at each performance reads for the first (and last) time, the true life story of a young Iranian.
          Will you really listen?</p>
          <p>On stage in a sealed envelope the script awaits as the audience arrives. 
          An actor, who has never read the script, steps on stage and opens the envelope. 
          Now, the audience seated, the actor performs the script for the first&mdash;and last&mdash;time. 
          And then a carrot, a ladder, a rabbit, a bear, a circus, some poison, a playwright, an actor, and the 
          audience are ensnared in this wild theatrical adventure. Unable to leave his country, Iranian playwright Nassim Soleimanpour 
          created <em>White Rabbit Red Rabbit</em> to travel the world when he couldn&#39;t, 
          and speak to audiences in his stead.</p>','http://www.livearts-fringe.org!/img/preview/2014/rabbit.jpg', 'Nassim Soleimanpour (Iran)')""")

conn.commit()