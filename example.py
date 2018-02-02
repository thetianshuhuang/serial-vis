# example program using serial-vis.

import src


# user vector graphics
# user commands go here
class user_vector_graphics(src.default_vector_graphics):

    def exampleusercommand(self, instruction):
        print("Example user command: " + instruction[1])


# extend the serial_device class to add user definitions.
class my_serial_vis(src.serial_vis):

    # graphics command registration
    user_commands = {"exampleusercommand": "s"}
    graphics_class = user_vector_graphics

    # settings
    user_settings = {}

    # user keyboard event processing
    def process_user_events(self, events):
        pass


# create object
# **kwargs can also be used to update settings
my_serial_device = my_serial_vis(path="/dev/ttyACM0", baudrate=115200)

# that's it!
while(1):
    my_serial_device.update()
