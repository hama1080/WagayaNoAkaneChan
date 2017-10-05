# -*- coding:utf-8 -*-
import urllib.request as urlreq
import json
import config

class Weather():
    def __init__(self):
        self.json_data = None
        self.update()

    def update(self):
        with urlreq.urlopen("http://weather.livedoor.com/forecast/webservice/json/v1?city=" + config.WE_LOCATION) as response:
            self.json_data = json.loads(response.read().decode("utf-8"))

    def get_location(self):
        return self.json_data["title"].lstrip(" の天気")

    def get_weather(self):
        res = []
        for forecast in self.json_data["forecasts"]:
            res.append(forecast["telop"])

        return res

    def get_temperture_min(self):
        res = []
        for forecast in self.json_data["forecasts"]:
            data = forecast["temperature"]["min"]
            if data == None:
                res.append(None)
            else:
                res.append(data["celsius"])
                
        return res

    def get_temperture_max(self):
        res = []

        for forecast in self.json_data["forecasts"]:
            data = forecast["temperature"]["max"]
            if data == None:
                res.append(None)
            else:
                res.append(data["celsius"])

        return res
    
    
if __name__ == "__main__":
    w = Weather()
    print(w.get_weather())
    print(w.get_temperture_min())
    print(w.get_temperture_max())
                  
    
        
    
