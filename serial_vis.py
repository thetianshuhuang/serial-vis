# serial_vis.py
# main class

# todo: implement docstrings

from buffer import *
from default_vector_graphics import *
from serial_device import *
from csv_log import *


# main serial_vis class

#

class serial_vis:

    self.settings = {}
    self.user_commands = {}
    self.graphics_class = default_vector_graphics

    self.keybindings = {}  # todo

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, path, **kwargs):

        # update settings
        self.settings.update(kwargs)

        # create serial device, serial parser, log, frame buffer db,
        # and graphics window
        self.serial_device = serial_device(path, **self.settings)
        self.serial_parser = serial_parser(self.user_commands)
        self.csv_log = csv_log(**self.settings)
        self.graphics_window = self.graphics_class(**self.settings)
        self.buffer_db = self.buffer_db(**self.settings)

        # set up initial frame buffer
        self.current_buffer = frame_buffer()

    def update(self):

        self.graphics_window.check_input()

        # todo: govern mode

        instruction = serial_device.process_command(serial_device.get_line())

        # control instructions:
        if(instruction[0]) == "draw":
            self.buffer_db.new_buffer(self.current_buffer, adv_frame=True)
            self.graphics_window.update_screen(
                self.buffer_db.get_buffer(0, relative=True))
            # todo: govern mode
        elif(instruction[0] == "log" or
             instruction[0] == "logstart" or
             instruction[0] == "logend"):
            self.csv_log.log_data(instruction)
        elif(instruction[0] == "echo"):
            print(instruction[1])

        # otherwise, add it to current buffer
        else:
            self.current_buffer.add_instruction(instruction)
