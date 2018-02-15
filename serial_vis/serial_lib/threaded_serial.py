# threaded_serial.py
# asynchronous serial handling

import threading
from ascii_device import ascii_device
from ascii_parser import ascii_parser
from bin_device import bin_device
from bin_parser import bin_parser


class threaded_serial(threading.Thread):

    """
    Multi-threaded serial parser

    Attributes
    ----------
    exit request : bool
        Serial device requests a system exit
    Created by __init__:
    settings : settings
        Settings object
    running : bool
        Must be set to True once every cycle, or the thread terminates
    instruction_buffer : array
        Buffer containing recieved instructionsxs
    """

    exit_request = False

    def __init__(self, settings):

        """
        Create a serial parser instance

        Parameters
        ----------
        settings
            settings object
        """

        # set settings
        self.settings = settings

        # exitflag
        self.running = True

        # instruction buffer
        self.instruction_buffer = []

        # create serial device and parser:

        # ascii transmission mode
        # slower, but more human-readable
        if(self.settings.serial_mode == "ascii"):
            self.serial_device = ascii_device(
                self.settings, self.error_handler)
            self.serial_parser = ascii_parser(
                self.user_commands, self.settings, self.error_handler)

        # binary transmission mode
        # 0% human readable
        elif(self.settings.serial_mode == "bin"):
            self.serial_device = bin_device(
                self.settings, self.error_handler)
            self.serial_parser = bin_parser(
                self.user_commands, self.settings, self.error_handler)

    def run(self):

        """
        Run the asynchronous serial device
        Requires for self.running to be set to True every cycle,
        or the thread with self-terminate.

        Fetch instructions by retrieving instructions from instruction_buffer,
        and clearing it periodically.
        """

        while(self.running):

            # reset running flag; must be set to True before this loop ends
            self.running = False

            # get line
            line = self.serial_device.get_line()

            # parse instruction
            instruction = self.serial_parser.process_command(line[0])
            self.intruction_buffer.append(instruction)

            if(not line[1]):
                self.exit_request = False
