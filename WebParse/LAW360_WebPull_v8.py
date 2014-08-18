#IMPORT LIBRARIES

import requests, urllib, urllib2, cookielib, csv, re, getpass
from operator import attrgetter
from BeautifulSoup import BeautifulSoup

#CREATE CLASS

class LawSuits:
    def __init__(self, date, title, casenum, court, nature, cause, judge, firms,
                 companies, sectors, defendants,defendant_reps,plaintiffs, plaintiff_reps):
        self.date = date
        self.title = title
        self.casenum = casenum
        self.court = court
        self.nature = nature
        self.cause = cause
        self.judge = judge
        self.firms = firms
        self.companies = companies
        self.sectors = sectors
        self.defendants = defendants
        self.defendant_reps = defendant_reps
        self.plaintiffs = plaintiffs
        self.plaintiff_reps = plaintiff_reps

LawSuits_List = []


#GET INPUT

login = raw_input('Enter email: ')
pswrd = getpass.getpass()
Url_Links = raw_input('Enter page 1 url: ')
Num_Cases = raw_input('How many cases would you like to extract?')

#LOG IN

cj = cookielib.CookieJar()
browser = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def open1(url, postdata=None):
    if postdata is not None:
        postdata = urllib.urlencode(postdata)
    return browser.open(url, postdata).read()

payload = {'email': login, 'password': pswrd, 'keep_signed_in': '1', 'submit': 'Submit', 'authenticity_token': 'yHijyvydIoW4JzNbxdgog3udi9abMP1jdj5mJh8xxQU='}
url0 = 'http://www.law360.com/account/login?return_url=%2F'
open1(url0,payload)

#EXTRACT ALL LINKS

Links_Text = open1(Url_Links)
Links_Soup = BeautifulSoup(Links_Text)

try:
    NumPages0 = Links_Soup.find("a", {"class": "next_page"})
    NumPages = int(NumPages0.findPrevious('a').text)
except:
    NumPages = 1

urls = []

for x in range(NumPages):
    if len(urls) < int(Num_Cases):
        TmpUrl = Url_Links + '&page=' + str(x+1) + '&per_page=200'
        Links_Text2 = open1(TmpUrl)
        Links_Soup2 = BeautifulSoup(Links_Text2)

        for a in Links_Soup2.findAll('a',href=re.compile('^/cases/')):
            if len(urls) < int(Num_Cases):
                TmpLink = 'http://www.law360.com' + str(a['href'])
                urls.append(TmpLink)
            else:
                break
    else:
        break
    
#READ PAGES OF INTEREST

for counter, url1 in enumerate(urls):

    UrlText = open1(url1)

    #PARSE

    soup = BeautifulSoup(UrlText)

        #EXTRACT DETAILS

    details = soup.find("div", {"id": "details"})
    details_h3 = details.findAll('h3')

    for i in range(len(details_h3)):
        if 'Firms' in details_h3[i].string:
            tmpFind = details_h3[i].findNext('ul')
            Firms = []
            tmpFind2 = tmpFind.findAll('li')
            for j in range(len(tmpFind2)):
                Firms.append(tmpFind2[j].text.replace("&amp;","&"))
        if 'Companies' in details_h3[i].string:
            tmpFind = details_h3[i].findNext('ul')
            Companies = []
            tmpFind2 = tmpFind.findAll('li')
            for j in range(len(tmpFind2)):
                Companies.append(tmpFind2[j].text.replace("&amp;","&"))
        if 'Sectors' in details_h3[i].string:
            tmpFind = details_h3[i].findNext('ul')
            Sectors = []
            tmpFind2 = tmpFind.findAll('a')
            for j in range(len(tmpFind2)):
                Sectors.append(tmpFind2[j].text.replace("&amp;","&"))
        if 'Case' in details_h3[i].string:
            CaseNum = details_h3[i].findNext('p').text
        if 'Court' in details_h3[i].string:
            Court = details_h3[i].findNext('p').text
        if 'Nature' in details_h3[i].string:
            Nature = details_h3[i].findNext('p').text
        if 'Judge' in details_h3[i].string:
            Judge = details_h3[i].findNext('p').text

    try:
        Cause = details.find("p",{"class":"notes"}).text[5:]
    except:
        Cause = 'No Data'

        #EXTRACT TITLE & DATE

    Title = soup.title.text
    Date = soup.find("p",{"class":"dtstamp"}).text

        #EXTRACT DEFENDANT INFORMATION

    Defend_Info = soup.findAll("h3",text="Defendant")
    Defendant = []
    Defendant_Rep = []

    for k in range(len(Defend_Info)):
        Defendant.append(Defend_Info[k].findNext('p').text)
        TmpFind = Defend_Info[k].findNext('div')
        try:
            TmpFind2 = TmpFind.findAll('p')
            for l in range(len(TmpFind2)):
                if l == 0:
                    TmpRep = TmpFind2[l].text.replace("&amp;","&")
                else:
                    TmpRep =  TmpRep + ' and ' + TmpFind2[l].text.replace("&amp;","&")
            Defendant_Rep.append(TmpRep)
        except:
            Defendant_Rep.append('None')

        #EXTRACT PLANTIFF INFORMATION

    Plaintiff_Info = soup.findAll("h3",text="Plaintiff")
    Plaintiff = []
    Plaintiff_Rep = []

    for k in range(len(Plaintiff_Info)):
        Plaintiff.append(Plaintiff_Info[k].findNext('p').text)
        TmpFind = Plaintiff_Info[k].findNext('div')
        try:
            TmpFind2 = TmpFind.findAll('p')
            for l in range(len(TmpFind2)):
                if l == 0:
                    TmpRep = TmpFind2[l].text.replace("&amp;","&")
                else:
                    TmpRep =  TmpRep + ' and ' + TmpFind2[l].text.replace("&amp;","&")
            Plaintiff_Rep.append(TmpRep)
        except:
            Plaintiff_Rep.append('None')

    #OUTPUT TO CLASS

    if 'Firms' not in locals():
        Firms = ['No Data']
    if 'Companies' not in locals():
        Companies = ['No Data']
    if 'Sectors' not in locals():
        Sectors = ['No Data']
    if 'Judge' not in locals():
        Judge = 'No Data'


    LawSuits_List.append(LawSuits(Date,Title,CaseNum,Court,Nature,Cause,Judge,Firms,Companies,Sectors,
                                    Defendant,Defendant_Rep,Plaintiff,Plaintiff_Rep))

    #CLEAR VARIABLES
    
    del Date,Title,CaseNum,Court,Nature,Cause,Judge,Firms,Companies,Sectors,Defendant,Defendant_Rep,Plaintiff,Plaintiff_Rep

