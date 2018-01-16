import pygame
import serial
from serial_parse import *
from csv_logger.py import *
from graphics import *


# main serial device class
class serial_device:

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

        # program state information
        self.exit = False
        self.mode = 1

        #
        # user modifiable defaults:
        #

        # controls
        self.controls = {"pause":pygame.K_SPACE,
                         "forward":pygame.K_PERIOD,
                         "superforward":pygame.K_LEFTBRACKET,
                         "backward":pygame.K_COMMA,
                         "superbackward":pygame.K_RIGHTBRACKET}

        # log file name
        self.log_output_name = "serial_log.csv"

        # default graphics settings
        self.settings = {"window_size":(800,600),
                         "scale":1.0,
                         "offset":(0,0),
                         "store_frames":100,
                         "frame_limit":120}

        # initialize color dictionary
        self.colors = {"black": (0,0,0), "white": (255,255,255)}

        # default command dictionary
        self.commands = {
            # control commands:
            # draw
            "draw":[],
            # log: label, datastring
            "log":["s","s"],
            # start log block
            "logstart":[],
            # end log block
            "logend":[],
            # print to console
            "echo":["s"],

            # drawing commands:
            # define color: name, (r,g,b)
            "definecolor":["s","dd"],
            # set scale: ratio
            "setscale":["f"],
            # set offset: (x,y)
            "setoffset":["dd"],
            # draw line: (x_1,y_1),(x_2,y_2),color
            "drawline":["ff","ff","s"],
            # draw line (pixel mode): (x_1,y_1),(x_2,y_2),color
            "drawlinep":["dd","dd","s"],
            # draw circle: (x,y),r,color
            "drawcircle":["ff","f","s"],
            # draw ray: (x,y),angle,radius,color
            "drawray":["ff","f","f","s"],
            # draw text: text,(x,y),size,color
            "text":["s","ff","d","s"],
            # draw text (pixel mode): text,(x,y),size,color
            "textp":["s","dd","d","s"],
        }

        # add user-defined commands, colors, scales, etc
        self.register_user_commands()
        self.register_user_settings()

        # create the log file object 
        # after giving the user a chance to change the output name.
        self.log = csv_logger(self.log_output_name)

        # create the draw buffer object
        self.graphics = graphics(self.controls,
                                 self.colors,
                                 self.settings,
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
    #   load user definitions (dummy function)
    #
    #   --------------------------------
    def user_functions(self,instruction):
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
        if(self.exit == True):
            self.log.closefile()
            exit()

        # get an instruction
        instruction = process_args(parse_line(self.get_line()),self.commands)

        # check for keyboard input
        self.mode = self.graphics.check_input(self.mode)

        # if it's a control instruction:
        if(instruction[0] == "draw"):
            self.graphics.execute_buffer(self.mode)
        elif(instruction[0] == "log" or 
             instruction[0] == "logstart" or 
             instruction[0] == "logend"):
            self.log.log_data(instruction)

        # otherwise, add it to the current buffer
        else:
            self.graphics.add_to_buffer(instruction)

        # check for unsatisfied frame change request
        if(self.mode == 1):
            self.graphics.check_pause_update()