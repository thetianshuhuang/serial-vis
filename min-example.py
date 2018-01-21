# minimal code to run serial-vis.

from src import serial_vis

serial_device = serial_vis.serial_vis("/dev/lm4f", baudrate=115200)
while(1):
    serial_device.update()
