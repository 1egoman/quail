from base import *
import datetime as dt
import weather as wtr
# what this should do:
#  reminders
#  weather
#  calender


# month list
months = {
  1: "january", 
  2: "febuary", 
  3: "march", 
  4: "april", 
  5: "may", 
  6: "june", 
  7: "july", 
  8: "augest", 
  9: "september", 
  10: "october", 
  11: "november", 
  12: "december"
}

# day list
days = {
  "monday": 0,
  "tuesday": 1,
  "wednesday": 2,
  "thursday": 3,
  "friday": 4,
  "saturday": 5,
  "sunday": 6
}

# weather terms
weather_terms = ["weather", "rain", "sun", "cloud", "snow", "wind", "tempurature", "conditions", "storm", "advisory"]

# weather listener
def weather_listener(parent):
  # print "listened!"
  pass


class main_parser(parser):
  """ weather parser class """

  def validate(self):
    return len([1 for d in weather_terms if d in self.query])

  def parse(self, parent):

    # get api key
    if self.info.has_key("key"):
      WEATHER_API_KEY = self.info["key"]
    else:
      self.resp["text"] = "bad key"
      self.resp["type"] = "weather"
      self.resp["status"] = STATUS_ERR
      return self.resp

    # define vars
    where = None
    times = ["am", "pm", "minutes", "tommorow", "yesterday"]
    times.extend(days)



    # if weather terms... get the weather
    if len([1 for d in weather_terms if d in self.query]):

      # determine when
      when = [w for w in self.query if type(w) == dict and w.has_key("type") and w["type"] == "time"]
      if len(when):
        when = when[0]
      else:
        out = dt.datetime.now().strftime("%Y:%m:%d:%X").replace("/", ":")
        when = [int(d) for d in out.split(":")]


      wtr.parse_weather(self, when, "", WEATHER_API_KEY)

    # return
    self.resp["status"] = STATUS_OK
    self.resp["type"] = "weather"
    return self.resp


