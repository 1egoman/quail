import datetime as dt
import urllib2
import json



def parse_weather(self, when, where, API_KEY):


    # if there is no time, create one
    if not (type(when) == dict and when.has_key("when") and when["when"][2] != dt.datetime.now().day):
      when = {"when": [dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day]}

    # get from api
    u = urllib2.urlopen("http://api.wunderground.com/api/%s/forecast10day/q/autoip.json" % API_KEY)
    weather = json.loads( u.read() )
    weather = weather["forecast"]["simpleforecast"]["forecastday"]


    # find correct day
    w = [w for w in weather if w["date"]["year"] == when["when"][0] and w["date"]["month"] == when["when"][1] and w["date"]["day"] == when["when"][2]]
    
    if len(w):

      # get weather
      weather = w[0]
      conditions = weather["conditions"].lower()
      temp = "a high of %s degrees, and a low of %s degrees" % (weather["high"]["fahrenheit"], weather["low"]["fahrenheit"])
      high, low = float(weather["high"]["fahrenheit"]), float(weather["low"]["fahrenheit"])
    else:

      # no conditions in query
      self.resp["text"] = "no weather available"
      return


    # tempurature
    if "tempurature" in self.query:
      t = (high+low)/2
      self.resp["text"] = "%s degrees" % t
      return


    elif "high" in self.query:
      self.resp["text"] = "%s degrees" % high
      return


    elif "low" in self.query:
      self.resp["text"] = "%s degrees" % low
      return


    elif "conditions" in self.query:
      self.resp["text"] = conditions
      return


    elif "rain" in self.query or "storm" in self.query or "snow" in self.query:

      # get when it is happening
      if when["when"] == [dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day]:
        p = "it is %sing"
      else:
        p = "it will %s"

      if "rain" in conditions or "storm" in conditions or "snow" in conditions:
        self.resp["text"] = p % "rain"
        self.resp["color"] = "blue"
      else:
        self.resp["text"] = p % "not rain"
      return 


    elif "sun" in self.query:

      # get when it is happening
      if when["when"] == [dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day]:
        p = "it is %s"
      else:
        p = "it will be %s"

      if "sun" in conditions:
        self.resp["text"] = p % "sunny"
        self.resp["color"] = "blue"
      else:
        self.resp["text"] = p % "not sunny"
      return 


    elif "cloud" in self.query:

      # get when it is happening
      if when["when"] == [dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day]:
        p = "it is %s"
      else:
        p = "it will be %s"

      if "cloud" in conditions:
        self.resp["text"] = p % "cloudy"
        self.resp["color"] = "blue"
      else:
        self.resp["text"] = p % "not cloudy"
      return 


    elif "weather" in self.query:
      t = (high+low)/2
      self.resp["text"] = "%s degrees, and %s" % (t, conditions)