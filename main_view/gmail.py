# -*- coding:utf-8 -*-
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools
import os

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

import config

class GMail():

    def __init__(self):

        credential_dir = "credential"

        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        credential_path = os.path.join(credential_dir, "mail.json")
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(config.GO_CLIENT_SECRET_FILE, config.MA_SCOPES)
            flow.user_agent = config.GO_APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)

        self.credentials = credentials

    def get_mail(self, count):

        credentials = self.credentials

        http = credentials.authorize(httplib2.Http())
        service = discovery.build("gmail", "v1", http=http)

        list_results = service.users().messages().list(userId="me", labelIds=config.MA_LABEL_ID).execute()
        message_list = list_results.get("messages", [])

        results = []
        if not message_list:
            raise Exception("No Messages")
        else:
            for i in range(count):
                mid = message_list[i]["id"]
                results.append(service.users().messages().get(userId="me", id = mid, format="metadata").execute())

        return results

def main():
    gmail = GMail()
    new = gmail.get_mail(1)
    print(type(new))
    for head in new:
        print(head) 
    
if __name__ == "__main__":
    main()
                  
    
        
    
