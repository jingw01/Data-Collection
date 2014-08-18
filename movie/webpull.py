import requests, urllib, urllib2, cookielib, csv, re, getpass
from operator import attrgetter
import urllib2
from bs4 import BeautifulSoup
import re

#CREATE CLASS

class Movies:
	def __init__(self,distributor,movie,date,budget,domestic,foreign):
	 self.distributor=distributor
	 self.movie=movie
	 self.date=date
	 self.budget=budget
	 self.domestic=domestic
	 self.foreign=foreign
  
Movies_List = []


url_link='http://boxofficemojo.com/studio/?view=company&view2=yearly&yr=2000&p=.htm'
studio_Text=urllib2.urlopen(url_link).read()
studio_Soup=BeautifulSoup(studio_Text)
studio_links=studio_Soup.find("div",{"id":"body"})
studio_list=[]
for a in studio_links.findAll('a',href=re.compile('/studio/chart')):
	tmplink='http://boxofficemojo.com'+str(a['href'])
	studio_list.append(tmplink)

url_list=[]
for studio, link in enumerate(studio_list):
	if studio<11:
		Link_Text=urllib2.urlopen(link).read()
		Link_Soup=BeautifulSoup(Link_Text)
		links=Link_Soup.find("div",{"id":"body"})
		for a in links.findAll('a',href=re.compile('/movies')):
			tmplink='http://boxofficemojo.com'+str(a['href'])
			url_list.append(tmplink)
		
for counter, url1 in enumerate(url_list):
	Text=urllib2.urlopen(url1).read()
	Soup=BeautifulSoup(Text)
	details=Soup.find("div",{"id":"body"})
	details_td=details.findAll('td')
	distributor=details_td[7].text
	movie=details_td[3].findNext('b').text
	date=details_td[8].text
	budget=details_td[12].text
	domestic=details_td[19].text.replace(u'\xa0',u' ')
	foreign=details_td[22].text.replace(u'\xa0',u' ')
	Movies_List.append(Movies(distributor,movie,date,budget,domestic,foreign))
	del distributor,movie,date,budget,domestic,foreign
	
#EXPORT TO CSV

#CREATE TITLES

Titles = ["Distributor","Movie","Release Date","Budget","Domestic","Foreign"]

#EXPORT

with open('WebPull_2000.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows([Titles])

	for i in range(len(url_list)):
		Data1 = [Movies_List[i].distributor,Movies_List[i].movie,Movies_List[i].date,Movies_List[i].budget,Movies_List[i].domestic,Movies_List[i].foreign]
		writer.writerows([Data1])