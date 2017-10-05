import threading
from twitter import Twitter
import time
import config

class TwitterChecker(threading.Thread):

    def __init__(self, event_manager):
        super(TwitterChecker, self).__init__()
        self.api = Twitter()
        self.running = True
        self.event_manager = event_manager


    def run(self):

        latest_get_time = None
        import event
        while self.running:
            
            text, post_time = self.api.get_newest_mention(with_time=True)
            if latest_get_time == None:
                latest_get_time = post_time
                
            if post_time > latest_get_time:
                command, value =  event.parse_from_string(text)
                self.event_manager.enqueue_event(command, value)
                self.api.post_tweet("@{} 了解やで。".format(config.TW_OWNER_ACCOUNT_ID))
                latest_get_time = post_time
                
            time.sleep(60)
            

    def stop(self):
        self.running = False
    
