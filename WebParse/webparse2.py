
#create class
class Suits:
	def __init__(self,title,dismiss,settlement,certification,appeal,grant):
	 self.title=title
	 self.dismiss = dismiss 
	 self.settlement = settlement
	 self.certification=certification
	 self.appeal=appeal
	 self.grant=grant
  
Suits_List = []

#check if the description has the keywords.
import requests, urllib, urllib2, cookielib, csv, re, getpass
from operator import attrgetter
import urllib2
from bs4 import BeautifulSoup
import re


#extract all links

#url_link = 'http://securities.stanford.edu/fmi/xsl/SCACPUDB/recordlist.xsl?-db=SCACPUDB&-lay=Search&FIC_DateFiled_Year=2007&-sortfield.1=FIC_DateFiled&-sortfield.2=LitigationName&-sortorder.1=ascend&-max=177&-find'
#url_link='http://securities.stanford.edu/fmi/xsl/SCACPUDB/recordlist.xsl?-db=SCACPUDB&-lay=Search&FIC_DateFiled_Year=2006&-sortfield.1=FIC_DateFiled&-sortfield.2=LitigationName&-sortorder.1=ascend&-max=120&-find'
#url_link='http://securities.stanford.edu/fmi/xsl/SCACPUDB/recordlist.xsl?-db=SCACPUDB&-lay=Search&FIC_DateFiled_Year=2005&-sortfield.1=FIC_DateFiled&-sortfield.2=LitigationName&-sortorder.1=ascend&-max=1&-find'
url_link='http://securities.stanford.edu/fmi/xsl/SCACPUDB/recordlist.xsl?-db=SCACPUDB&-lay=Search&FIC_DateFiled_Year=2008&-sortfield.1=FIC_DateFiled&-sortfield.2=LitigationName&-sortorder.1=ascend&-max=223&-find'

#file=open('2005_List.html')
#Links_Text=file.read()
Links_Text=urllib2.urlopen(url_link).read()
Links_Soup=BeautifulSoup(Links_Text)


url_list=[]

for a in Links_Soup.findAll('a',href=re.compile('/10')):
	tmplink='http://securities.stanford.edu'+str(a['href'])
	url_list.append(tmplink)



for counter, url1 in enumerate(url_list):
	Text=urllib2.urlopen(url1).read()
	Soup=BeautifulSoup(Text)
	string=Soup.get_text()
	text=string.encode('ascii', 'ignore')
	str_text=str(text)
	Title=str(Soup.title.string)
	match=re.search(r'dismiss',str_text)
	Dismiss="0"
	if match:
	 Dismiss="1"
	Settlement="0"
	match2=re.search(r'settlement',str_text)
	if match2:
	 Settlement="1"
	Certification="0"
	match3=re.search(r'certif',str_text)
	if match3:
	 Certification="1"
	Appeal="0"
	match3=re.search(r'Court of Appeals',str_text)
	if match3:
	 Appeal="1"
	Grant="0"
	match4=re.search(r'grant',str_text)
	if match4:
	 Grant="1"
	Suits_List.append(Suits(Title,Dismiss,Settlement,Certification,Appeal,Grant))
	del Title,Dismiss,Settlement,Certification,Appeal,Grant


#EXPORT TO CSV

#CREATE TITLES

Titles = ["Title","Dismiss","Settlement","Certification","Appeal","Grant"]

#EXPORT

with open('WebPull_2008.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows([Titles])

	for i in range(len(url_list)):
		Data1 = [Suits_List[i].title,Suits_List[i].dismiss,Suits_List[i].settlement,Suits_List[i].certification,Suits_List[i].appeal,Suits_List[i].grant]
		writer.writerows([Data1])