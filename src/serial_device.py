# serial_device.py
# serial device interaction class

import serial
from time import sleep


#   --------------------------------
#
#   Serial Device class
#
#   --------------------------------

class serial_device:

    """
    Serial Device class; governs serial interactions

    Attributes:
    settings : dict
        settings for serial communication.

    Created by __init__:
    device : serial.Serial object
        Serial device object
    """

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
    def __init__(self, path, **kwargs):

        """
        Initialize serial device.

        Parameters
        ----------
        path : str
            filepath of the desired serial device
        kwargs : dict
            merged with settings
        """

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

                # read one line to avoid passing incomplete lines
                self.discard_line()

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
    #   get serial output
    #
    #   --------------------------------
    def get_line(self):

        """
        Get one line of serial data

        Returns
        -------
        [str, bool]
            [line read from serial, True if successful]
        """

        try:
            return([self.device.readline().strip(), True])
        except (OSError, serial.serialutil.SerialException):
            print("Device disconnected.")
            return(["", False])

    #   --------------------------------
    #
    #   close serial port cleanly
    #
    #   --------------------------------
    def close(self):

        """
        Close the serial port cleanly
        """

        self.device.close()

    #   --------------------------------
    #
    #   discard one line to avoid incomplete reading
    #
    #   --------------------------------
    def discard_line(self):

        """
        Read a line, and discard it in case a partial line is stored
        """

        self.device.readline().strip()

    #   --------------------------------
    #
    #   write to serial
    #
    #   --------------------------------
    def write(self, line):

        """
        Write a line to serial.

        Parameters
        ----------
        line : str
            line to be written; must have its own newline character if needed
        """

        self.device.write(line.encode(self.settings["encoding"]))
