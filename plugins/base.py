# main file
import datetime
import urllib2
import json
import os

""" Constants for user_data """
class RELATION:
  # family
  MOTHER = 0
  FATHER = 0.1
  SISTER = 0.2
  BROTHER = 0.3
  CHILD = 0.4

  # extended family
  AUNT = 0.5
  UNCLE = 0.6
  GRANDMA = 0.7
  COUSIN = 0.8

  # freinds
  FREIND = 2.0
  ACQUAINT = 2.1 # acquaintance

  # work
  BOSS = 3.0
  COWORKER = 3.1


# status codes
STATUS_OK = "OK"
STATUS_NO_HIT = "NO_HIT"
STATUS_ERR = "ERROR"
STATUS_UNKNOWN = "NONE"


""" searchable_list: list with a function to search through the records """
class searchable_list(list):
  # search records
  def search(self, key, value):
    for i in self:
      if i.__dict__.has_key(key) and i.__dict__[key] == value:
        return i
        break



""" Record: holds information inside a collection """
class record(object):

  def __eq__(self, other):
    if type(other) == type(self):
      return True
    else:
      return False

  def __getitem__(self, k):
    return self.__dict__[k]

  # for printing
  def __repr__(self):
    # name
    if self.__dict__.has_key("name"): return self.name

    # first/last name
    if self.__dict__.has_key("first"): 
      if self.__dict__.has_key("last"):
        return "%s %s" % (self.first, self.last)
      else:
        return self.first

    # aliases
    if self.__dict__.has_key("aliases") and type(self.aliases) == list: 
      return self.aliases[0]

    return "<%s object>" % self.__class__.__name__

""" Person: contains a person's info """
class person(record):
  first = None
  last = None
  relation = None
  aliases = []

""" Place: contains a person's info """
class place(record):
  name = None
  aliases = []
  address = None
  city = None
  state = None
  zip = None

""" Event: contains everything for an event """
class event(record):
  name = None
  aliases = None
  when = None
  where = None
  type = None



""" Contains the information of the user """
class user_data(object):


  # info object
  class info: pass


  def __init__(self):

    # get user's info
    with open( os.path.abspath( os.path.join("..", "user.json") ), 'r') as f:
      self.raw = json.loads( f.read() )


    # let the parsing begin!
    self.extract_creds()



  # put users info into the class
  def extract_creds(self):

    # user data
    self.info.first = self.extract_at("info", "first")
    self.info.last = self.extract_at("info", "last")
    self.info.gender = self.extract_at("info", "gender")

    # people
    self.people = searchable_list()

    # add records
    for i in self.extract_at("people"):
      p = person()

      # loop through json, adding records
      for k,v in i.items():
        p.__dict__[k] = v

      self.people.append(p)



    # places
    self.places = searchable_list()

    # add records
    for i in self.extract_at("places"):
      p = place()

      # loop through json, adding records
      for k,v in i.items():
        p.__dict__[k] = v

      self.places.append(p)



    # events
    self.events = searchable_list()

    # add records
    for i in self.extract_at("events"):
      p = event()

      # loop through json, adding records
      for k,v in i.items():
        p.__dict__[k] = v

      self.events.append(p)


  def push(self):

    # add records
    people = []
    for i in self.people:
      people.append( i.__dict__ )

    places = []
    for i in self.places:
      places.append( i.__dict__ )

    events = []
    for i in self.events:
      events.append( i.__dict__ )

    total = { "info": self.raw["info"], "people": people, "places": places, "events": events }

    with open( os.path.abspath( os.path.join("..", "user.json") ), 'w') as f:
      f.write( json.dumps(total, indent=2) )


  # get element at dictionary keys specified by *args
  def extract_at(self, *args):
    cursor = self.raw
    for i in args:
      if ( type(cursor) == dict and cursor.has_key(i) ) or ( type(cursor) == list and len(cursor) < i ):
        cursor = cursor[i]
      else:
        raise Warning( "Couldn't traverse data with key '%s': please add to config" % i )
        return None

    return cursor





# initilize user data
user = user_data()






""" Packet response """
class packet(dict):

  def __init__(self): 
    self.status = STATUS_UNKNOWN
    self.packet = "response"
    self.type = None
    self.text = ""
    self.__dict__["return"] = ""


  # for dictionary-like addressing
  def __getitem__(self, k):
    return self.__dict__[k]





""" Base class for each plugin """
class parser(object):

  # initialization
  def __init__(self, s, info):
    self.query = s
    self.info = info
    self.resp = packet()
    self.resp = {
      "status": "BAD",
      "packet": "response",
      "type": None,
      "text": "No Response."
    }

  # validate the query
  def validate(self): return False

  # parse user's query
  def parse(self):
    
    # return response packet
    self.resp["status"] = STATUS_OK
    return self.resp

  def get_plugin_dir(self, f): # f should be __file__
    d = f.split(os.sep)[-2]
    return os.path.abspath( os.path.join("..", "plugins", d) )

