import sys,pdb
import usb.core
import usb.util
from pymouse import PyMouse

# white coordinates axis computed by checking the output against strokes
white_board_x_min=(1<<8)+1
white_board_x_max=(127<<8)+255
white_board_y_min=(1<<8)+1
white_board_y_max=(127<<8)+255

white_board_x_diff=white_board_x_max-white_board_x_min
white_board_y_diff=white_board_y_max-white_board_y_min

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
while True :
    try:
        data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        # click value
        click=data[1] # if it is 7 mouse down else if it is 4 it is mouse up 
        # get the coordinates
        xcor,ycor,dec_x_binary,dec_y_binary=data[4],data[6],data[3],data[5]
        # convert to decimal
        xcor_dec=(xcor<<8)+dec_x_binary
        ycor_dec=(ycor<<8)+dec_y_binary
        # convert to relative screen coordinates
        screen_xcor=int(round((float(xcor_dec-white_board_x_min)/float(white_board_x_diff)) * x_screen))
        screen_ycor=int(round((float(ycor_dec-white_board_y_min)/float(white_board_y_diff)) * y_screen))
        print "%d, %d"%(xcor_dec,ycor_dec)
        print "%d, %d"%(screen_xcor,screen_ycor)
        # move mouse
        if xcor_dec!=0 and ycor_dec!=0:
          pass
          #m.click(screen_xcor, screen_ycor, 1)
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue  
# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
dev.attach_kernel_driver(interface)
