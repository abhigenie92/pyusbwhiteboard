import random, sys, pygame
from pygame.locals import *

class PygameCalib:
	"""docstring for ClassName"""
	def __init__(self,screen_size):
		#intiate a pygame object
		pygame.init()
		self.xlim,self.ylim=screen_size[0],screen_size[1]
		self.screen=pygame.display.set_mode(screen_size)
		self.black=(0,0,0)
		self.red=(255,0,0)

	def draw(self):
		# clear screen 
		self.screen.fill(self.black)
		# set a random location on screen
		coordinates_circle=random.randint(50,self.xlim-50),random.randint(50,self.ylim-50)
		pygame.draw.circle(self.screen,self.red,coordinates_circle,5,0)
		pygame.display.set_caption('Touch the red dot')
		pygame.display.update()
		return coordinates_circle

	def clear_screen(self):
		self.screen.fill(self.black)

	def set_display_title(self,string):
		pygame.display.set_caption(string)

	def quit(self):
		pygame.display.quit()

if __name__ == '__main__':
	from pymouse import PyMouse
	import time
	m = PyMouse()
	x_screen, y_screen = m.screen_size()
	pygame_obj=PygameCalib((x_screen,y_screen))
	for i in range(5):
		coordinates_circle=pygame_obj.draw()
		print coordinates_circle
		time.sleep(1)




