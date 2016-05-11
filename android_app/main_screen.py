from kivy.uix.screenmanager import Screen
import pdb,requests
from kivy.app import App

class MainScreen(Screen):
    def __init__(self,**kwargs):
        super(MainScreen, self).__init__(**kwargs)
    def connect(self,*args):
    	# set the details
    	App.get_running_app().connection_details.ip_addr=self.ids["ip_addr"].text
    	App.get_running_app().connection_details.port_no=self.ids["port_no"].text
    	# change screen
        self.parent.current = 'ConnectedScreen'
        self.manager.get_screen('ConnectedScreen').start_server()
