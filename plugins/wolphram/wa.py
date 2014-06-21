import base
import xml.etree.ElementTree as et
import urllib2



# main class
class WAParser(base.parser):

  def __init__(self, *args, **kwargs):
    super(WAParser, self).__init__(*args, **kwargs)

  # always our last hope
  def validate(self): return True

  # parse user's query
  def parse(self, parent):

    # get key from config
    if self.info.has_key("key"):
      API_KEY = self.info["key"]
    else:
      self.resp["text"] = "bad key"
      self.resp["type"] = "wa"
      self.resp["status"] = base.STATUS_ERR
      return self.resp


    # set data type of packet
    self.resp["type"] = "wolfram"

    # get text from query string
    query = ""
    for q in self.query:
      if type(q) == dict:
        query += q["text"]
      else:
        query += q

    # query
    h = urllib2.urlopen("http://api.wolframalpha.com/v2/query?input="+query.replace(" ", "%20")+"&appid="+API_KEY)
    xml = h.read()
    root = et.fromstring(xml)

    # sub data type
    self.resp["subtype"] = root.attrib["datatypes"]
    
    # parse now
    for pod in root:
      if pod.tag == "pod":
        # loop through pod now
        # don't even check input pods
        if "Input" in pod.attrib["title"]: continue

        # check through sub pod's to find any plaintext
        for sp in pod:
          # look at tags inside subpod
          for t in sp:
            if t.tag == "plaintext":
              self.resp["text"] = t.text.replace("\n", " ").replace(" | ", ": ")

              if t.text and " | " in t.text:
                self.resp["return"] = [g.split(" | ") for g in t.text.split("\n") if g]
              elif t.text:
                self.resp["return"] = t.text.split("\n")
              else:
                self.resp["return"] = None

              # close socket
              h.close()
              
              # return response packet
              self.resp["status"] = base.STATUS_OK
              return self.resp

