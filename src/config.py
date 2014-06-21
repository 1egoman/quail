import json
import os

"""
Parse config files
"""
class configParser(object):

  def __init__(self, configdirectory="../config/"):

    # get config directory
    cfgdir = os.path.abspath(configdirectory)

    # make sure config folder exists
    if not os.path.exists( cfgdir ): os.mkdir(cfgdir)



    # server settings
    if not os.path.exists(os.path.join(cfgdir, "server.json")):
      # set default contents
      with open(os.path.join(cfgdir, "server.json"), 'w') as f:
        f.write("{\n  \"port\": 8000, \n  \"color\": true, \n  \"log-file\": \"log-latest.log\", \n  \"secret\": \"abc\"\n}\n")

    # read and parse json
    with open(os.path.join(cfgdir, "server.json")) as f:
      self.server = json.loads( f.read() )



    # quail personalization options
    if not os.path.exists(os.path.join(cfgdir, "quail.json")):
      # set default contents
      with open(os.path.join(cfgdir, "quail.json"), 'w') as f:
        f.write("""{\n  "name": "quail", \n  "gender": "male"\n}""")

    # read and parse json
    with open(os.path.join(cfgdir, "quail.json")) as f:
      self.quail = json.loads( f.read() )