from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import inspect
import urllib2
import urlparse
import os
from json import dumps

from queryobject import create_query_object
from query import find_correct_plugin


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


lastplugin = None
iteration = 0




class http_rest(BaseHTTPRequestHandler):
  """ this class deals with incoming http requests """
  

  def do_GET(self):
    global lastplugin, iteration

    # make sure we have permission
    data = self.parse_path()

    # authentication
    if len(data) and self.server.parent.config.server.has_key("secret") and data[0] == self.server.parent.config.server["secret"]:


      # get rid of password in data string
      data = data[1:]

      # get any variables from url
      lastquestion = self.path.rfind('?')
      if lastquestion != -1:
        get_args = urlparse.parse_qs(self.path[lastquestion+1:])
      else:
        get_args = {}

      # if there is data
      if len(data):

        # the header
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


        # start building json response
        response = {}

        # parse text for plugin
        query = create_query_object( data[0] )


        # what kind of request?
        if len(data) > 1:
          # a plugin was specified in the url

          # find the correct plugin
          plugin = [  p for p in self.server.parent.plugins if p["name"] == data[0] or (p.has_key("shortname") and p["shortname"] == data[0])  ]
          if len(plugin):
            query = create_query_object( data[1] )
            d, plugin_name = plugin[0], plugin[0]["name"]
            plugin_call = d["call"](query, d)
          else:
            self.send_error(404, "no such plugin can be found")
            return




        else:
          # a plugin wasn't specified in the url

          # find correct plugin
          plugin = find_correct_plugin( query, self.server.parent.plugins, lastplugin=lastplugin)
          if plugin:
            plugin_call, plugin_name = plugin[0], plugin[1]["name"]
          else:
            self.send_error(404, "no such plugin can be found")
            return

        # set this plugin to be last plugin, for checking it first later on
        if lastplugin == plugin_name:
          iteration += 1
        else:
          iteration = 0
        lastplugin = plugin_name
        plugin_call.iteration = iteration




        # log what we are doing
        self.server.parent.log( "plugin: %s -> %s" % (plugin_name, query) )

        # parse it, and add to stack
        plugin_call.parse(parent=self.server.parent)
        out = plugin_call.resp

        # write out the stack
        if out:
          self.server.parent.stack.append(out)
        else:
          self.server.parent.stack.append("{\n  \"status\": \"NO_HIT\", \n  \"type\": \"no_hit\" \n}")



      if get_args.has_key("n") and get_args['n'][0] != '0':

        # write out n times
        y = []
        try:
          for _ in xrange(0, int(get_args['n'][0])):
            y.append( self.server.parent.stack.pop() )
        except IndexError: pass

        self.wfile.write( y )
      else:
        # write out whole stack
        self.wfile.write( "%s" % dumps(self.server.parent.stack) )
        self.server.parent.stack = []


      





    elif "favicon" not in self.path: # stupid modern browsers
      # bad secret (403 forbidden)
      self.send_error(403, "no secret provided or secret was bad")




  # log stuff
  def log_message(self, format, *args):
    self.server.parent.log( format%args )


  # parse self.path into folder list, and remove get vars
  def parse_path(self):
    path = urllib2.unquote(self.path)
    lastquestion = path.rfind('?')
    if lastquestion != -1:
      path = path[:lastquestion]
    return path.split('/')[1:]





class MyHTTPServer(HTTPServer):
    """this class is necessary to allow passing custom request handler into
       the RequestHandlerClass"""
    def __init__(self, server_address, RequestHandlerClass, parent=None):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.parent = parent


