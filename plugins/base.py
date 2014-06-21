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

# true or false evaluation
PHRASE_TRUE = True
PHRASE_FALSE = False

# preset types
TYPE_PUSH = "PUSH"

# different presentations
AS_LIST = "AS_LIST"
NORMAL = "NORMAL"


"""
Error for invalid key or credentials
"""
class InvalidKeyException(Exception): pass


"""
Base class for each plugin's parser
"""
class parser(object):

  # initialization
  def __init__(self, s, info=None):
    self.query = s
    self.info = info
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