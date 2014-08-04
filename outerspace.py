import connectionBoiler
conn = connectionBoiler.get_conn()
c = conn.cursor()

c.execute("""UPDATE fringeshows SET description = ' <p>Experiments on the frontier of dance.</p>
        
      <p>Three wildly contemporary choreographers create three new experimental dances on the Pennsylvania Ballet&#39;s classically trained dancers, with music composed and performed by alumni of the Curtis Institute. A high-stakes artistic dare, the collaboration begins when the dance makers (from Israel, Austria, and Seattle), dancers, and musicians meet each other for the first time, and then create the dances from scratch based on the interactions of their artistry&mdash;only three weeks before opening night! Expect a virtuosic, highly creative program of dance unlike any seen before.</p>
        
      <p>Choreographers: Georg Reischl, Zoe Scofield, Itamar Serussi</p>
 ' where id = 886""")
c.execute("""UPDATE fringeshows SET venueid = 90  where id = 886""")


conn.commit()