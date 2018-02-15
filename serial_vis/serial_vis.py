# serial_vis.py
# main class

import time
import pygame
import serial_lib
import graphics_lib
import util_lib


#   --------------------------------
#
#   Main Serial-Vis Class
#
#   --------------------------------
class serial_vis:

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
    is_live : bool
        Track whether the current view is live
    display_buffer_id : int
        Current buffer being displayed, relative to the current view

    Created by __init__:
    serial_device : serial_device object
        Serial interface object.
    serial_parser : serial_parser object
        Serial command parser object.
    csv_log : csv_log object
        CSV log object
    graphics_window : graphics_class
        Vector graphics class to be used
    buffer_db : buffer_db object
        Frame buffer storage and tracking
    """

    user_settings = {}
    user_commands = {}
    graphics_class = graphics_lib.default_vector_graphics
    command_mode = False

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
        self.settings = util_lib.sv_settings()
        self.settings.update(self.user_settings)
        self.settings.update(kwargs)

        # set up centralized error handling
        self.error_handler = util_lib.error_handler(self.settings)

        # create log
        self.csv_log = util_lib.csv_log(self.settings)

        # create threaded serial handler
        self.serial_device = serial_lib.threaded_serial(
            self.settings,
            self.error_handler,
            self.user_commands)
        self.serial_device.start()

        # create graphics window
        if(self.settings.enable_graphics):
            self.graphics_window = self.graphics_class(
                self.settings, self.error_handler)

        # initialize buffer manager
        self.buffer_manager = graphics_lib.buffer_manager(
            self.settings, self.error_handler)

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
        if(self.settings.enable_graphics):
            if(self.command_mode):
                line = self.command_line.update()
                if(line[0]):
                    self.command_mode = False
                    if(line[1] == "quit"):
                        self.quit_sv()
                    # run command
                command_line = self.command_line.get_text_object()
            else:
                command_line = pygame.Surface((0, 0))
                window_events = self.graphics_window.check_events()
                self.process_events(window_events)
                self.process_user_events(window_events)

        # check for exit request
        if(self.serial_device.exit_request):
            self.quit_sv()
        # refresh thread timeout
        else:
            self.serial_device.thread_timeout = time.time() + 0.1

        # acquire thread lock -------------------------------------------------
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
        # release lock --------------------------------------------------------

        if(self.settings.enable_graphics):
            # update buffer
            self.graphics_window.update_screen(
                self.buffer_manager.get_buffer(),
                self.command_mode,
                command_line)

    #   --------------------------------
    #
    #   command bindings (default)
    #
    #   --------------------------------
    def process_events(self, events):

        """
        Process keyboard instructions. Doesn't run in command mode

        Parameters
        ----------
        events : dict
            Event list from keyboard
        """

        # unpack events
        (events_hold, events_press) = events

        # hold key events:
        if "quit" in events_press:
            self.quit_sv()

        if "cmd" in events_press:
            self.command_mode = True
            # create new command line
            self.command_line = graphics_lib.command_line(self.settings)

        # check buffer related controls
        self.buffer_manager.check_controls(events)

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
        if(self.settings.enable_graphics):
            self.graphics_window.close_window()
        self.csv_log.close_file()

        exit()

    #   --------------------------------
    #
    #   command bindings (user, dummy function)
    #
    #   --------------------------------
    def process_user_events(self, events):

        """
        Placeholder class for user events
        """

        pass


#   --------------------------------
#
#   Default run parameters
#
#   --------------------------------
if __name__ == "__main__":
    serial_device = serial_vis(path="/dev/ttyACM0", baudrate=115200)
    while(1):
        serial_device.update()
