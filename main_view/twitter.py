# -*- coding:utf-8 -*-
from requests_oauthlib import OAuth1Session
import json
import config
import datetime
#endpoint
mentions_timeline = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"
update = "https://api.twitter.com/1.1/statuses/update.json"

class Twitter():

    def __init__(self):
        self.session = OAuth1Session(
            config.TW_CONSUMER_KEY,
            config.TW_CONSUMER_SECRET,
            config.TW_ACCESS_TOKEN,
            config.TW_ACCESS_TOKEN_SECRET)
        
    def get_newest_mention(self, with_time=False):

        #requests
        params = {}
        req = self.session.get(mentions_timeline, params = params)

        #parse json
        mentions = json.loads(req.text)

        if with_time:
            owner_mentions = [(m["text"], datetime.datetime.strptime(m["created_at"], "%a %b %d %H:%M:%S %z %Y")) for m in mentions if m["user"]["screen_name"] == config.TW_OWNER_ACCOUNT_ID]
        else:
            owner_mentions = [m["text"] for m in mentions if m["user"]["screen_name"] == config.TW_OWNER_ACCOUNT_ID]
        if not owner_mentions:
            return None
        
        return owner_mentions[0]

        
    def get_mentions(self):

        #requests
        params = {}
        req = self.session.get(mentions_timeline, params = params)

        #parse json
        mentions = json.loads(req.text)
        owner_mentions = [m["text"] for m in mentions if m["user"]["screen_name"] == config.TW_OWNER_ACCOUNT_ID]

        if not owner_mentions:
            return None
        
        return owner_mentions[0]

    def post_tweet(self, tweet):

        params = {"status": tweet}
        req = self.session.post(update, params = params)

def main():
    
    twiapi = Twitter()
    print(twiapi.get_newest_mention(with_time=True))
    #twiapi.post_tweet("@{} てすとやで。".format(config.TW_OWNER_ACCOUNT_ID))

if __name__ == "__main__":
    main()
