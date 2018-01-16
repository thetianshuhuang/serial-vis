import pygame
import serial
from serial_parse import *
from csv_logger.py import *

# command scheme:
# OPCODE:argument:argument:arrayarg,arrayarg,arrayarg:argument

class serial_device:

    #   --------------------------------
	#
	#	Initialization
	#
    #   --------------------------------
	def __init__(self, path, baudrate, window_size):
		
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


        #
        # system initializations:
        #

        # set up graphics
		pygame.init()
		screen = pygame.display.set_mode(window_size)

        # initialize draw buffer
        self.current_buffer = []

        # initialize frame history for oscilloscope-like functions
        self.frame_queue = []
        self.frame_queue_end = 0

        # program state information
        self.exit = False
        self.mode = 1
        self.current_frame = 0
        self.force_redraw = False

        #
        # user modifiable defaults:
        #

        # controls
        self.key_pause = pygame.K_SPACE
        self.key_forward = pygame.K_PERIOD
        self.key_superforward = pygame.K_LEFTBRACKET
        self.key_backward = pygame.K_COMMA
        self.key_superbackward = pygame.K_RIGHTBRACKET

        # frame memory
        self.store_frames = 100

        # log file name
        self.log_output_name = "serial_log.csv"

        # default scale
        self.scale = 1
        self.offset = (0,0)

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
    #   execute the instruction buffer
    #
    #   --------------------------------
    def execute_buffer(self):

        # in live mode
        if(self.mode == 1):
            self.draw_buffer(self.current_buffer)

        # in pause mode, and a redraw has been requested
        elif(self.mode == -1 and self.force_redraw == True):
            
            # todo: find buffer
            self.draw_buffer(self.asdf)

            # acknowledge receipt of the redraw request.
            self.force_redraw = False

        # add the buffer to memory
        if(len(self.frame_queue) < self.store_frames):
            self.frame_queue.append(current_buffer)
        elif(self.frame_queue_end <= self.store_frames):
            self.frame_queue[frame_queue_end] = current_buffer
            frame_queue_end += 1
        else:
            self.frame_queue[0] = current_buffer
            frame_queue_end = 0

        # clear buffer
        self.current_buffer = []


    #   --------------------------------
    #
    #   draw the instruction buffer
    #
    #   --------------------------------
    def draw_buffer(target_buffer):

        for instruction in target_buffer:

            # run functions
            # todo

            # run default functions
            if(self.user_functions(self,instruction) == False)
                
                # print out the unrecognized opcode to the console for debugging.
                print("ERROR: unrecognized opcode: " + instruction[0])


    #   --------------------------------
    #
    #   load user definitions (dummy function)
    #
    #   --------------------------------
    def user_functions(self,instruction):
        pass


    #   --------------------------------
    #
    #   check for keyboard input
    #
    #   --------------------------------
    def check_input(self):

        for event in pygame.event.get():

            # check for exit command
            if event.type == pygame.QUIT:
                self.exit = True

            # go through controls
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_pause:
                    self.mode = -self.mode
                elif event.key == self.key_forward:
                    self.change_frame(1)
                elif event.key == self.key_superforward:
                    self.change_frame(10)
                elif event.key == self.key_backward:
                    self.change_frame(-1)
                elif event.key == self.key_superforward:
                    self.change_frame(-10)


    #   --------------------------------
    #
    #   change the current frame (with protection of course)
    #
    #   --------------------------------
    def change_frame(index):
        # change the current frame index
        self.current_frame += index
        if(self.current_frame > self.store_frames):
            self.current_frame = 100
        elif(self.current_frames < -self.store_frames):
            self.current_frame = -100

        # force a redraw to reflect the change in frame.
        self.force_redraw = True


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

        # check for keyboard input
        self.check_input()

        # get an instruction
        instruction = self.parse_line(self.get_line())

        # if it's a control instruction:
        if(instruction[0] == "draw"):
            self.execute_buffer()
        elif(instruction[0] == "log" or 
             instruction[0] == "logstart" or 
             instruction[0] == "logend"):
            self.log.log_data(instruction)

        # otherwise, add it to the current buffer
        else:
            self.current_buffer.append(instruction)