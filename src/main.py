import factory
from query import *
import serverin as si
from config import configParser
from listener import listenerThread

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

  # quail version
  VERSION_MAJOR = 0
  VERSION_MINOR = 3
  VERSION_PATCH = 'E'

  def __init__(self):


    # read config files
    self.config = None
    self.config = configParser()


    # disable colors if needed
    if self.config.server.has_key("color") and not self.config.server["color"]:
      colors.reset()

    # create stack, used to store outgoing packets
    self.stack = []


    # open log if needed
    if self.config.server.has_key("log-file") and self.config.server["log-file"]:
      self.log_file = open( os.path.join("..", self.config.server["log-file"]), 'a')
    else:
      self.log_file = None


    self.log( "version %s.%s%s by Ryan Gaus! https://github.com/1egoman/quail" % (self.VERSION_MAJOR, self.VERSION_MINOR, self.VERSION_PATCH) )
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

      # create thread to update each listener
      thrd = listenerThread(self, self.plugins)
      thrd.setName("threadListener")
      thrd.daemon = True
      thrd.start()

      # get port
      if self.config.server.has_key("port"):
        port = self.config.server["port"]
      else:
        port = 8000


      # start server
      self.server = factory.MyHTTPServer(('', port), factory.http_rest, self)
      self.log("hosted on port :%s" % port)
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

  # reload server
  def reload(self):
    self.plugins = load_all_plugins(self)
    self.log("plugin reload complete.. done")

    # reload config
    self.config = configParser()
    self.log("config reload complete..done")

if __name__ == '__main__':
  App()
