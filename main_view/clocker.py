# -*- coding:utf-8 -*-
import threading
import time
import event
import config

class Clocker(threading.Thread):

    def __init__(self, event_manager, limit=config.MAIN_PROGRESS_BAR_MAX, screen=event.Value.NEXT):
        super(Clocker, self).__init__()
        self.event_manager = event_manager
        self.elapsed_time = 0
        self.running = True
        self.limit = limit
        self.screen = screen
        
    def run(self):

        self.elapsed_time = 0
        prev_step = time.time()
        
        while self.running:
            self.elapsed_time += time.time() - prev_step
            prev_step = time.time()
            if self.elapsed_time > self.limit:
                self.event_manager.enqueue_event(event.Command.TRANSITION, self.screen)
                self.elapsed_time = 0
                
    def get_current_time(self):
        return self.elapsed_time
    
    def reset(self):
        self.elapsed_time = 0
        
    def stop(self):
        self.running = False

    def get_max(self):
        return self.limit

