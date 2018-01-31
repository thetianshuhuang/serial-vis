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
        "path": "",
        "baudrate": 115200,
        "seek_timeout": 60,
        "rx_timeout": 0.1,
        "tx_timeout": 0.1,
        "encoding": "ascii",
        "verify": 2,
        "confirmation": True,
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
        # path is forcibly updated separately
        self.settings.update(kwargs)
        self.settings.update({"path": path})

        # set up error handling
        self.error_handler = error_handler(**kwargs)

        counter = 0
        timeout = False
        # open serial interface
        while(not timeout):

            try:
                self.device = serial.Serial(
                    path,
                    self.settings["baudrate"],
                    timeout=self.settings["rx_timeout"],
                    writeTimeout=self.settings["tx_timeout"])
                print("Device connected: " + path + "\n\n")

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
            if(counter >= self.settings["seek_timeout"] * 4):
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

        # while loop to reject empty lines
        raw_line = ["", False]
        while(raw_line[0] == ""):
            # get line
            try:
                raw_line = [self.device.readline().strip(), True]
            except (OSError, serial.serialutil.SerialException):
                print("Device disconnected.")
                return(["", False])

        # verify checksum:
        if(self.settings["verify"] > 0):

            (checksum_sent, raw_line[0]) = self.strip_checksum(
                raw_line[0], self.settings["verify"])

            checksum_recieved = self.checksum(
                raw_line[0], self.settings["verify"])

            # correct checksum -> proceed
            if(checksum_recieved == checksum_sent):
                # provide confirmation if selected
                if(self.settings["confirmation"]):
                        self.write(b"\xFF")

                return(raw_line)

            # incorrect checksum
            else:
                # raise error
                self.error_handler.raise_error(
                    "chk",
                    raw_line,
                    "sent=" + hex(checksum_sent) +
                    " recieved=" + hex(checksum_recieved))

                # provide confirmation if selected
                if(self.settings["confirmation"]):
                    self.write(b"\xFF")

                # return null instruction
                return(["null", True])

        # don't verify checksum
        else:
            return(raw_line)

    #   --------------------------------
    #
    #   calculate checksum
    #
    #   --------------------------------
    def checksum(self, string, size):

        """
        Get a checksum with 4*size bits of string.

        Arguments
        ---------
        string: str
            String to calculate the checksum for
        size: int
            1/4 number of bits of the output

        Returns
        -------
        int
            last 4*size bits of the checksum
        """

        output = 0
        for char in string:
            output += ord(char)
            output &= int("F" * size, 16)
        return(output)

    #   --------------------------------
    #
    #   strip checksum from the end of a string
    #
    #   --------------------------------
    def strip_checksum(self, string, size):

        """
        Strip the last size characters from a string and interpret them as a
        checksum.

        Arguments
        ---------
        string: str
            input string
        size: int
            number of characters stripped off the end

        Returns
        -------
        [int, str]
            checksum converted to int, string with checksum stripped off
        """

        output = -1
        if(len(string) >= size):
            # build checksum
            checksum = string[-size:]
            try:
                output = int(checksum, 16)
            except ValueError:
                output = -1

        # remove checksum once done
        string = string[:-size]

        return((output, string))

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

        try:
            self.device.write(line.encode(self.settings["encoding"]))
        # line isn't ascii, then send the bits directly
        except UnicodeDecodeError:
            try:
                self.device.write(line)
            # read buffer is full
            except serial.serialutil.SerialTimeoutException:
                self.error_handler.raise_error(
                    "wto", [], self.settings["path"])
