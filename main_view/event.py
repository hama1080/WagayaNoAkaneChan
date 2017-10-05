# -*- coding:utf-8 -*-
from enum import Enum

class Value(Enum):
    WEATHER = 1
    MAIL = 2
    SCHEDULE = 3
    VOICE_RECOGNITION = 4
    NEXT = 5
    ON = 6
    OFF = 7
    ORANGE = 8
    

class Command(Enum):
    TRANSITION = 1
    LIGHT = 2
    TV = 3

def parse_from_string(s):

    command = Command.TRANSITION
    value = Value.WEATHER
    
    if "天気" in s:
        value = Value.WEATHER
    elif "スケジュール" in s:
        value = Value.SCHEDULE
    elif "メール" in s:
        value = Value.MAIL
    elif "電気" in s:
        if "つけて" in s:
            command = Command.LIGHT
            value = Value.ON
        elif "消して" in s:
            command = Command.LIGHT
            value = Value.OFF
    elif "常備" in s:
        command = Command.LIGHT
        value = Value.ORANGE
    elif "テレビ" in s:
        if "つけて" in s:
            command = Command.TV
            value = Value.ON
        elif "消して" in s:
            command = Command.TV
            value = Value.OFF
        

    return command, value
    
    
class EventManager:
    
    def __init__(self):
        #threading.Lockとかで管理するべき
        self.event_queue = []

    def enqueue_event(self, command, value):
        self.event_queue.append({"command": command, "value":value})

    #生文から判別できたら便利すぎうち
    def enqueue_event_from_string(self, event_str):
        pass
    
    def dequeue_event(self):
        if len(self.event_queue) == 0:
            return None, None
        
        next_event = self.event_queue[0]
        self.event_queue = self.event_queue[1:]
        return next_event["command"], next_event["value"]

    
    
