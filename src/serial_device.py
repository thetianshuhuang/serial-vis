# serial_device.py
# serial device interaction class

import serial
from time import sleep


# class governing serial interaction

# methods:
# __init__              - takes filepath and **kwargs containing
#                       - baudrate= sets baudrate
#                       - timeout= sets initial timeout for device detection
#                       - encoding= serial encoding ("ascii" or "utf-8")
# get_line              - gets line from serial output and strips newline
# close                 - cleanly close serial interface
# write                 - write string to serial interface
class serial_device:

    #   --------------------------------
    #
    #   Attributes (default)
    #
    #   --------------------------------
    settings = {
        "baudrate": 115200,
        "timeout": 60,
        "encoding": "ascii"
    }

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------

    #   Find serial device.
    def __init__(self, path, **kwargs):

        # update settings
        self.settings.update(kwargs)

        counter = 0
        timeout = False
        # open serial interface
        while(not timeout):

            try:
                self.device = serial.Serial(
                    path, self.settings["baudrate"], timeout=1)
                print("Device connected: " + path)
                break

            except serial.serialutil.SerialException:
                # limit the error message to once every 2.5 seconds.
                if(counter % 10 == 0):
                    print("Serial device " +
                          path +
                          " not found. Trying again.")

            # wait 250ms before trying again to avoid spamming the system
            sleep(0.25)
            counter += 1

            # trigger timeout. Default is 60 seconds (300 attempts).
            if(counter >= self.settings["timeout"] * 4):
                timeout = True
                print("Operation timed out.")

    #   --------------------------------
    #
    #   get launchpad uart output
    #
    #   --------------------------------
    def get_line(self):
        return(self.device.readline().strip())

    #   --------------------------------
    #
    #   close serial port cleanly
    #
    #   --------------------------------
    def close(self):
        self.device.close()

    #   --------------------------------
    #
    #   write to serial
    #
    #   --------------------------------
    def write(self, line):
        self.device.write(line.encode(self.settings["encoding"]))
