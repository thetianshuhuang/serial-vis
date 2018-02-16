# serial_device.py
# serial device interaction class

import serial
import time


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

        # message spam limiter
        self.next_time = 0

    #   --------------------------------
    #
    #   search for device connection
    #
    #   --------------------------------
    def connect_device(self):

        """
        Attempt to connect a serial device.

        Returns
        -------
        bool
            Success (True) or failure (False).
        """

        # open serial interface
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

            # return success
            return(True)

        except serial.serialutil.SerialException:
            # limit the error message to once every 2.5 seconds.
            if(self.next_time < time.time()):
                print("Serial device " +
                      self.settings.path +
                      " not found. Trying again.")

                self.next_time = time.time() + 2.5

            # return failure
            return(False)

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
