# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import pyb
import sys

sys.path.extend(['/sd', '/sd/lib'])

#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse
