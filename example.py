# example program using serial-vis.

import serial_vis


# user vector graphics
# user commands go here
class user_vector_graphics(serial_vis.default_vector_graphics):

    pass


# extend the serial_device class to add user definitions.
class my_serial_vis(serial_vis.serial_vis):

    # graphics command registration
    user_commands = {"exampleusercommand": "s"}
    graphics_class = user_vector_graphics

    # settings
    user_settings = {}

    # user keyboard event processing
    def _exampleEvent(self, arguments, command):
        pass


# create object
# **kwargs can also be used to update settings
my_serial_device = my_serial_vis(path="/dev/ttyUSB0", baudrate=115200)

# that's it!
while(1):
    my_serial_device.update()
