from base import *
import os
import json


class staticParser(Parser):
  """ Static Plugin Parser """

  def validate(self):

    # read phrases
    with open(  os.path.join(self.get_plugin_dir(__file__), "phrases.json")  ) as f:
      self.phrases = json.loads( f.read() )

    # validate
    querystr = ' '.join(self.query)
    return len([1 for i in self.phrases if i in querystr])

  def parse(self, parent):

    # get phrase
    querystr = ' '.join(self.query)
    phrase = [i for i in self.phrases if i in querystr]
    if len(phrase):
      longestphrase = sorted(phrase, key=lambda x: len(x))[-1]
      self.resp["text"] = self.phrases[ longestphrase ]
      self.resp["status"] = STATUS_OK
    else:
      self.resp["text"] = "phrase doesn't exist"
      self.resp["status"] = STATUS_NO_HIT

    # return the packet
    self.resp["type"] = "static"
    return self.resp