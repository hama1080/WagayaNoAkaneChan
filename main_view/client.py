# -*- coding:utf-8 -*-
import time
import re
import datetime
import subprocess

#modules
from audio_play import play
from weather import Weather
from gmail import GMail
from schedule import Schedule
from clocker import Clocker
from event import EventManager
from voice_recognizer import VoiceRecognizer
from twitter_checker import TwitterChecker
from remote_module import Remote_module
import event
import config

#import kivy modules
import kivy
kivy.require("1.10.0")

#from kivy.core.window import Window
#Window.size = (770, 520)
#タイトルバー消すときはここをTrue
#Window.borderless = False

from kivy.config import Config
Config.set('graphics','resizable',0)

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.lang import Builder

#GLOBAL
FONT = "RoundMPlus"

class MainApp(App):
    
    def build(self):
        
        layout = BoxLayout(orientation="vertical", padding = 10, size_hint_x=0.65)

        #label
        self.label = ScreenLabel()
        
        #screen
        self.main_screen = MainScreen()

        #ProgressBar
        self.progress_bar = TimeProgressBar()

        #clock
        self.clock = MyClock()
        
        
        layout.add_widget(self.label)
        layout.add_widget(self.main_screen)
        layout.add_widget(self.progress_bar)
        layout.add_widget(self.clock)

        #event manager
        self.event_manager = EventManager()
        
        #clocker
        self.clocker = Clocker(self.event_manager)
        self.clocker.start()
        
        #voice_recognition
        self.voice_recognizer = VoiceRecognizer(self.event_manager)
        self.voice_recognizer.start()

        #twitter checker
        self.twitter_checker = TwitterChecker(self.event_manager)
        self.twitter_checker.start()

        #remote controller
        self.remote = Remote_module()
        
        #voice audio list
        self.VOICE={"VOICE_RECOGNITION":"voice/01.wav",
                    "WEATHER":"voice/02.wav",
                    "MAIL":"voice/03.wav",
                    "SCHEDULE":"voice/04.wav",
                    "LIGHT_ON":"voice/05.wav",
                    "LIGHT_OFF":"voice/06.wav",
                    "LIGHT_ORANGE":"voice/07.wav",
                    "TV_ON":"voice/08.wav",
                    "TV_OFF":"voice/09.wav"}

        Clock.schedule_interval(self.update, 0.05)
        
        return layout

    def on_stop(self):
        self.clocker.stop()
        self.voice_recognizer.stop()
        self.twitter_checker.stop()
        
    def update(self, dt):

        command, value = self.event_manager.dequeue_event()

        def restart_clocker(clocker):
            self.clocker.stop()
            self.clocker = clocker
            self.clocker.start()
        
        #どちらも値が入ってる場合、イベント処理
        if command and value:
            if command == event.Command.TRANSITION:
                if value == event.Value.NEXT:
                    self.main_screen.switch_next()
                    self.clocker.reset()
                elif value == event.Value.VOICE_RECOGNITION:
                    self.clocker.stop()
                    self.main_screen.switch("音声認識")
                    play(self.VOICE["VOICE_RECOGNITION"])
                elif value == event.Value.WEATHER:
                    restart_clocker(Clocker(self.event_manager))
                    self.main_screen.switch("天気")
                    play(self.VOICE["WEATHER"])
                elif value == event.Value.MAIL:
                    restart_clocker(Clocker(self.event_manager))
                    self.main_screen.switch("メール")
                    play(self.VOICE["MAIL"])
                elif value == event.Value.SCHEDULE:
                    restart_clocker(Clocker(self.event_manager))
                    self.main_screen.switch("スケジュール")
                    play(self.VOICE["SCHEDULE"])           
            if command == event.Command.LIGHT:
                if value == event.Value.ON:
                    restart_clocker(Clocker(self.event_manager, 3, event.Value.WEATHER))
                    self.main_screen.switch("メッセージ")
                    self.main_screen.current_screen.set_text("電気つけたで")
                    self.remote.remoteAction("LIGHT_ON")
                    play(self.VOICE["LIGHT_ON"])
                elif value == event.Value.OFF:
                    restart_clocker(Clocker(self.event_manager, 3, event.Value.WEATHER))
                    self.main_screen.switch("メッセージ")
                    self.main_screen.current_screen.set_text("電気消したで")
                    self.remote.remoteAction("LIGHT_OFF")
                    play(self.VOICE["LIGHT_OFF"])
                elif value == event.Value.ORANGE:
                    restart_clocker(Clocker(self.event_manager, 3, event.Value.WEATHER))
                    self.main_screen.switch("メッセージ")
                    self.main_screen.current_screen.set_text("常備灯にしたで")
                    self.remote.remoteAction("LIGHT_ORANGE")
                    play(self.VOICE["LIGHT_ORANGE"])
            if command == event.Command.TV:
                if value == event.Value.ON:
                    restart_clocker(Clocker(self.event_manager, 3, event.Value.WEATHER))
                    self.main_screen.switch("メッセージ")
                    self.main_screen.current_screen.set_text("テレビつけたで")
                    self.remote.remoteAction("TV_ON")
                    play(self.VOICE["TV_ON"])
                elif value == event.Value.OFF:
                    restart_clocker(Clocker(self.event_manager, 3, event.Value.WEATHER))
                    self.main_screen.switch("メッセージ")
                    self.main_screen.current_screen.set_text("テレビ消したで")
                    self.remote.remoteAction("TV_OFF")
                    play(self.VOICE["TV_OFF"])
                
        
        self.label.set_screen_name(self.main_screen.get_current_name())
        self.progress_bar.update(self.clocker.get_current_time())
        self.clock.update()

        if "update" in dir(self.main_screen.current_screen):
            self.main_screen.current_screen.update()
        

