from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import inspect
import urllib2
import os

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




"""
this class deals with incoming http requests
"""
class http_rest(BaseHTTPRequestHandler):


  def do_GET(self):


    # make sure we have permission
    data = self.parse_path()

    # authentication
    if len(data) and self.server.parent.config.has_key("secret") and data[0] == self.server.parent.config["secret"]:


      # get rid of password in data string
      data = data[1:]

      # make sure some data is there
      if not len(data):
        self.send_error(404, "no query provided")
        return


      # the header
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()


      # start building json string
      response = {}




      # what kind of request?
      if len(data) > 1:

        # a plugin was specified in the url

        # find the correct plugin
        plugin = [  p for p in self.server.parent.plugins if p["name"] == data[0] or (p.has_key("shortname") and p["shortname"] == data[0])  ]
        if len(plugin):
          query = create_query_object( data[1] )
          d, plugin_name = plugin[0], plugin[0]["name"]
          plugin_call = d["call"](query, None)
        else:
          self.send_error(404, "no such plugin can be found")
          return




      else:

        # a plugin wasn't specified in the url

        # parse text for plugin, if requested
        query = create_query_object( data[0] )

        # find correct plugin
        plugin = find_correct_plugin( query, self.server.parent.plugins)
        if plugin:
          plugin_call, plugin_name = plugin[0], plugin[1]["name"]
        else:
          self.send_error(404, "no such plugin can be found")
          return




      # log what we are doing
      self.server.parent.log( "plugin: %s -> %s" % (plugin_name, query) )

      # parse it
      out = plugin_call.parse(parent=self.server.parent)
      if out:
        self.wfile.write( "%s" % out )
      else:
        self.wfile.write( "{\n  \"status\": \"NO_HIT\", \n  \"type\": \"no_hit\" \n}")





    elif "favicon" not in self.path: # stupid modern browsers
      # bad secret (403 forbidden)
      self.send_error(403, "no secret provided or secret was bad")




  # log stuff
  def log_message(self, format, *args):
    self.server.parent.log( format%args )


  # parse self.path into folder list
  def parse_path(self):
    return urllib2.unquote(self.path).split('/')[1:]





class MyHTTPServer(HTTPServer):
    """this class is necessary to allow passing custom request handler into
       the RequestHandlerClass"""
    def __init__(self, server_address, RequestHandlerClass, parent=None):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.parent = parent









