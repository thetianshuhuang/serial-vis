# minimal code to run serial-vis.

import serial_vis

serial_device = serial_vis.serial_vis(path="/dev/ttyACM0", baudrate=115200)
while(1):
    serial_device.update()
