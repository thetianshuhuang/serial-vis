# serial_device.py
# serial device interaction class

import serial
from time import sleep
from error_handler import *


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
        "encoding": "ascii",
        "verify": 2
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

        # set up error handling
        self.error_handler = error_handler(**kwargs)

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

        # get line
        try:
            raw_line = [self.device.readline().strip(), True]
        except (OSError, serial.serialutil.SerialException):
            print("Device disconnected.")
            return(["", False])

        # verify checksum:

        # compute sent checksum
        # generalized for arbitrary verify size
        checksum_sent = -1
        if(len(raw_line[0]) >= self.settings["verify"]):

            # build checksum
            checksum = raw_line[0][-self.settings["verify"]:]
            try:
                checksum_sent = int(checksum, 16)
            except ValueError:
                checksum_sent = -1

            # remove checksum once done
            raw_line[0] = raw_line[0][:-self.settings["verify"]]

        # compute recieved checksum
        checksum_recieved = 0
        for char in raw_line[0]:
            checksum_recieved += ord(char)
            checksum_recieved &= 0xFF

        # correct checksum -> proceed
        if(checksum_recieved == checksum_sent):
            return(raw_line)
        # incorrect checksum -> raise error, turn line into a null instruction
        else:
            print("---------")
            print(checksum_sent)
            print(checksum_recieved)
            self.error_handler.raise_error("chk", raw_line)
            return(["null", True])

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
