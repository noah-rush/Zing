from xlrd import open_workbook
wb = open_workbook('zingTheaterMarketingDirectory.xlsx')

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
 				print employee
 	
 		
 		

 		
# for s in wb.sheets():
#  	print 'Sheet:',s.name
#  	for row in range(s.nrows):
#  		values = []
#  		for col in range(s.ncols):
#  			values.append(s.cell_value(row,col))
#  		print values
