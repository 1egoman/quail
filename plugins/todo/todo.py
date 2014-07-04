from base import *
import os
from json import loads, dumps

# what is on my grocery list
# add bread to my grocery list

LIST_FILE = "lists.json"
TODO_ADD_WORDS = ["named", "called", "create", "add"]
TODO_DEL_WORDS = ["named", "called", "check", "delete", "remove"]
STRIP_WORDS = ["to", "from", "on", "in", "by", "list"]


class TodoParser(Parser):




  def validate(self): 

    # read lists from file
    with open(os.path.join(self.get_plugin_dir(__file__), LIST_FILE)) as j:
      self.lists = loads( j.read() )

    # validate
    querystr = ' '.join([str(i) for i in self.query])
    for l in self.lists:
      if l["name"] in querystr:
        self.our_list = l
        return 1
    return 0




  def parse(self, parent):

    # set packet type
    self.resp["type"] = "todo"


    # add item
    if self.our_list and "add" in self.query or "create" in self.query:

      addwords = [aw for aw in TODO_ADD_WORDS if aw in self.query]
      if len(addwords):
        
        # strip off all words before the keyword
        qw = self.query[ self.query.index(addwords[0])+1: ]

        endwords = [aw for aw in STRIP_WORDS if aw in reversed(qw)]
        if len(endwords):
          # strip off all words after keyword
          qw = qw[ :qw.index(endwords[0]) ]

        # get items to add to list
        items = [{"name": f.strip(), "tags": [], "when": ""} for f in ' '.join(qw).replace("and", ',').split(',')]

        # now, actually add to list
        self.our_list["contents"].extend( items )
        self.update_list()
        self.resp["status"] = STATUS_OK
        self.resp["text"] = "Added to %s" % self.our_list["name"]



    # delete item
    elif self.our_list and ("delete" in self.query or "check" in self.query or "remove" in self.query):

      addwords = [aw for aw in TODO_DEL_WORDS if aw in self.query]
      if len(addwords):
        
        # strip off all words before the keyword
        qw = self.query[ self.query.index(addwords[0])+1: ]

        endwords = [aw for aw in STRIP_WORDS if aw in reversed(qw)]
        if len(endwords):
          # strip off all words after keyword
          qw = qw[ :qw.index(endwords[0]) ]

        # get items to add to list
        items = [f.strip() for f in ' '.join(qw).replace("and", ',').split(',')]

        # now, actually delete from list
        for i in self.our_list["contents"]: 
          if type(i) == dict and i["name"] in items:
            self.our_list["contents"].remove(i)

        self.update_list()
        self.resp["status"] = STATUS_OK
        self.resp["text"] = "Removed from %s" % self.our_list["name"]



    else:
      # list all items
      self.resp["status"] = STATUS_OK
      self.resp["return"] = [i["name"] for i in self.our_list["contents"]]
      self.resp["text"] = "%s list: %s" % (self.our_list["name"], ';'.join(self.resp["return"]))
      self.resp["present"] = AS_LIST

  def update_list(self):
    with open(os.path.join(self.get_plugin_dir(__file__), LIST_FILE), 'w') as j:
      j.write(dumps(self.lists, indent=2))