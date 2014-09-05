#import libraries

import json
import requests
import csv
import os

class Address:
	def __init__(self,street,city,state,zip,X,Y,BLKGRP,STATE,FUNCSTAT,AREAWATER,NAME,SUFFIX,LSADC,CENTLON,HU100,BLOCK,BASENAME,INTPTLAT,POP100,MTFCC,COUNTY,GEOID,CENTLAT,INTPTLON,AREALAND,OBJECTID,TRACT):
		self.street=street
		self.city=city
		self.state=state
		self.zip=zip
		self.X=X
		self.Y=Y
		self.BLKGRP=BLKGRP
		self.STATE=STATE
		self.FUNCSTAT=FUNCSTAT
		self.AREAWATER=AREAWATER
		self.NAME=NAME
		self.SUFFIX=SUFFIX
		self.LSADC=LSADC
		self.CENTLON=CENTLON
		self.HU100=HU100
		self.BLOCK=BLOCK
		self.BASENAME=BASENAME
		self.INTPTLAT=INTPTLAT
		self.POP100=POP100
		self.MTFCC=MTFCC
		self.COUNTY=COUNTY
		self.GEOID=GEOID
		self.CENTLAT=CENTLAT
		self.INTPTLON=INTPTLON
		self.AREALAND=AREALAND
		self.OBJECTID=OBJECTID
		self.TRACT=TRACT


#function to extract geographic info for an address
def geocoderesult(address,benchmark='Public_AR_Census2010',vintage='Census2010_Census2010',layers='14'):
	url1='http://geocoding.geo.census.gov/geocoder/geographies/address'
	param1={'street':address['street'],'city':address['city'],'state':address['state'],'benchmark':benchmark,'vintage':vintage,'layers':layers,'format':'json'}
	data=requests.get(url1,params=param1).text
	data=json.loads(data)
	try:
		geo=dict(data['result']['addressMatches'][0]['geographies']['Census Blocks'][0])
		x=data['result']['addressMatches'][0]['coordinates']['x']
		y=data['result']['addressMatches'][0]['coordinates']['y']
	except:
		zero=[0]*21
		geot=['BLKGRP','STATE','FUNCSTAT','AREAWATER','NAME','SUFFIX','LSADC','CENTLON','HU100','BLOCK','BASENAME','INTPTLAT','POP100','MTFCC','COUNTY','GEOID','CENTLAT','INTPTLON','AREALAND','OBJECTID','TRACT']
		geo=dict(zip(geot,zeros))
		x=0
		y=0
	geo['X']=x
	geo['Y']=y
	geo.update(address)
	street=geo['street']
	city=geo['city']
	state=geo['state']
	zip=geo['zip']
	X=geo['X']
	Y=geo['Y']
	BLKGRP=geo['BLKGRP']
	STATE=geo['STATE']
	FUNCSTAT=geo['FUNCSTAT']
	AREAWATER=geo['AREAWATER']
	NAME=geo['NAME']
	SUFFIX=geo['SUFFIX']
	LSADC=geo['LSADC']
	CENTLON=geo['CENTLON']
	HU100=geo['HU100']
	BLOCK=geo['BLOCK']
	BASENAME=geo['BASENAME']
	INTPTLAT=geo['INTPTLAT']
	POP100=geo['POP100']
	MTFCC=geo['MTFCC']
	COUNTY=geo['COUNTY']
	GEOID=geo['GEOID']
	CENTLAT=geo['CENTLAT']
	INTPTLON=geo['INTPTLON']
	AREALAND=geo['AREALAND']
	OBJECTID=geo['OBJECTID']
	TRACT=geo['TRACT']
    
	list.append(Address(street,city,state,zip,X,Y,BLKGRP,STATE,FUNCSTAT,AREAWATER,NAME,SUFFIX,LSADC,CENTLON,HU100,BLOCK,BASENAME,INTPTLAT,POP100,MTFCC,COUNTY,GEOID,CENTLAT,INTPTLON,AREALAND,OBJECTID,TRACT))
	del street,city,state,zip,X,Y,BLKGRP,STATE,FUNCSTAT,AREAWATER,NAME,SUFFIX,LSADC,CENTLON,HU100,BLOCK,BASENAME,INTPTLAT,POP100,MTFCC,COUNTY,GEOID,CENTLAT,INTPTLON,AREALAND,OBJECTID,TRACT
	
	#function to extract geographic info for a list of addresses
def addressbatch(filename,folderOut):
    with open(filename, 'rb') as csvfile:
    #with open('address.csv', 'rb') as csvfile:
        addresses=csv.reader(csvfile,delimiter=',',dialect=csv.excel_tab)
        header=addresses.next()
        for row in addresses:
            address=dict(zip(header,row))
            #location data - x y coordinates
            geocoderesult(address) 
	csvfile.close()
	

addresslist = raw_input('Where is csv file?')
dirout = raw_input('Where should results be output?')
list=[]  
print 'Reading the file'
addressbatch(addresslist,dirout)

#EXPORT
print 'Start to Export'
Titles=['street','city','state','zip','X','Y','BLKGRP','STATE','FUNCSTAT','AREAWATER','NAME','SUFFIX','LSADC','CENTLON','HU100','BLOCK','BASENAME','INTPTLAT','POP100','MTFCC','COUNTY','GEOID','CENTLAT','INTPTLON','AREALAND','OBJECTID','TRACT']
with open('WebPull.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows([Titles])

	for i in range(len(list)):
		Data1 = [list[i].street,list[i].city,list[i].state,list[i].zip,list[i].X,list[i].Y,list[i].BLKGRP,list[i].STATE,list[i].FUNCSTAT,list[i].AREAWATER,\
		list[i].NAME,list[i].SUFFIX,list[i].LSADC,list[i].CENTLON,list[i].HU100,list[i].BLOCK,list[i].BASENAME,list[i].INTPTLAT,list[i].POP100,list[i].MTFCC,\
		list[i].COUNTY,list[i].GEOID,list[i].CENTLAT,list[i].INTPTLON,list[i].AREALAND,list[i].OBJECTID,list[i].TRACT]

		writer.writerows([Data1])

