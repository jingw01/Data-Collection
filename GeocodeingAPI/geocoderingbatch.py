#import libraries

import json
import requests
import csv
import pandas as pd
import os

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
		geo={}
		x='nan'
		y='nan'
	geo['X']=x
	geo['Y']=y
	geo.update(address)
	return geo
#function to extract geographic info for a list of addresses
def addressbatch(filename,folderOut):
    cols=['street','city','state','zip','X','Y','BLKGRP','STATE','FUNCSTAT','AREAWATER','NAME','SUFFIX','LSADC','CENTLON','HU100','BLOCK','BASENAME','INTPTLAT','POP100','MTFCC','COUNTY','GEOID','CENTLAT','INTPTLON','AREALAND','OBJECTID','TRACT']
    df=pd.DataFrame(columns=cols)
    df=pd.DataFrame()
    with open(filename, 'rb') as csvfile:
    #with open('address.csv', 'rb') as csvfile:
        addresses=csv.reader(csvfile,delimiter=',')
        header=addresses.next()
        for row in addresses:
            address=dict(zip(header,row))
            #location data - x y coordinates
            result=geocoderesult(address)
            tmp=pd.DataFrame(result,index=[0])
            df=df.append(tmp,ignore_index=True)

    csvfile.close()
        
    #df.to_csv('georesult.csv')
    df.to_csv("{}/georesult.csv".format(folderOut))


addresslist = raw_input('Where is csv file?')
dirout = raw_input('Where should results be output?')
addressbatch(addresslist,dirout)

