# serial_vis.py
# main class

# todo: implement docstrings

from buffer import *
from default_vector_graphics import *
from serial_device import *
from serial_parser import *
from csv_log import *


# main serial_vis class
class serial_vis:

    #   --------------------------------
    #
    #   Attributes
    #
    #   --------------------------------

    user_settings = {}
    user_commands = {}
    graphics_class = default_vector_graphics

    is_live = True
    display_buffer_id = 0

    settings = {
        "quit_on_disconnect": True
    }

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, path, **kwargs):

        # update settings
        dict_merge(self.settings, self.user_settings)
        dict_merge(self.settings, kwargs)

        # create serial device, serial parser, log, frame buffer db,
        # and graphics window
        self.serial_device = serial_device(path, **self.settings)
        self.serial_parser = parser(self.user_commands, **self.settings)
        self.csv_log = csv_log(**self.settings)
        self.graphics_window = self.graphics_class(**self.settings)
        self.buffer_db = buffer_db(**self.settings)

        # set up initial frame buffer
        self.current_buffer = frame_buffer()

        # discard incomplete line
        self.serial_device.discard_line()

    #   --------------------------------
    #
    #   execute program update
    #
    #   --------------------------------
    def update(self):

        # process keyboard/mouse commands
        window_events = self.graphics_window.check_events()
        self.process_events(window_events)
        self.process_user_events(window_events)

        # get line
        line = self.serial_device.get_line()

        # check for device disconnect
        if(not line[1]):
            if(self.settings["quit_on_disconnect"]):
                self.quit_sv()

        # parse instruction
        instruction = self.serial_parser.process_command(line[0])

        # log command with window fps tracker
        self.graphics_window.update_fps(instruction)

        # check for control instructions:
        if(instruction[0]) == "draw":

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
            self.current_buffer = frame_buffer()

        # log instructions
        elif(instruction[0] in ["logs", "logf", "logstart", "logend"]):
            self.csv_log.log_data(instruction)

        # print instruction
        elif(instruction[0] == "echo"):
            print(instruction[1])

        # otherwise, add it to current buffer
        else:
            self.current_buffer.add_instruction(instruction)

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

        # unpack events
        (events_hold, events_press) = events

        # hold key events:
        if pygame.QUIT in events_hold:
            self.quit_sv()

        # press key events:
        if "pause" in events_press:
            self.is_live = not self.is_live
            if(self.is_live):
                self.display_buffer_id = 0

        if "fwd" in events_press:
            self.display_buffer_id += 1

        if "fwdplus" in events_press:
            self.display_buffer_id += 10

        if "back" in events_press:
            self.display_buffer_id += -1

        if "backplus" in events_press:
            self.display_buffer_id += -10

    #   --------------------------------
    #
    #   quit
    #
    #   --------------------------------
    def quit_sv(self):
        # call clean close methods
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
        pass
