# -*- coding:utf-8 -*-
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools
import os
from pytz import timezone
import datetime
import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
import config
class Schedule():

    def __init__(self):

        credential_dir = "credential"

        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        credential_path = os.path.join(credential_dir, "calendar.json")
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(config.GO_CLIENT_SECRET_FILE, config.SC_SCOPES)
            flow.user_agent = config.GO_APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)

        self.credentials = credentials


    #翌日からの予定の取得
    def get_after_events(self):

        credentials = self.credentials

        http = credentials.authorize(httplib2.Http())
        service = discovery.build("calendar", "v3", http=http)

        tomorrow = (datetime.datetime.now(timezone("Asia/Tokyo")).replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)).isoformat()
        
        events_results = service.events().list(
            calendarId=config.SC_CALENDAR_ID,
            timeMin=tomorrow,
            maxResults=9,
            singleEvents=True,
            orderBy="startTime").execute()
        
        events = events_results.get("items", [])
            
        return events


    def get_today_events(self):

        credentials = self.credentials

        http = credentials.authorize(httplib2.Http())
        service = discovery.build("calendar", "v3", http=http)

        start = datetime.datetime.now(timezone("Asia/Tokyo")).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        end = datetime.datetime.now(timezone("Asia/Tokyo")).replace(hour=23, minute=59, second=59, microsecond=0).isoformat()
        
        events_results = service.events().list(
            calendarId = config.SC_CALENDAR_ID,
            timeMin = start,
            timeMax = end,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime").execute()
        
        events = events_results.get("items", [])            

        return events

def main():
    calendar = Schedule()
    c = calendar.get_after_events()
    print(c)
    
if __name__ == "__main__":
    main()
                  
    
        
    
