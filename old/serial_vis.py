import pygame
import serial
from serial_parse import *
from csv_logger.py import *
from graphics import *


# main serial device class
class serial_device:


    #   --------------------------------
    #
    #   Attributes
    #
    #   --------------------------------

    # program state information
    mode = 1

    #
    # user modifiable overrides:
    #

    # controls overrides
    controls = {}

    # log settings overrides
    log_settings = {}

    # graphics settings overrides
    graphics_settings = {}

    # color overrides
    colors = {}

    # user commands (function prototypes)
    commands = {}

    # user functions (actual function objects)
    # todo
    user_functions = []


    #   --------------------------------
	#
	#	Initialization
	#
    #   --------------------------------
	def __init__(self, path, baudrate):
		

        #
        # system initializations:
        #

		counter = 0
		# open serial interface
		while(1): 

			try:
    	        self.device = serial.Serial(path,baudrate,timeout=1)
        	    print("Launchpad connected: "+path)
            	break

        	except:
        		# Limit the message to one every two seconds
        		if(counter % 10 == 0):
	            	print("No launchpad found.")

            # wait 200ms before trying again
            pygame.time.wait(200)
            counter += 1

        # add user-defined commands, colors, scales, etc
        self.register_user_commands()
        self.register_user_settings()

        # create the parser object
        self.parser = parser(self.commands)

        # create the log file object 
        # after giving the user a chance to change the output name.
        self.log = csv_logger(self.log_settings)

        # create the draw buffer object
        self.graphics = graphics(self.controls,
                                 self.colors,
                                 self.graphics_settings,
                                 self.user_functions)

    #   --------------------------------
    #
    #   load user definitions (dummy function)
    #
    #   --------------------------------

    def register_user_commands(self):
        pass

    def register_user_settings(self):
        pass


    #   --------------------------------
    #
    #   get launchpad uart output
    #
    #   --------------------------------
    def get_line(self):
        return(self.device.readline().strip())


    #   --------------------------------
    #
    #   execute program update
    #
    #   --------------------------------
    def update(self):

        # exit cleanly.
        if(self.mode == 0):
            self.log.closefile()
            exit()

        # get an instruction
        instruction = process_command(self.get_line())

        # check for keyboard input
        self.mode = self.graphics.check_input(self.mode)

        # if it's a control instruction:
        if(instruction[0] == "draw"):
            self.graphics.execute_buffer(self.mode)
        elif(instruction[0] == "log" or 
             instruction[0] == "logstart" or 
             instruction[0] == "logend"):
            self.log.log_data(instruction)
        elif(instruction[0] == "echo"):
            print(instruction[1])

        # otherwise, add it to the current buffer
        else:
            self.graphics.add_to_buffer(instruction)

        # check for unsatisfied frame change request
        if(self.mode == 1):
            self.graphics.check_pause_update()