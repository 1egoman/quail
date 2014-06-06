import factory
from query import *
import serverin as si

import inspect
import time
import json
import os

from BaseHTTPServer import HTTPServer


"""
List of ansi escape codes for color
"""
class colors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

  @staticmethod
  def reset():
    colors.HEADER = ''
    colors.OKBLUE = ''
    colors.OKGREEN = ''
    colors.WARNING = ''
    colors.FAIL = ''
    colors.ENDC = ''



""" 
Main application instance, which holds global vars and controls the server 
"""
class App(object):

  VERSION_MAJOR = 0
  VERSION_MINOR = 1
  VERSION_PATCH = 'A'

  def __init__(self):


    # read config file
    self.config = None

    # make sure config exists
    if not os.path.exists("../config.json"):
      with open("../config.json", 'w') as f:
        f.write("{\n  \"port\": 8000, \n  \"color\": true, \n  \"log-file\": \"log-latest.log\", \n  \"secret\": \"abc\"\n}\n")

    # read and parse json
    with open("../config.json") as f:
      self.config = json.loads( f.read() )

    # disable colors if needed
    if self.config.has_key("color") and not self.config["color"]:
      colors.reset()



    # open log if needed
    if self.config.has_key("log-file") and self.config["log-file"]:
      self.log_file = open( os.path.join("..", self.config["log-file"]), 'a')
    else:
      self.log_file = None

    self.log( "version %s.%s%s by Ryan Gaus! https://github.com/1egoman/qparser" % (self.VERSION_MAJOR, self.VERSION_MINOR, self.VERSION_PATCH) )
    self.running = 1
    self.plugins = load_all_plugins(self)


    # start server
    self.run()

  def run(self):
    try:

      # create terminal thread
      thrd = si.terminalFetcher(self)
      thrd.setName("terminalGetter")
      thrd.daemon = True
      thrd.start()

      # create thread to update each plugin regularly
      # thrd = updatethread(self)
      # thrd.setName("threadUpdate")
      # thrd.daemon = True
      # thrd.start()

      # get port
      if self.config.has_key("port"):
        port = self.config["port"]
      else:
        port = 8000

      # start server
      self.server = factory.MyHTTPServer(('', port), factory.http_rest, self)
      self.log( "done! type help or ? for a command list." )
      self.server.serve_forever()

      self.stop()

    except (KeyboardInterrupt, SystemExit):
      print '\n'
      self.stop()


  def stop(self):
    self.log( 'shutting down server' )
    self.server.socket.close()

    # close log
    if self.log_file: self.log_file.close()

  # logging
  def log(self, content, l=0):
    header = "%s[%s:%s%s%s]%s" % (colors.OKGREEN, inspect.stack()[1][3], colors.OKBLUE, time.strftime('%c'), colors.OKGREEN, colors.ENDC )
    colorless_header = "[%s:%s] " % (inspect.stack()[1][3], time.strftime('%c'))

    # to screen
    print header, content

    # to file
    if self.log_file: 
      self.log_file.write(colorless_header)
      self.log_file.write(content)
      self.log_file.write('\n')

if __name__ == '__main__':
  App()