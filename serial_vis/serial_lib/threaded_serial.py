# threaded_serial.py
# asynchronous serial handling

import threading
import time
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
    instruction_buffer : array
        Buffer containing recieved instructions
    device_connected : bool
        Tracks whether a device is currently connected

    Created by __init__:
    serial_device : serial device object
        Serial device; either ascii_serial_device or bin_serial_device
    serial_parser : serial parser object
        Serial parser; either ascii_serial_parser or bin_serial_parser
    settings : settings
        Settings object
    done : bool
        Exits main loop if set to True
    lock : threading.Lock
        Threading lock for accessing the main queue
    """

    exit_request = False
    instruction_buffer = []
    device_connected = False

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, settings, error_handler, user_commands):

        """
        Create a serial parser instance

        Parameters
        ----------
        settings
            settings object
        """

        # initialize thread
        threading.Thread.__init__(self)

        # set settings
        self.settings = settings
        self.user_commands = user_commands

        # set error handler
        self.error_handler = error_handler

        # thread utility
        self.lock = threading.Lock()
        self.done = False

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

    #   --------------------------------
    #
    #   Run thread (called by threading module)
    #
    #   --------------------------------
    def run(self):

        """
        Run the asynchronous serial device
        Requires for self.running to increment the timeout every cycle,
        or the thread with self-terminate.

        Fetch instructions by retrieving instructions from instruction_buffer,
        and clearing it periodically.
        """

        timeout = time.time() + self.settings.seek_timeout

        # main loop
        # runs when not done, and main thread is alive
        while(not self.done and self.main_alive()):

            # no device connected; attempt to establish connection
            if(not self.device_connected):
                self.device_connected = self.serial_device.connect_device()

                # wait 100ms before trying again to avoid spamming the system
                time.sleep(0.1)

                # trigger timeout. Default is 60 seconds.
                if(time.time() > timeout):
                    self.error_handler.raise_error(
                        "cto", [], self.settings.path)
                    self.exit_request = True
                    self.done = True

            # device is connected
            else:
                # get line
                line = self.serial_device.get_line()

                # parse instruction
                instruction = self.serial_parser.process_command(line[0])

                self.lock.acquire()
                try:
                    self.instruction_buffer.append(instruction)
                finally:
                    self.lock.release()

                # exit request passed by the serial device; pass it on
                if(not line[1]):
                    self.exit_request = True

        self.serial_device.close()

    #   --------------------------------
    #
    #   Check if main thread is alive
    #
    #   --------------------------------
    def main_alive(self):

        """
        Check if the main thread is alive. Should be used by all threads.

        Returns
        -------
        bool
            True if the main thread is alive; False otherwise
        """

        # search for main thread is_alive state
        for thread in threading.enumerate():
            if(thread.name == "MainThread"):
                return(thread.is_alive())

        # return not alive if the main thread can't be found
        return(False)
