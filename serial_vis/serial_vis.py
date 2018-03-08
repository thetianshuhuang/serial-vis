# serial_vis.py
# main class

import pygame
import serial_lib
import graphics_lib
import buffer_lib
import util_lib
from sv_command import *


#   --------------------------------
#
#   Main Serial-Vis Class
#
#   --------------------------------
class serial_vis(sv_command):

    """
    Main serial vis class; extend this class to use its API.

    Attributes
    ----------
    user_settings : dict
        Settings defined by the user. Empty; is overwritten by user extensions.
    user_commands : dict
        Commands defined by the user. Empty; is overwritten by user extensions.
    graphics_class : class
        Is set to default_vector_graphics by default; overwrite this in
        extensions to add custom graphics commands.
    command_mode : bool
        Whether the program is currently in command mode or normal input mode
        All key inputs are directed to the command line in command mode.
    connect_device : bool
        Is set to False if no device is connected, and no device connection
        attempts should be made.

    Created by __init__:
    serial_device : threaded serial device object
        Combines a serial device and parser into a secondary thread.
    csv_log : csv_log object
        CSV log object
    error_handler : error handler object
        Hosts centralized error handling
    graphics_window : graphics_class
        Vector graphics class to be used
    buffer_db : buffer_db object
        Frame buffer storage and tracking
    """

    user_settings = {}
    user_commands = {}
    graphics_class = graphics_lib.default_vector_graphics
    command_mode = False
    connect_device = True

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        """
        Create a master serial_vis object

        Parameters
        ----------
        path : str
            Filepath to be passed on to serial_device
        kwargs : dict
            Sent to settings object
        """

        # update settings
        self.settings = {"main": util_lib.sv_settings()}
        self.settings["main"].update(self.user_settings)
        self.settings["main"].update(kwargs)

        # set up centralized error handling
        self.error_handler = util_lib.error_handler(self.settings["main"])

        # create log
        self.csv_log = util_lib.csv_log(self.settings["main"])

        # disable device connection if a blank path is specified.
        if(self.settings["main"].path == ""):
            self.connect_device = False

        # create threaded serial handler for the main instance
        if(self.connect_device):
            self.serial_device = serial_lib.threaded_serial(
                self.settings["main"],
                self.error_handler,
                self.user_commands)
            self.serial_device.start()

        # create graphics window using main settings
        self.graphics_window = self.graphics_class(
            self.settings, self.error_handler)

        # initialize buffer manager
        self.buffer_manager = buffer_lib.buffer_manager(
            self.settings["main"], self.error_handler)

    #   --------------------------------
    #
    #   execute program update
    #
    #   --------------------------------
    def update(self):

        """
        Execute master program update.
        """

        # process keyboard/mouse commands
        if(self.command_mode):
            line = self.command_line.update()
            if(line[0]):
                self.command_mode = False
                self.process_command(line[1])
            command_line = self.command_line.get_text_object()
        else:
            command_line = pygame.Surface((0, 0))
            self.process_events(self.graphics_window.check_events())

        # fetch serial device output if enabled
        if(self.connect_device):
            self.service_device()

        # update buffer
        self.graphics_window.update_screen(
            self.buffer_manager.get_buffer(),
            self.command_mode,
            command_line)

    #   --------------------------------
    #
    #   service serial device
    #
    #   --------------------------------
    def service_device(self):

        """
        Service the serial device thread
        """

        # check for exit request
        if(self.serial_device.exit_request):
            if(self.settings["main"].quit_on_disconnect):
                self.quit_sv()
            else:
                self.connect_device = False
                self.serial_device.done = True

        # acquire thread lock ---------------------------------------------
        self.serial_device.lock.acquire()

        # fetch instruction if it exists
        while(len(self.serial_device.instruction_buffer) > 0):
            instruction = self.serial_device.instruction_buffer.pop(0)

            # log command with window fps tracker
            self.graphics_window.update_fps(instruction)

            # log instructions
            if(instruction[0] in ["logs", "logf", "logstart", "logend"]):
                self.csv_log.log_data(instruction)

            # print instruction
            elif(instruction[0] == "echo"):
                print(instruction[1])

            # null instruction
            elif(instruction[0] == "null" or len(instruction) == 0):
                pass

            # process draw-related instructions
            else:
                self.buffer_manager.update(instruction)

        self.serial_device.lock.release()
        # release lock ----------------------------------------------------

    #   --------------------------------
    #
    #   quit
    #
    #   --------------------------------
    def quit_sv(self):

        """
        Cleanly quit all sub-objects.
        """

        # print message

        print("\nClosing serial-vis ... \n")

        # call clean close methods
        self.graphics_window.close_window()
        self.csv_log.close_file()
        self.serial_device.done = True

        exit()


#   --------------------------------
#
#   Default run parameters
#
#   --------------------------------
if __name__ == "__main__":
    serial_device = serial_vis(path="/dev/ttyACM0", baudrate=115200)
    while(1):
        serial_device.update()
