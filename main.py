from serial_vis.py import *


class user_vector_graphics(default_vector_graphics):

    def exampleusercommand(self, instruction):
        print("Example user command: " + instruction[1])

    # put user commands here


# extend the serial_device class to add user definitions.
class my_serial_vis(serial_vis):

    # graphics command registration
    user_commands = {"exampleusercommand": "s"}
    graphics_class = user_vector_graphics

    # settings
    settings = {}


# create object
my_serial_device = my_serial_device("/dev/lm4f", baudrate=115200)

# that's it!
while(1):
    my_serial_device.update()
