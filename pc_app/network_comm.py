# client code
from twisted.internet import defer
import json,uuid,pdb
from kivy.clock import Clock
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
class StrokeClient(WebSocketClientProtocol):
# connection made handler-used to register username for protocol at the server's end
    def onConnect(self):
        
        print "Connected to white via android device server"

# processes the string received and assigns the data to the apt handle
    def onMessage(self, string):
        payload=json.loads(string)
        print payload

class StrokeClientFactory(WebSocketClientFactory):
    protocol = StrokeClient
    def __init__(self, canvas_obj, username,reactor):
        self.canvas_obj = canvas_obj
        self.username = username
        self.reactor=reactor
        super(StrokeClientFactory, self).__init__()    