class TimeProgressBar(ProgressBar):
    def __init__(self):
        import clocker
        super(TimeProgressBar, self).__init__(size_hint_y = 0.1, max = config.MAIN_PROGRESS_BAR_MAX)

    def update(self, value):
        self.value = value
        
class ScreenLabel(Label):
    
    def __init__(self):
        super(ScreenLabel, self).__init__(
            font_name = FONT,
            font_size = self.height / 2,
            text_size = self.size,
            halign="left",
            valign="middle",
            padding=(10,0),
            size_hint_y = 0.2
            )

        #sizeを設定してやるとalignが左になる
        self.bind(size=self.setter("text_size"))

    def set_screen_name(self, screen_name):
        self.text = screen_name

  
class MyClock(Widget):
    time_str = StringProperty()
    day_str = StringProperty()
    
    def __init__(self):
        super(MyClock, self).__init__(size_hint_y = 0.2)
        self.update()

    def update(self):
        self.time_str = self.get_time()
        self.day_str = self.get_day()

    def get_time(self):
        return time.strftime("%H:%M:%S", time.strptime(time.ctime()))

    def get_day(self):
        return time.strftime("%Y/%m/%d", time.strptime(time.ctime()))
    
        
class MainScreen(ScreenManager):
    
    def __init__(self):
        super(MainScreen, self).__init__(transition=SlideTransition())
        self.add_widget(MailScreen())
        self.add_widget(ScheduleScreen())
        self.add_widget(WeatherScreen())
        self.add_widget(VoiceRecognitionScreen())
        self.add_widget(MessageScreen())

        self.ordinary_list = ["スケジュール","天気", "メール"]
        
    def get_current_name(self):
        return self.current

    def switch_next(self):
        self.current = self.ordinary_list[(self.ordinary_list.index(self.current) + 1) % len(self.ordinary_list)]

    def switch(self, scr):
        self.current = scr

class WeatherScreen(Screen):
    
    def __init__(self):
        self.font = FONT
        self.api = Weather()
        super(WeatherScreen, self).__init__(name = "天気")#self.api.get_location()
        
    def get_weather(self, index):
        weather_list = self.api.get_weather()

        if index >= len(weather_list):
            return "NoData"
        
        return weather_list[index]

    def get_weather_image(self, index):
        weather_list = self.api.get_weather()
        if index < len(weather_list):
            weather = weather_list[index]
            si = re.search("[晴曇雨]", weather).start()
            if si != None:
                if weather[si] == "晴":
                    return "img/sunny.png"
                elif weather[si] == "雨":
                    return "img/rainy.png"
                elif weather[si] == "曇":
                    return "img/cloudy.png"
            
        return "img/no_image.png"


