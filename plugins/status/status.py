from base import *

class statusParser(Parser):
  """ Parses status queries sent by a client """

  def validate(self):
    return ["_quail"] == self.query

  def parse(self, parent): 

    # quail
    if ["_quail"] == self.query:
      # return status info
      self.resp["text"] = parent.config.quail

    self.resp["status"] = STATUS_OK
    self.resp["type"] = "quailstatus"
    return self.resp