![quail logo](https://cdn.rawgit.com/1egoman/quail/83cab06d22c9e30a714e58a978d65d8e4f9d7b45/logo.svg)



Minimal Plugin
===

A minimal plugin generally looks like this:

info.json:
```json
{
  "name": "Plugin Name, Capitalized",
  "desc": "short description of the plugin, maybe a line or so",
  "author": "your name, contact info",
  "main": "main_file.py:sample_parser"
}
```

main_file.py (named accordingly in info.json):
```python
from base import *
class sample_parser(Parser):
  
  def validate(self):
    return "phrase" in self.query
  
  def parse(self): 
    self.resp["text"] = "hello, world"
    self.resp["status"] = STATUS_OK
```

These 2 files (info.json and main_file.py) need to go inside of a folder inside of Quail's plugins folder:
```
- plugins
  - my_plugin_folder
    - info.json
    - main_file.py
  - other plugins...
```
Now, start the server with `$ ./go.sh` and try out your new plugin:
```
$ curl 127.0.0.1:8000/abc/sample
[{"status": "OK", "text": "hello, world", "type": "static", "files": [], "packet": "response"}]
```

What did that do?
---
1. First, we wrote the info.json file to tell Quail some metadata. **Most importantly**, this also tells quail where to look for the plugin class.
2. Next, we created a new plugin that subclasses `base.Parser`. This class will incorporate much of the core functionality of the plugin.
3. We then told the plugin to only respond to queries containing the word 'sample' in the `validate()` function.
4. Finally, the parse function will resond to queries by saying 'hello, world'.



Listeners
===

Normally, communication in Quail goes from client to server, only. Listeners allow the server to do the reverse, and send messages back to the client. In Quail, all packets that are being sent out are appended to the end of a list. If a packet is appended to the stack, it will be sent the next time any client connects. A normal query will return the stack, and empty it. If, for example, you wanted only the last packet on the stack (the one you requested with the query), you could specify the ```n``` GET variable with a value of 1. A value of zero is the default and means to send the whole stack.

Setting up a Listener
---

1. In the plugin's info.json, add
```json
"listener": "example.py:exampleListener"
```
in the same format as the ```main``` parameter. Then, create the listener method:
```python
def exampleListener(parent):
  """ example listener """
  pass
```

Sending messages with a Listener
---

```python
def exampleListener(parent):
  """ example listener """

  # send packet to client
  msg = {"status": STATUS_OK, "type": TYPE_PUSH, "text": "test response"}
  parent.stack.append(msg)
```

For any message that is to be sent to the client, the type should be `base.TYPE_PUSH`. Don't clutter the stack with lots of packets!


<br/><br/>
Class Definitions
===

- `base.Parser`
  - `query`: This list contains the query that the plugin should parse. This value is often just a list of the plugin's words, but can also contain other metadata, such as dates or times. Example: `["will", "it", "rain", {"when": [2014, 1, 1, 0, 0, 0], "text": "tommorow"}]`
  - `resp`: This `base.Packet` object is the final result send to the user. 
  - `info`: The json-parsed contents of your info.json.
  - `addr`: Tuple containing ip and port of client.
  - `validate()`: This function should return a true value if the plugin is equipped to handle the query. If the plugin cannot handle the query, return a false value.
  - `parse()`: Parse the query and compute a response. The response and all its relevent information should be put into `resp`.

- `base.Packet`

  ###Required Parameters:
  - `["status"]`: The plugin's status.
    - `base.STATUS_OK` for success
    - `base.STATUS_NO_HIT` if the plugin cannot find it's target (failed search?)
    - `base.STATUS_ERR` for a general error. 
      
  - `["text"]`: This is a textual representation of whatever other data is sent in the packet. The default is 'No Response.', but in most cases should be changed to something else. Some clients will only look at this and nothing else in the packet.

  ###Optional, but highly recommended:
  - `["type"]`: A unique identifier that allows the client (and the server) to determine what plugin responded to which queries.
  - `["return"]`: A list containing each phrase of the response as an element of the list. 

  ###Others:
  - `["color"]`: A color or color shade that matches a query. Can be specified as `[r, g, b]` or `blue`

  ###Files
  A packet can contain attached files. These are added by calling `add_file(path)`, subsituting in a path to the file.
