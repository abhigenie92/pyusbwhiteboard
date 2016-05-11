# client code
from twisted.internet import defer
import json,uuid,pdb
from kivy.clock import Clock
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
class StrokeClient(WebSocketClientProtocol):
# connection made handler-used to register username for protocol at the server's end
    def onConnect(self):
        print "Connected to stroke remote server"

# server-code
    def send_request_to_allow(self,stroke,audio):
        ''' sends a request to the server allow this connection to send data'''
        self.sendMessage(json.dumps(payload))


class StrokeClientFactory(WebSocketClientFactory):
    protocol = StrokeClient
    def __init__(self):
        super(StrokeClientFactory, self).__init__()    