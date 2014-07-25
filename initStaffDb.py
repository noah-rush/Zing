import os
import psycopg2
import urlparse
from xlrd import open_workbook


def main():
  wb = open_workbook('zingTheaterMarketingDirectory.xlsx')
  urlparse.uses_netloc.append("postgres")
  url = urlparse.urlparse(os.environ["DATABASE_URL"])

  conn = psycopg2.connect(
      database=url.path[1:],
      user=url.username,
      password=url.password,
      host=url.hostname,
      port=url.port
  )



  c = conn.cursor()

  c.execute("CREATE TABLE Karlstaff(id serial PRIMARY KEY, theatre VARCHAR(100), name VARCHAR(500), title VARCHAR(500), email VARCHAR(500))")
  sheet = wb.sheet_by_index(2) 

  for row in range(sheet.nrows):
      values = []
      for col in range(sheet.ncols):
          values.append(sheet.cell_value(row,col))
    #numTitles = values[2].count("-")
      splitnum = values[2].find(",")
      while True:
          if splitnum == -1:
              break
          employee = []
          theatre = values[1]
          staffName_staffTitle = values[2][0:splitnum]
          title_split = staffName_staffTitle.find(" - ")
          name = staffName_staffTitle[:title_split]
          title = staffName_staffTitle[(title_split+3):]
          emailSplit = values[3].find(",")
          email = values[3][0:emailSplit]
          employee.append(theatre)
          employee.append(name)
          employee.append(title)
          employee.append(email)
          if employee[1] != "" and employee[1] != " ":
              print employee
              c.execute("INSERT INTO Karlstaff(theatre, name,title,email) VALUES(%s, %s, %s, %s)", (employee[0], employee[1], employee[2], employee[3]))
          values[2] = values[2][(splitnum+2):]
          values[3] = values[3][(emailSplit+1):]
          splitnum = values[2].find(",")
      if values[2] != "" and values[2] != " ":
          employee = []
          theatre = values[1]
          staffName_staffTitle = values[2]
          title_split = staffName_staffTitle.find(" - ")
          if title_split == -1:
              name = staffName_staffTitle
              email= values[3]
              employee.append(theatre)
              employee.append(name)
              employee.append("")
              employee.append(email)
              c.execute("INSERT INTO Karlstaff(theatre, name,title,email) VALUES(%s, %s, %s, %s)", (employee[0], employee[1], employee[2], employee[3]))
              print employee
          else: 
              title_split = staffName_staffTitle.find(" - ")
              name = staffName_staffTitle
              name = staffName_staffTitle[:title_split]
              title = staffName_staffTitle[(title_split+3):]
              email = values[3]
              employee.append(theatre)
              employee.append(name)
              employee.append(title)
              employee.append(email)
              c.execute("INSERT INTO Karlstaff(theatre, name,title,email) VALUES(%s, %s, %s, %s)", (employee[0], employee[1], employee[2], employee[3]))
              print employee
      
 
  c.close()

  conn.commit()


if __name__ == '__main__':
  main()

