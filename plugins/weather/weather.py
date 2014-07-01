import datetime as dt
import urllib2
import json

def parse_weather(self, when, where, API_KEY):

    # get the weather
    #if when == dupwhen:

    # do time
    if type(when) == dict and when.has_key("when") and when["when"][2] != dt.datetime.now().day:
      u = urllib2.urlopen("http://api.wunderground.com/api/%s/forecast10day/q/autoip.json" % API_KEY)
      weather = json.loads( u.read() )
      weather = weather["forecast"]["simpleforecast"]["forecastday"]
      

      # find correct day
      w = [w for w in weather if w["date"]["year"] == when["when"][0] and w["date"]["month"] == when["when"][1] and w["date"]["day"] == when["when"][2]]
      
      if len(w):

        # get weather
        weather = w[0]
        conditions = "with %s" % weather["conditions"].lower()
        temp = "a high of %s degrees, and a low of %s degrees" % (weather["high"]["fahrenheit"], weather["low"]["fahrenheit"])
      else:

        # no cnditions in query
        conditions = "No weather for this day"
        temp = ""


    else:
      u = urllib2.urlopen("http://api.wunderground.com/api/%s/conditions/q/autoip.json" % API_KEY)
      weather = json.loads( u.read() )
      conditions = "and %s" % weather["current_observation"]["weather"].lower()
      temp = "a tempurature of %s degrees" % weather["current_observation"]["feelslike_f"]




    # find type of request

    if "rain" in self.query:
      if "rain" in conditions or "storm" in conditions or "snow" in conditions:
        self.resp["return"] = "raining"
        self.resp["color"] = "blue"
      else:
        self.resp["return"] = "not raining"
      self.resp["text"] = "it is %s" % self.resp["return"]


    elif "sun" in self.query:
      if "sun" in conditions:
        self.resp["return"] = "sunny"
        self.resp["color"] = "yellow"
      else:
        self.resp["return"] = "not sunny"
      self.resp["text"] = "it is %s" % self.resp["return"]


    elif "cloud" in self.query:
      if "cloud" in conditions:
        self.resp["return"] = "cloudy"
        self.resp["color"] = "white"
      else:
        self.resp["return"] = "not cloudy"
      self.resp["text"] = "it is %s" % self.resp["return"]
    
    elif "conditions" in self.query:
      self.resp["text"] = conditions

    elif "weather" in self.query:
      self.resp["return"] = [temp, conditions ]
      self.resp["text"] = ( "%s %s" % tuple( self.resp["return"] ) ).strip()

