# serial_vis.py
# main class

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

    is_live = True
    display_buffer_id = 0

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
        self.serial_device = serial_lib.threaded_serial(self.settings)

        # create graphics window
        if(self.settings.enable_graphics):
            self.graphics_window = self.graphics_class(
                self.settings, self.error_handler)

        # set up buffer db
        self.buffer_db = graphics_lib.buffer_db(self.settings)

        # set up initial frame buffer
        self.current_buffer = graphics_lib.frame_buffer()

    #   --------------------------------
    #
    #   execute program update
    #
    #   --------------------------------
    def update(self):

        """
        Execute master program update.
        """

        if(self.settings.enable_graphics):
            # process keyboard/mouse commands
            window_events = self.graphics_window.check_events()
            self.process_events(window_events)
            self.process_user_events(window_events)

        # check for exit request
        if(self.serial_device.exit_request):
            self.quit_sv()
        # refresh running flag
        else:
            self.serial_device.running = True

        # fetch instruction
        if(len(self.serial_device.instruction_buffer) > 0):
            instruction = self.serial_device.instruction_buffer[-1]

        # log command with window fps tracker
        self.graphics_window.update_fps(instruction)

        # check for control instructions:
        if(instruction[0] == "draw" and self.settings.enable_graphics):

            # live => create new buffer
            # set the current view
            if(self.is_live):
                self.buffer_db.new_buffer(self.current_buffer)
                self.buffer_db.set_current_view()
            # not live => create new buffer
            # do not set current view
            else:
                self.buffer_db.new_buffer(self.current_buffer)

            # create new frame buffer
            self.current_buffer = graphics_lib.frame_buffer()

        # trigger instruction
        elif(instruction[0] == "trigger"):
            self.is_live = False
            self.display_buffer_id = 0

        # log instructions
        elif(instruction[0] in ["logs", "logf", "logstart", "logend"]):
            self.csv_log.log_data(instruction)

        # print instruction
        elif(instruction[0] == "echo"):
            print(instruction[1])

        # null instruction
        elif(instruction[0] == "null"):
            pass

        # otherwise, add it to current buffer
        else:
            self.current_buffer.add_instruction(instruction)

        if(self.settings.enable_graphics):
            # update buffer
            self.graphics_window.update_screen(
                self.buffer_db.get_buffer(
                    self.display_buffer_id, relative=True))

    #   --------------------------------
    #
    #   command bindings (default)
    #
    #   --------------------------------
    def process_events(self, events):

        """
        Process keyboard instructions.

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

        # press key events:
        if "pause" in events_press:
            self.is_live = not self.is_live
            if(self.is_live):
                self.display_buffer_id = 0

        # controls only enabled when not live
        if not self.is_live:
            if "fwd" in events_press:
                self.display_buffer_id += 1

            if "fwdplus" in events_press:
                self.display_buffer_id += 10

            if "back" in events_press:
                self.display_buffer_id += -1

            if "backplus" in events_press:
                self.display_buffer_id += -10

        # check for out of bounds
        if (self.display_buffer_id > self.settings.max_size_forward):
            self.display_buffer_id = self.settings.max_size_forward

        if (self.display_buffer_id < -self.settings.max_size_backward):
            self.display_buffer_id = -self.settings.max_size_backward

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
        self.serial_device.close()
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
