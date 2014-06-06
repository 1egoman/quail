from threading import Thread
import os
import sys
import warnings
import readline

import time
import query, queryobject as qo

class terminalFetcher(Thread):

  def __init__(self, parent):
    ''' Constructor. '''

    Thread.__init__(self)
    self.parent = parent
    self.prev_lines = []


  # keep it always running
  def run(self):
    try:
      self.main_part()
    except Exception, e:
      # warnings.warn(repr(e), Warning)
      raise
      self.run()

  def main_part(self):

    while self.parent.running:

      # normal input
      r = raw_input("")
      w = r.split(" ")[0]

      # quit
      if r == "quit" or r == "end" or r == "exit" or r == "stop":
        self.parent.running = 0
        self.parent.server.shutdown()#socket.close()

      elif r == "plugins":
        self.parent.log("Plugins:")
        self.parent.log( ', '.join([p["name"] for p in self.parent.plugins]) + " (%d)" % len(self.parent.plugins) )

      elif r == "help" or r == "?":
        self.parent.log("quit, plugins, query, reload, secret")

      elif r == "conn":
        self.parent.log( "Connections: %s" % [t.addr for t in self.parent.threads] )

      elif r == "reload":
        self.parent.plugins = query.load_all_plugins(self.parent)
        self.parent.log("reload complete.")

      elif r == "secret":
        if self.parent.config.has_key("secret"):
          self.parent.log( "Secret: '%s'" % self.parent.config["secret"] )
        else:
          self.parent.log( "No Secret" )

      elif w == "query" or w == "q":
        g = ' '.join(r.split(' ')[1:])
        g = qo.create_query_object( g )

        c = query.find_correct_plugin(g, self.parent.plugins)

        if c:
          out = c[0].parse(parent=self.parent)
          if out:
            self.parent.log( repr(out) )
          else:
            self.parent.log("(empty response)")



