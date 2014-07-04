import sys, os, json, imp
# location of plugins
PLGN_LOC = os.path.abspath("../plugins")

user = {}


# load all plugins
def load_all_plugins(q=None):
  # add to plugin search location
  sys.path.append(PLGN_LOC)
  plugins = []

  # look for plugins
  for s in sorted( os.listdir(PLGN_LOC) ):

    # make sure s is a folder, not a file and it doesn't start with _
    if not os.path.isdir( os.path.join(PLGN_LOC, s) ): continue
    if s.startswith('_'): continue

    # load plugin
    p = os.path.join(PLGN_LOC, s)

    # open config
    if not os.path.exists(os.path.join(p, "info.json")):
      if q:
        q.log( "plugin '%s' doesn't have info.json; ignoring plugin" % s)
      else:
        print "plugin '%s' doesn't have info.json; ignoring plugin" % s
      continue
    with open(os.path.join(p, "info.json")) as f:
      j = json.loads( f.read() )

    # output
    if q:
      q.log("loading %s: %s" % (j["name"], j["desc"]))
    else:
      print "loading %s: %s" % (j["name"], j["desc"])

    # now, read stuff from json into the plugins list
    plugins.append(j)

    # create a ready-to-call instance to the main class
    loc, name = j["main"].split(":")

    # also, temporarily add the plugin's folder to the search path
    sys.path.append(p)
    plugins[-1]["module"] = imp.load_source( name, os.path.join(p, loc) )
    exec "d = plugins[-1]['module']."+name
    plugins[-1]["call"] = d
    sys.path.remove(p)

    # add plugin directory to plugin list
    plugins[-1]["dir"] = p

  return plugins


# find the plugin that works
def find_correct_plugin(e, p, lastplugin=None, addr=None):

  # check last plugin
  if lastplugin:
    plgn = [  pl for pl in p if pl["name"] == lastplugin and "Wolfram Alpha" not in pl["name"]  ]
    if len(plgn):
      l = plgn[0]["call"](e, plgn[0], addr)
      if l.validate():
        return l, plgn[0]

  # loop through plugins
  for pl in p:
    c = pl["call"](e, pl)
    if c.validate():
      return c, pl

  return None

# get reference to 'd' at 'path'
def get_definition(path, d):
  loc, name = d.split(":")
  g = imp.load_source( name, os.path.join(path, loc) )
  exec "g = g."+name
  return g

# plugin test
def main():


  # load plugins
  a = load_all_plugins()



  print "Done! Enter a question."
  while 1:

    e = raw_input()
    if not e: 
      print "Quiting"
      break

    # run it
    c = find_correct_plugin(e, a)
    
    if c:
      print c.parse()
    else:
      print {"status": "NO_HIT"}





if __name__ == '__main__':
  main()