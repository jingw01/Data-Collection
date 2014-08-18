import requests
from pattern import web
import pandas as pd
import re
import os
import logging

#import log
log_filename='Scanhtm.log'
logging.basicConfig(filename=log_filename,
                    level=logging.DEBUG)
					
def extractdata(table,start,end,entry):
    row=table[start:end]
    ext=row.index('-',1)+1
    CUSIP=row[0:ext].encode('utf8')
    CUSIPext=row[ext:ext+1].encode('utf8').strip()
    middle=row.index("\n")
    SecDesc=row[ext+2:middle].encode('utf8').strip()
    end=row.index("\n",middle+2)
    rowdata=row[middle+2:end]
    OpenPos=rowdata[0:entry[0]].encode('utf8').strip()
    SettlingTrd=rowdata[entry[0]+1:entry[1]].encode('utf8').strip()
    Div_Misc=rowdata[entry[1]+1:entry[2]].encode('utf8').strip()
    Receipts=rowdata[entry[2]+1:entry[3]].encode('utf8').strip()
    ClosePos=rowdata[entry[3]+1:entry[4]].encode('utf8').strip()
    MktPrice=rowdata[entry[4]+1:entry[5]].encode('utf8').strip()
    MktValue=rowdata[entry[5]+1:entry[7]].encode('utf8').strip()
    CurrCode=rowdata[entry[7]+1:entry[8]].encode('utf8').strip()
    result=[CUSIP,CUSIPext,SecDesc,OpenPos,SettlingTrd,Div_Misc,Receipts,ClosePos,MktPrice,MktValue,CurrCode]
    return result


#EXTRACT DATA FOR THE REPORT OF EACH SETTLEMENT DATE
def perdate(table):
    m=re.search('FOR SETTLEMENT ON: ',table)
    SettleDate=table[m.end():m.end()+10]
    m=re.search('\nPARTICIPANT: ',table)
    Participant=table[m.end():m.end()+5]
    m=re.search('\nSUB-ACCOUNT: ',table)
    sub_acct=table[m.end():m.end()+5]

#CREATE A LIST OF POSITION OF LAST CHARACTER OF EACH VARIABLE
    tstart=table.index("\nISIN")+6
    tmiddle1=table.index("\n",tstart)
    tmiddle2=table.index("\n",tmiddle1+2)
    tend=table.index("\n",tmiddle2+2)
    trow=table[tmiddle2+2:tend]
    tp=re.compile("[A-Z] ")
    entry={}
    for i,m in enumerate(tp.finditer(trow)):
        entry[i]=m.end();

#EXTRACT THE DATA OF EACH ENTRY    
    p=re.compile('\nUS')
    start=[m.end() for m in p.finditer(table)]
    end=[m.end() for m in p.finditer(table)][1:]
    end.append(len(table))
    data=[extractdata(table,start[r],end[r],entry) for r in range(len(start)) ]
    data2=[dict(SettleDate=SettleDate,
                Participant=Participant,
                Sub_Acct=sub_acct,
                CUSIP=r[0],
                CUSIPext=r[1],
                SecDesc=r[2],
                OpenPos=r[3],
                SettlingTrd=r[4],
                Div_Misc=r[5],
                Receipts=r[6],
                ClosePos=r[7],
                MktPrice=r[8],
                MktValue=r[9],
                CurrCode=r[10]) for r in data]
    return pd.DataFrame(data2),len(data)


def openfiles(root,file):
	logging.debug('Reading File: %s',file)
	filename=os.path.join(root, file)
	pl=open(filename,"r")
	htm=pl.read()
	dom = web.Element(htm)
	cols=["SettleDate","Participant","Sub_Acct","CUSIP","CUSIPext","SecDesc",
	"OpenPos","SettlingTrd","Div_Misc","Receipts","ClosePos","MktPrice","MktValue","CurrCode"]
	df=pd.DataFrame(columns=cols)
	totalrow=0
	count=0
	skipped=[]
	for i,t in enumerate(dom.by_tag('pre')):
		table=t.content
		try:
			result,rows=perdate(table)
			totalrow=totalrow+rows
			count=count+1
		except (ValueError,AttributeError) as e:
			result=pd.DataFrame()
			skipped.append(i)
		df=df.append(result,ignore_index=True)
	logging.debug("Skip Tag_Value: %s",skipped)
	logging.debug("Total number of %s Daily Reports:",count)
	logging.debug("Total number of %s Entries:",totalrow)
	outname=file.replace(".htm",".csv")
	path=os.path.join('output\\',outname)
	df.to_csv(path)
	pl.close()
	return [outname,skipped,count,totalrow]

recordt=["file","SkippedTag","NofReports","TotalRow"]
recorddf=pd.DataFrame(columns=recordt)
for root, dirs, files in os.walk("CNSReports"):
	
	logging.debug('Reading Folder: %s', root)
	for file in files:
		if file.endswith(".htm"):
			outname=file.replace(".htm",".csv")
			path=os.path.join('output\\',outname)
			if os.path.isfile(path):
				logging.debug('Already Imported File: %s', outname)
				print 'skip file: '+str(outname)
			else:
				print 'reading file: '+str(file)
				record=openfiles(root,file)
				tmpdf=pd.DataFrame(dict(zip(recordt,record)))
				recorddf=recorddf.append(tmpdf,ignore_index=True)
	
	
recorddf.to_csv("Record.csv")				

			
				


