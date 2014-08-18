
#create class
class Suits:
	def __init__(self,title,dismiss,settlement,certification):
	 self.title=title
	 self.dismiss = dismiss 
	 self.settlement = settlement
	 self.certification=certification
  
Suits_List = []

#check if the description has the keywords.
import requests, urllib, urllib2, cookielib, csv, re, getpass
from operator import attrgetter
import urllib2
from bs4 import BeautifulSoup
import re


#extract all links

url_link = 'http://securities.stanford.edu/fmi/xsl/SCACPUDB/recordlist.xsl?-db=SCACPUDB&-lay=Search&FIC_DateFiled_Year=2005&-sortfield.1=FIC_DateFiled&-sortfield.2=LitigationName&-sortorder.1=ascend&-max=10&-find'

Links_Text=urllib2.urlopen(url_link)
Links_Soup=BeautifulSoup(Links_Text)


urls=[]
	
for link in Links_Soup.find_all('a'):
	tmp=link.get('href')
	urls.append(tmp)

url_list=[]

for x in range(len(urls)):
 if str(urls[x]).find("/1")==0:
	tmp='http://securities.stanford.edu'+str(urls[x])
	url_list.append(tmp)



for counter, url1 in enumerate(url_list):
	Text=urllib2.urlopen(url1).read()
	Soup=BeautifulSoup(Text)
	string=Soup.get_text()
	text=string.encode('ascii', 'ignore')
	str_text=str(text)
	Title=[]
	name=Soup.title.string
	Title.append(name)
	Dismiss=[]
	match=re.search(r'dimiss',str_text)
	if match:
	 Dismiss.append(1)
	match2=re.search(r'settlement',str_text)
	Settlement=[]
	if match2:
	 Settlement.append(1)
	match3=re.search(r'certif',str_text)
	Certification=[]
	if match3:
	 Certification.append(1)
	Suits_List.append(Suits(Title,Dismiss,Settlement,Certification))
	del Title,Dismiss,Settlement,Certification

MaxTitle = 1
MaxDismiss = 1
MaxSettlement = 1
MaxCertification = 1

for i in range(len(url_list)):
	MaxTitle = max(MaxTitle,len(Suits_List[i].title))



#EXPORT TO CSV

#CREATE TITLES

Titles = ["Title","Dismiss","Settlement","Certification"]

for i in range(MaxTitle):
	TmpTitle = "Title_" + str(i+1)
	Titles.append(TmpTitle)
for i in range(MaxDismiss):
	TmpTitle = "Dismiss_" + str(i+1)
	Titles.append(TmpTitle)
for i in range(MaxSettlement):
	TmpTitle = "Settlement_" + str(i+1)
	Titles.append(TmpTitle)
for i in range(MaxCertification):
	TmpTitle = "Certification_" + str(i+1)
	Titles.append(TmpTitle)


#EXPORT

with open('WebPull.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows([Titles])

	for i in range(len(url_list)):
		Data1 = [Suits_List[i].title,Suits_List[i].dismiss,Suits_List[i].settlement,Suits_List[i].certification]
		Data1.append(Suits_List[i].title)
		Data1.append(Suits_List[i].dismiss)
		Data1.append(Suits_List[i].settlement)
		Data1.append(Suits_List[i].certification)

		writer.writerows([Data1])