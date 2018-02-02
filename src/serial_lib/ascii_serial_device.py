# serial_device.py
# serial device interaction class

import serial
from base_serial_device import *


#   --------------------------------
#
#   Serial Device class
#
#   --------------------------------

class ascii_serial_device(base_serial_device):

    """
    ASCII serial device class
    Contains subroutines for reading an ascii-formatted line
    """

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
        if(self.settings.verify > 0):

            (checksum_sent, raw_line[0]) = self.strip_checksum(
                raw_line[0], self.settings.verify)

            checksum_recieved = self.checksum(
                raw_line[0], self.settings.verify)

            # correct checksum -> proceed
            if(checksum_recieved == checksum_sent):
                # provide confirmation if selected
                if(self.settings.confirmation):
                        self.write_raw(b"\xFF")

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
                if(self.settings.confirmation):
                    self.write_raw(b"\xFF")

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
