import time
import secrets
import lxml.html
from selenium import webdriver

print(secrets.phantom_location)


def NBA_Lookup():
	suffix=time.strftime("%Y%m%d")
	url= 'http://www.espn.com/nba/scoreboard/_/date/' + suffix
	# url = 'http://www.espn.com/nba/scoreboard/_/date/20170327'
	print("Running for date {}...".format(suffix))
	driver = webdriver.PhantomJS(secrets.phantom_location)
	driver.set_window_size(0,0)
	driver.get(url)

	# tree = lxml.html.fromstring(driver.page_source)
	score_date = driver.find_element_by_xpath('//*[(@id = "sbpDate")]').text
	Teams = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "sb-team-short", " " ))]')
	Scores = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "total", " " ))]//span')
	Time_left = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "date-time", " " ))]')
	# print(Teams)
	a=[]
	b=[]
	c=[]

	def xpathToStr(xpathElements, part):
		for i in range(len(xpathElements)):
			temp=xpathElements[i].text
			part.append(temp)

	xpathToStr(Teams, a)
	xpathToStr(Scores, b)
	xpathToStr(Time_left, c)
	box_score=[]
	box_score.append(score_date)
	# if empty score/game hasn't been played
	if not b:
		for i in range(len(a)//2):	
			i*=2
			temp=a[i] + '   ' + '     ' + a[i+1] + '   ' +  '    ' + c[(i)//2]
			box_score.append(temp)
	elif len(b)<len(a):
		for i in range(len(a)-len(b)):
			b.append('')
		for i in range(len(a)//2):
			i*=2
			# for bolding
			if b[i]!='' and b[i+1]!='':		
				if int(b[i])>int(b[i+1]):	
					temp='**'+a[i] + '   ' +b[i]+'**'+ '     ' + a[i+1] + '   ' + b[i+1] + '    ' + c[(i)//2]
					box_score.append(temp)
				else:
					temp=a[i] + '   ' + b[i] + '     ' + '**'+a[i+1] + '   ' + b[i+1]+'**' + '    ' + c[(i)//2]
					box_score.append(temp)	
			else:
				temp=a[i] + '   ' + b[i] + '     ' + '**'+a[i+1] + '   ' + b[i+1]+'**' + '    ' + c[(i)//2]
				box_score.append(temp)	

	else:
		# print("baby loves you")
		for i in range(len(a)//2):
			i*=2
			if b[i]!='' and b[i+1]!='':	
				if int(b[i])>int(b[i+1]):	
					# print("first score: {}, second score: {}. first is bigger, bolding".format(b[i], b[i+1]))
					temp='**'+a[i] + '   ' + b[i]+'**' + '     ' + a[i+1] + '   ' + b[i+1] + '    ' + c[(i)//2]
					box_score.append(temp)
				else:
					# print("first score: {}, second score: {}. second is bigger, bolding".format(b[i], b[i+1]))
					temp=a[i] + '   ' + b[i] + '     ' + '**'+a[i+1] + '   ' +b[i+1]+'**' + '    ' + c[(i)//2]
					box_score.append(temp)
					print(box_score)
			else:
				# print("first score: {}, second score: {}. second is bigger, bolding".format(b[i], b[i+1]))
				temp=a[i] + '   ' + b[i] + '     ' + '**'+a[i+1] + '   ' +b[i+1]+'**' + '    ' + c[(i)//2]
				box_score.append(temp)
				print(box_score)

	NBA_Scores=''
	for i in range(len(box_score)):
	    NBA_Scores=NBA_Scores + box_score[i] + '\n'
	driver.quit()

	print('Finished running NBA scores')
	return NBA_Scores

# NBA_Lookup()

