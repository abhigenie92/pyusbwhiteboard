# start a twisted server
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


# print public address, port
from urllib2 import urlopen
ip_addr = urlopen('http://ip.42.pl/raw').read()
print "Public address is",ip_addr
print "Port number is",ip_addr
# mouse the click and drag 