class VoiceRecognitionScreen(Screen):
    pb_value = NumericProperty()
    
    def __init__(self):
        super(VoiceRecognitionScreen, self).__init__(name = "音声認識")
        self.start_time = 0
        
    def on_enter(self):
        self.pb_value = 0
        self.start_time = time.time()
        
    def update(self):
        self.pb_value = time.time() - self.start_time

    def get_max(self):
        return config.VR_RECORD_SECONDS

class MessageScreen(Screen):
    text_str = StringProperty("DEFAULT MESSAGE")
    
    def __init__(self):
        super(MessageScreen, self).__init__(name = "メッセージ")

    def set_text(self, text):
        self.text_str = text
    

class ScheduleScreen(Screen):
    def __init__(self):
        super(ScheduleScreen, self).__init__(name = "スケジュール")
        self.api = Schedule()
        self.update_nodes()

    def update_nodes(self):
        self.ids["today"].clear_widgets()
        self.ids["after"].clear_widgets()

        def encode_day(start_time):
            dt = ""

            if "dateTime" in start_time:
                dt = datetime.datetime.strptime(start_time["dateTime"][:-6], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d")
            elif "date" in start_time:
                dt = datetime.datetime.strptime(start_time["date"], "%Y-%m-%d").strftime("%m/%d")
            else:
                dt = "Day"

            return dt

        def encode_time(start_time):
            dt = ""

            if "dateTime" in start_time:
                dt = datetime.datetime.strptime(start_time["dateTime"][:-6], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")
            else:
                dt = "All Day"

            return dt
            
        for event in self.api.get_after_events():
            summary = event["summary"].replace(" ", "")
            start_time = event["start"]
            dt = encode_day(start_time)
            self.ids["after"].add_widget(ScheduleNodeAfter(dt, summary))
            

        for event in self.api.get_today_events():
            summary = event["summary"].replace(" ", "")
            start_time = event["start"]
            dt = encode_time(start_time)
            self.ids["today"].add_widget(ScheduleNodeDay(dt, summary))
        
class ScheduleNodeDay(Widget):
    time_str = StringProperty()
    summary_str = StringProperty()
    
    def __init__(self, time, summary):
        super(ScheduleNodeDay, self).__init__(size_hint = (1, 0.2))
        self.time_str = time
        self.summary_str = summary

class ScheduleNodeAfter(Widget):
    time_str = StringProperty()
    summary_str = StringProperty()
    
    def __init__(self, time, summary, orient="vertical"):
        super(ScheduleNodeAfter, self).__init__(size_hint = (1, 0.13))
        self.time_str = time
        self.summary_str = summary

class MailNode(Widget):
    from_str = StringProperty("from")
    subject_str = StringProperty("subject")
    text_str = StringProperty("text")
    date_str = StringProperty("date")

    def set(self, f, s, t, d):
        self.from_str = f
        self.subject_str = s
        self.text_str = t
        self.date_str = d
    
    def __init__(self):
        super(MailNode, self).__init__(size_hint = (1, 1))

    
class MailScreen(Screen):

    def __init__(self):
        self.api = GMail()
        super(MailScreen, self).__init__(name = "メール", size_hint=(1, 1))
        self.ids.layout.add_widget(MailNode())
        self.ids.layout.add_widget(MailNode())
        self.ids.layout.add_widget(MailNode())
        self.update_nodes()

    #ここ２つちょっと追加
    def cut_FromText(self,fromText):
        return fromText.split('<')[0]
    
    def shape_DateText(self,dateText):
        return dateText.split('+')[0]

    def update_nodes(self):
        
        self.mails = self.api.get_mail(3)
        
        for mail, node in zip(self.mails, self.ids.layout.children[::-1]):
            snippet = mail["snippet"].replace("\n", "")

            data = {}
            for elem in mail["payload"]["headers"]:
                if elem["name"] in ["From", "Subject", "Date"]:
                    data.update({elem["name"]:elem["value"]})


            node.set(self.cut_FromText(data["From"]), data["Subject"], snippet,self.shape_DateText(data["Date"]))

if __name__ == "__main__":
    config.check()
    MainApp().run()
