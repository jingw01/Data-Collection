from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from BeautifulSoup import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from pattern import web
from time import sleep

#to scrape every case of the list of cases of advanced search page
def scrape_perlist(driver,sleepInt=4,endcase=31,mainpage=0):
	listcase=[]

	for r in range(1,endcase):
		'''
		try:
	
		except ElementNotVisibleException:
			pass
		'''
		row=driver.find_element_by_xpath("//*[@id='dTable_searchResults']/tbody/tr["+str(r)+"]/td[1]/a")
		row.click()

		sleep(sleepInt)

		case=scrape_page(browser)
		listcase.append(case)
		
	        back=driver.find_element_by_xpath("//*[@id='backButtons']/span")
		back.click()
		sleep(sleepInt)
		
		if mainpage!=0:
			nextpage=browser.find_element_by_xpath(mainpage)
			nextpage.click()
			sleep(sleepInt)
		
	
	return listcase

#scrape data from the page of each case
def scrape_page(driver):
	html=driver.page_source
	soup=BeautifulSoup(html)
	soup2=soup.findAll(id="content")
	title=soup2[0].find('h1').string
	sec=1 if '(SEC)' in title else 0
	varnames=soup2[0].findAll('dt')
	link=" "
	for n in range(len(varnames)):
		if 'Case Status' in varnames[n].string:
			status=varnames[n].findNext('dd').text
		if 'Class Period' in varnames[n].string:
			period=varnames[n].findNext('dd').text
		if 'Settlement Fund' in varnames[n].string:
			settlement=varnames[n].findNext('dd').text
		if 'Class Definition' in varnames[n].string:
			definition=varnames[n].findNext('dd').text
		if 'Security ID' in varnames[n].string:
			securityid=varnames[n].findNext('dd').text
		if 'Final Settlement Date' in varnames[n].string:
			finaldate=varnames[n].findNext('dd').text
		if 'Court' in varnames[n].string:
			if 'Appellate' not in varnames[n].string:
				court=varnames[n].findNext('dd').text
		if 'Institutional' in varnames[n].string:
			institutional=varnames[n].findNext('dd').string
			leadInst=1 if len(institutional)>4 else 0
		if 'Settling Defendants' in varnames[n].string:
			settlingdef=varnames[n].findNext('dd').text
		if 'Case Summary' in varnames[n].string:
			summary=varnames[n].findNext('dd').text
		if 'Complaint Document(s)' in varnames[n].string:
			link="https://link.issgovernance.com/scas/"+str(varnames[n].findNext('dd').findAll('a')[-1]['href'])
		
	result=casesprofile(title,status,period,settlement,definition,securityid,finaldate,court,institutional,settlingdef,sec,leadInst,summary,link)

	return result


#Create Class
class casesprofile:
	def __init__(self,title,status,period,settlement,definition,securityid,finaldate,court,institutional,settlingdef,sec,leadInst,summary,link):
		self.title=title
		self.status=status
		self.period=period
		self.settlement=settlement
		self.definition=definition
		self.securityid=securityid
		self.finaldate=finaldate		
		self.court=court
		self.institutional=institutional
		self.settlingdef=settlingdef
		self.sec=sec
		self.leadInst=leadInst
		self.summary=summary
		self.link=link


browser = webdriver.Firefox()

browser.get('https://link.issgovernance.com/')

elem = browser.find_element_by_name('userName')  # Find the search box
elem.send_keys('charles')

elem2= browser.find_element_by_name('password')  # Find the search box
elem2.send_keys('river')
option=browser.find_element_by_id('login')
option.click()
browser.implicitly_wait(60) # seconds

def advanceSearchSettlement(dateStart='01/01/2013',dateEnd='12/13/2013'):
	browser.get('https://link.issgovernance.com/scas/index.php?c=index&tabName=advancedSearch')
	browser.implicitly_wait(60) # seconds
	
	start=browser.find_element_by_id('settlementDateStart')
	start.send_keys(dateStart)
	end=browser.find_element_by_id('settlementDateEnd')
	end.send_keys(dateEnd)
	submit=browser.find_element_by_id('btnSearch')
	submit.click()

	sleep(5)
	#find the number of cases

	page=browser.page_source
	souppage=BeautifulSoup(page)
	pageinfo=souppage.find('div',id='dTable_searchResults_info').contents[0].string
	listlength=int(pageinfo.split()[5])
	residualno=listlength%30
	totalpage=(listlength-residualno)/30+1
	
	return listlength,residualno,totalpage

listlen,residual,pageno=advanceSearchSettlement()
print "There are "+str(listlen)+" number of cases, and a total of "+str(pageno)+" pages with "+str(residual)+" cases per page."

#scraping first page
cases=scrape_perlist(browser)

#scraping 2 to 2nd last page

for n in range(2,pageno):
	path="//*[@id='dTable_searchResults_paginate']/span/a["+str(n)+"]"
	nextpage=browser.find_element_by_xpath(path)
	nextpage.click()
	print "Currently on Page "+str(n)
	newcases=scrape_perlist(browser,mainpage=path)
	cases.append(newcases)
	

#scraping last page
path="//*[@id='dTable_searchResults_paginate']/span/a["+str(pageno)+"]"
nextpage=browser.find_element_by_xpath(path)
nextpage.click()
print "Currently on Last Page."
newcases=scrape_perlist(browser,endcase=residual,mainpage=path)
cases.append(newcases)


Titles=['Title','Status','Class Period','Settlement Fund','Case Definition','Security Id','FinalSettlementdate','Court','Lead Institutional','Settling Defendants','SEC Case','leadInst','Case Summary','Latest Complaint-Link']


with open('Output2.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows([Titles])

	#for i in range(listlen):
	for i in range(5):
		Data1 = [cases[i].title,cases[i].status,cases[i].period,cases[i].settlement,cases[i].definition,cases[i].securityid,cases[i].finaldate,cases[i].court,cases[i].institutional,cases[i].settlingdef,cases[i].sec,cases[i].leadInst,cases[i].summary,cases[i].link]
		writer.writerows([Data1])

