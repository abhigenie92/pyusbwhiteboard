# delete the hook by twisted to import it
import sys
try:
    del sys.modules['twisted.internet.reactor'] 
except:
    pass

# reactor import (compulsory first import)
'''from kivy.support import install_twisted_reactor
install_twisted_reactor() # twisted eventloop with kivy on the same reactor
'''
# kivy import
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen

# twisted and other-control imports
from twisted.internet import reactor

# screen imports
from main_screen import MainScreen
from connected_screen import ConnectedScreen

class ConnectionDetails:
	'''contains the connection details'''
	def __init__(self):
		self.ip_addr='' # ip address of the connected pc 
		self.port_no='' # port number of the connected pc
        
class AppScreenManager(ScreenManager):
    '''ScreenManager class'''

class whiteboard(App):
    '''Base application class'''
    def build(self):
        self.reactor=reactor
        self.connection_details=ConnectionDetails()
        return Builder.load_file('style.kv')

if __name__ == '__main__':
    #Config.set('graphics', 'height', '540')  # 16:9
    # disabling multi-touch and resizing the app
    whiteboard().run()