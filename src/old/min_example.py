# minimum usable example
# configured for a Stellaris Launchpad (TM4C or LM4F) at 115200 baud
from serial_vis.py import *

my_serial_device = serial_device("/dev/lm4f",115200)

while(1):
	my_serial_device.update()
