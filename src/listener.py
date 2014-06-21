from threading import Thread
import time
import query

class listenerThread(Thread):
  """ Thread that runs all the listeners each frame """

  def __init__(self, parent, pl):
    Thread.__init__(self)
    self.plugins = pl
    self.parent = parent

  def run(self):
    while 1:
      # loop through all plugins
      for p in self.plugins:

        # only worry about plugins with listeners
        if not p.has_key("listener"): continue

        # get listener instance
        direc = p["dir"]
        l = query.get_definition(direc, p["listener"])
        l(parent=self.parent)

      # delay before next frams
      time.sleep(1)