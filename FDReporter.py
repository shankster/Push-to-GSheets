import json
import time
import datetime
import csv
import gspread
import time
import pytz
import requests
import os
from jsontraverse.parser import JsonTraverseParser
from oauth2client.service_account import ServiceAccountCredentials

local_tz=pytz.timezone('Asia/Kolkata')
sleepDuration=900.0
# starttime=1535625000.0
serviceAccountKeyFile="replace_with_your_gSheets_json"
sheetName="Hourly Open Ticket Count"
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
date=''
timeStamp=''
hour=''
minute=''
seconds=''

def urlMaker(domain,agentId,status,pageNumber):
    domain=domain
    basicUrl="https://{}.freshdesk.com/api/v2".format(domain)
    operation="search"
    item="tickets"
    parameter="query"
    agentId=agentId
    status=status

    statusString=''
    statusLength=len(status)
    if statusLength==1:
        statusString='status:{}'.format(status[0])
    elif statusLength>1:
        for eachStatus in status:
            statusString=statusString+('status:{}').format(eachStatus)+' OR '
        statusString=statusString[:(len(statusString)-4)]

    queryString="group_id:{} AND ({})".format(agentId,statusString)
    page="page={}".format(pageNumber)
    requestUrl=basicUrl+'/'+operation+'/'+item+'?'+page+'&'+parameter+"="+"\""+queryString+"\""
    #print (requestUrl+'\n')
    return requestUrl

def makeRequest(url):
    url=url
    apiKey=os.environ["FRESHDESK_AGENT_API_KEY"]
    password=""
    apiRequest=requests.get(url,auth=(apiKey,password))
    apiResponse=json.dumps(apiRequest.json(),indent=4,sort_keys=True)
    return apiResponse

def totalFinder(statusCode):
    uri=urlMaker('eneter_fd_site_name',5,[statusCode],1)
    apiResponse=makeRequest(uri)
    responseParser=JsonTraverseParser(apiResponse)
    total=responseParser.traverse("total")
    return total

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def pushToSheets():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(serviceAccountKeyFile, scope)
    gc = gspread.authorize(credentials)
    worksheet = gc.open(sheetName).sheet1
    #Open Tickets
    openTotal=totalFinder(2)
    #Dev Followup Tickets
    devFollowUpTotal=totalFinder(10)
    #Migration Tickets
    migrationTotal=totalFinder(11)
    #Collect Date and Time
    dateObject=utc_to_local(datetime.datetime.now())
    date=("{}-{}-{}".format(dateObject.strftime("%d"),dateObject.strftime("%m"),dateObject.strftime("%Y")))
    hour=dateObject.strftime("%H")
    minute=dateObject.strftime("%M")
    seconds=dateObject.strftime("%S")
    timeStamp=("{}:{}:{}".format(hour,minute,seconds))
    #Write Data to gSheet
    values=[date,timeStamp,hour,minute,seconds,openTotal,devFollowUpTotal,migrationTotal]
    worksheet.append_row(values,value_input_option='RAW')

pushToSheets()
