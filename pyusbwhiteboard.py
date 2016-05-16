import sys,pdb
import usb.core
import usb.util
from pymouse import PyMouse
import sys, pygame
pygame.init()
from pygame_calib import PygameCalib
import time
# flage to determine if calibration has to be done
board_calib=True

# whiteboard coordinates axis computed by checking the output against strokes
white_board_x_min=(1<<8)+1
white_board_x_max=(127<<8)+255
white_board_y_min=(1<<8)+1
white_board_y_max=(127<<8)+255

white_board_x_diff=white_board_x_max-white_board_x_min
white_board_y_diff=white_board_y_max-white_board_y_min

# intialize offsets to zero, will change later after calbiration
offset_x,offset_y=0,0

def transform_board_screen(xcor,ycor,dec_x_binary,dec_y_binary):
	''' transforms board coordinateas to screen coordinates'''
	# convert to decimal
	xcor_dec=(xcor<<8)+dec_x_binary
	ycor_dec=(ycor<<8)+dec_y_binary
	print xcor,ycor
	# convert to relative screen coordinates
	screen_xcor=int(round((float(xcor_dec-white_board_x_min)/float(white_board_x_diff)) * x_screen))
	screen_ycor=int(round((float(ycor_dec-white_board_y_min)/float(white_board_y_diff)) * y_screen))
	# add the offset
	screen_xcor=screen_xcor+offset_x
	screen_ycor=screen_ycor+offset_y
	return screen_xcor,screen_ycor

# mouse handler
m = PyMouse()
x_screen, y_screen = m.screen_size()

# decimal vendor and product values
dev = usb.core.find(idVendor=17955, idProduct=282)

# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]
# if the OS kernel already claimed the device, which is most likely true
# thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
if dev.is_kernel_driver_active(interface) is True:
	# tell the kernel to detach
	dev.detach_kernel_driver(interface)
	# claim the device
	usb.util.claim_interface(dev, interface)
mouse_down_event=False

# board calibration code
if board_calib:
	print "Started Board Calibration"
	pygame_obj=PygameCalib((x_screen,y_screen))
	offset_x_list=[]
	offset_y_list=[]
	for i in range(4):
		pygame_obj.set_display_title('Touch the red dot'+str(i))
		coordinates_circle=pygame_obj.draw()
		data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize,1000*500)
		xcor,ycor,dec_x_binary,dec_y_binary=data[4],data[6],data[3],data[5]
		screen_xcor,screen_ycor=transform_board_screen(xcor,ycor,dec_x_binary,dec_y_binary)
		# determine offsets for this click
		x_iter_off=coordinates_circle[0]-screen_xcor
		y_iter_off=coordinates_circle[1]-screen_ycor
		offset_x_list.append(x_iter_off)
		offset_y_list.append(y_iter_off)
		# clears the screen and waits for 5 seconds
		pygame_obj.clear_screen()
		pygame_obj.set_display_title("Done")
		time.sleep(1)
		
	offset_x=sum(offset_x_list) / len(offset_x_list)
	offset_y=sum(offset_y_list) / len(offset_y_list)
	pygame_obj.quit()
	print "Finished Board Calibration"
sub
# normal movement code
try:	
	while True :
		try:
			data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
			# click value
			click=data[1] # if it is 7 mouse down else if it is 4 it is mouse up 
			# get the coordinates
			xcor,ycor,dec_x_binary,dec_y_binary=data[4],data[6],data[3],data[5]
			screen_xcor,screen_ycor=transform_board_screen(xcor,ycor,dec_x_binary,dec_y_binary)
			#print "%d, %d"%(xcor_dec,ycor_dec)
			#print "%d, %d"%(screen_xcor,screen_ycor)
			# check if it is valid event
			if xcor!=0 and ycor!=0:
				# move mouse	
				if click==7:
					# mean mouse down event
					if mouse_down_event:
						# drag event
						# draw a line from previous coordinates
						m.drag(screen_xcor, screen_ycor)
					else:
						# first button press event
						m.click(screen_xcor, screen_ycor, 1)
					mouse_down_event=True
				else:
					# mouse up event
					# set event type in mouse_down_event
					# first button press and drag
					mouse_down_event=False
		except usb.core.USBError as e:
			data = None
			if e.args == ('Operation timed out',):
				continue  
finally:
	# release the device
	usb.util.release_interface(dev, interface)
	# reattach the device to the OS kernel
	dev.attach_kernel_driver(interface)
