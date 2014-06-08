
![quail logo](https://cdn.rawgit.com/1egoman/quail/master/logo.svg)
=======


What is This?
---
Basically, the goal is to have an api where a question is asked, and the computer should be able to respond to that question and answer it somewhat reliably.


Wow, that's a huge goal! How do you plan to do this?
---
When a query is sent to the server:
- Parse query
- Determine which plugin that is installed can handle the data
- If a plugin is found, let the plugin deal with that
- Otherwise, send to Wolphram Alpha and hope that an answer is received
- If WA failed, admit defeat...

How do I make this thing come to life?
---
In config.json:
- secret: key needed to make queries. (may work without one, but I wouldn't try)
- port: TCP network port that the server should run on
- color: uses ANSI colors; Windows users should set this to false
- log-file: location of the log file
- wa-key: go to http://products.wolframalpha.com/developers/ and get an api key. Put this here.
- weather-key: go to http://www.wunderground.com/weather/api/ and get an api key. Put this here.

How do I start Quail?
---
First, make sure you've got Python 2.7.x on your system.
- open a terminal, and go to quail's folder
- For debugging and other times where you would want to see Quail's stdout/stderr, run ```./quail.py go```
- In a production environment, Quail can be started as a daemon. (```./quail.py start``, ```./quail.py stop``, ```./quail.py restart``)

Plugins?
---
Yes, plugins. Want to tell your 3D printer to print that model of a cactus from a simple API query? That's what I thought.

#### NOTE: Start a plugin by forking (or cloning) https://github.com/1egoman/qplugin! All the setup work is done for you!

All a plugin minimally has to have is an info.json:
```json
{
  "name": "Plugin Name",
  "desc": "Short Description, maybe a line or so",
  "author": "Your name, contact info",
  "main": "main_file.py:sample_plugin"
}
```

and a main_file.py (named accordingly in info.json):

```python
from base import *
class sample_plugin(parser):
  
  # wether to run the plugin based on the user's query
  def validate(self):
    # the query is available under self.query to test against
    return False
  
  # parse the query if it was validated
  def parse(self, parent): 
    self.resp["text"] = "The Response"
    self.resp["status"] = STATUS_OK
    return self.resp
```

Put both those files in a folder inside the plugins folder, and you've made a small plugin (that does nothing)!
Check out the plugins folder for some better examples, or take a look at https://github.com/1egoman/qplugin