MaxFirms = 1
MaxCompanies = 1
MaxSectors = 1
MaxDefendants = 1
MaxDefendants_R = 1
MaxPlaintiffs = 1
MaxPlaintiffs_R = 1

for i in range(len(urls)):
    MaxFirms = max(MaxFirms,len(LawSuits_List[i].firms))
    MaxCompanies = max(MaxCompanies,len(LawSuits_List[i].companies))
    MaxSectors = max(MaxSectors,len(LawSuits_List[i].sectors))
    MaxDefendants = max(MaxDefendants,len(LawSuits_List[i].defendants))
    MaxDefendants_R = max(MaxDefendants_R,len(LawSuits_List[i].defendant_reps))
    MaxPlaintiffs = max(MaxPlaintiffs,len(LawSuits_List[i].plaintiffs))
    MaxPlaintiffs_R = max(MaxPlaintiffs_R,len(LawSuits_List[i].plaintiff_reps))

#EXPORT TO CSV

    #CREATE TITLES

Titles = ["Date","Title","Case Number","Court","Nature of Suit","Cause","Judge"]

for i in range(MaxFirms):
    TmpTitle = "Firm_" + str(i+1)
    Titles.append(TmpTitle)
for i in range(MaxCompanies):
    TmpTitle = "Company_" + str(i+1)
    Titles.append(TmpTitle)
for i in range(MaxSectors):
    TmpTitle = "Sector_" + str(i+1)
    Titles.append(TmpTitle)
for i in range(MaxDefendants):
    TmpTitle = "Defendant_" + str(i+1)
    Titles.append(TmpTitle)
for i in range(MaxDefendants_R):
    TmpTitle = "Representation for Defendant_" + str(i+1)
    Titles.append(TmpTitle)
for i in range(MaxPlaintiffs):
    TmpTitle = "Plaintiff_" + str(i+1)
    Titles.append(TmpTitle)
for i in range(MaxPlaintiffs_R):
    TmpTitle = "Representation for Plaintiff_" + str(i+1)
    Titles.append(TmpTitle)

    #PAD LISTS

def padlists(the_list,maxnum):
    if len(the_list) < maxnum:
        the_list += ['No Data'] * (maxnum - len(the_list))

for i in range(len(urls)):
    padlists(LawSuits_List[i].firms,MaxFirms)
    padlists(LawSuits_List[i].companies,MaxCompanies)
    padlists(LawSuits_List[i].sectors,MaxSectors)
    padlists(LawSuits_List[i].defendants,MaxDefendants)
    padlists(LawSuits_List[i].defendant_reps,MaxDefendants_R)
    padlists(LawSuits_List[i].plaintiffs,MaxPlaintiffs)
    padlists(LawSuits_List[i].plaintiff_reps,MaxPlaintiffs_R)

    #EXPORT

with open('WebPull.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows([Titles])

    for i in range(len(urls)):
        Data1 = [LawSuits_List[i].date,LawSuits_List[i].title,LawSuits_List[i].casenum,LawSuits_List[i].court,
                 LawSuits_List[i].nature,LawSuits_List[i].cause,LawSuits_List[i].judge]

        for j in range(MaxFirms):
            Data1.append(LawSuits_List[i].firms[j])
        for j in range(MaxCompanies):
            Data1.append(LawSuits_List[i].companies[j])
        for j in range(MaxSectors):
            Data1.append(LawSuits_List[i].sectors[j])
        for j in range(MaxDefendants):
            Data1.append(LawSuits_List[i].defendants[j])
        for j in range(MaxDefendants_R):
            Data1.append(LawSuits_List[i].defendant_reps[j])
        for j in range(MaxPlaintiffs):
            Data1.append(LawSuits_List[i].plaintiffs[j])
        for j in range(MaxPlaintiffs_R):
            Data1.append(LawSuits_List[i].plaintiff_reps[j])

        writer.writerows([Data1])





        

