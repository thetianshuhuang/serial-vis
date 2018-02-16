# serial_device.py
# serial device interaction class

import serial
from time import sleep


#   --------------------------------
#
#   Serial Device class
#
#   --------------------------------

class base_device:

    """
    Base Serial Device class; governs serial interactions

    Attributes
    ----------

    Created by __init__:
    device : serial.Serial object
        Serial device object
    """

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, settings, error_handler):

        """
        Initialize serial device.

        Parameters
        ----------
        path : str
            filepath of the desired serial device
        settings : sv_settings object
            Object containing program settings
        """

        # update settings
        self.settings = settings

        # set up error handling
        self.error_handler = error_handler

        counter = 0
        timeout = False
        # open serial interface
        while(not timeout):

            try:
                # initialize device
                self.device = serial.Serial(
                    self.settings.path,
                    self.settings.baudrate,
                    timeout=self.settings.rx_timeout,
                    writeTimeout=self.settings.tx_timeout)
                print("Device connected: " + self.settings.path + "\n")

                # flush potentially incomplete commands from buffer
                self.device.flushInput()

                break

            except serial.serialutil.SerialException:
                # limit the error message to once every 2.5 seconds.
                if(counter % 10 == 0):
                    print("Serial device " +
                          self.settings.path +
                          " not found. Trying again.")

            # wait 250ms before trying again to avoid spamming the system
            sleep(0.25)
            counter += 1

            # trigger timeout. Default is 60 seconds (300 attempts).
            if(counter >= self.settings.seek_timeout * 4):
                timeout = True
                print("Operation timed out.")

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

        try:
            self.write_raw(line.encode(self.settings.encoding))
        except UnicodeDecodeError:
            self.error_handler.raise_error("nas", [], line)

    #   --------------------------------
    #
    #   write pre-formatted string to serial
    #
    #   --------------------------------
    def write_raw(self, line):

        """
        Write a byte array (already formatted) to serial.

        Parameters
        ----------
        line : str / byte[]
            line to be written; must be encoded.
        """

        try:
            self.device.write(line)
        except serial.serialutil.SerialTimeoutException:
            self.error_handler.raise_error(
                "wto", [], self.settings.path)
