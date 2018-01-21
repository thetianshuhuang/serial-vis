from serial_vis import *


# user vector graphics
# can have any name, as long as it is correctly referenced by my_serial_device
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

    def process_user_events(self, events):
    	pass
    	# this function gets called to process events.

# create object
# **kwargs can also be used to update settings
my_serial_device = my_serial_vis("/dev/lm4f", baudrate=115200)

# that's it!
while(1):
    my_serial_device.update()
