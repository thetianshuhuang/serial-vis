# serial_device.py
# serial device interaction class

import time
import serial
from .base_device import *


#   --------------------------------
#
#   Serial Device class
#
#   --------------------------------

class bin_device(base_device):

    """
    Binary serial device class
    Contains subroutines for reading a raw byte instruction array
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

        timeout_time = time.time() + self.settings.rx_timeout
        outarray = ""

        # wait for start character
        # return null instruction if no character given
        while(Serial.read(1) != b"\xFF"):
            if(timeout_time < time.time()):
                return("null", True)

        # get opcode
        outarray.append(Serial.read(1))

        # control information for the main loop
        current_size = 0
        eot = False

        in_string = False
        current_string = ""

        in_tuple = False
        current_tuple = []

        # set timeout
        timeout_time = time.time() + 1000 * self.settings.rx_timeout
        while(timeout_time > time.time() and not eot):

            # previous term depleted
            if(current_size == 0 and not in_string):

                # append to tuple or main array
                if(in_tuple):
                    current_tuple.append(current_string)
                else:
                    outarray.append(current_string)

                current_string = ""
                next_size = Serial.read(1)

                # enter string mode
                if(next_size == b"\x00"):
                    in_string = True
                # EOT character recieved
                elif(next_size == b"\xFF"):
                    eot = True
                # end of tuple mode
                elif(next_size == b"\xFE" and in_tuple):
                    in_tuple = False
                    outarray.append(current_tuple)
                # start of tuple mode
                elif(next_size == b"\xFE" and not in_tuple):
                    in_tuple = True
                # normal term entered
                else:
                    current_size += ord(next_size)

            # term not finished
            else:
                next_char = Serial.read(1)

                # currently in string block, and null termination is recieved
                if(in_string and next_char == b"\x00"):
                    outarray.append(current_string)
                    current_string = ""
                    in_string = False
                # normal char or element
                else:
                    current_string += next_char

                # decrement current size
                current_size -= 1

            # reset timeout
            timeout_time = time.time() + self.settings.rx_timeout * 1000
