import time
import pygame
import serial
from serial_parse import *

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
        self.logblock_in_progress = False
        self.logcache = []
        self.logcache_time = "0"

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
            # str name, int r, int g, int b
            "definecolor":["s","dd"],
            # float scale
            "setscale":["f"],
            # int xoffset, in yoffset
            "setoffset":["d","d"],
            # float x_1, float y_1, float x_2, float y_2, str color
            "drawline":["f","f","f","f","s"],
            # float x, float y, float r, str color
            "drawcircle":["f","f","f","s"],
            # float x, float y, float r, float theta, str color
            "drawray":["f","f","f","f","s"],
            # float x, float y, str label, str color
            "text":["f","f","s","s"],
            # str message
            "echo":["s"],
            # float message with multiple parts
            "echol":["l","_"],
            # clear screen
            "clrscrn":[],
            # start drawing
            "start":[],
            # stop drawing
            "stop":[],
            # draw current buffer
            "draw":[]
        }

        # add user-defined commands, colors, scales, etc
        self.register_user_commands()
        self.register_user_settings()

        # open log file after giving the user a chance to rename the output.
        self.log_output_file = open(self.log_output_name,w)


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
    #   log data given in a log opcode.
    #
    #   --------------------------------
    def log_data(self,instruction):

        # logstart opcode is called
        if(instruction[0] == "logstart"):
            # set flag
            self.logblock_in_progress == True
            # record start time
            self.logcache_time = str(time.time())
            # clear cache
            self.logcache = []

        # logend opcode is called, 
        elif(instruction[0] == "logend"):
            # clear flag
            self.logblock_in_progress == False
            
            # write each entry
            for datatype in self.logcache:
                self.log_output_file.write(self.logcache_time)
                for entry in datatype:
                    self.log_output_file.write(",",entry)
                self.write("\n")

        # if a log block is in progress:
        elif(self.logblock_in_progress == True):

            # see if it matches an existing entry in the cache
            match = False
            for datatype in self.logcache:
                # match -> insert
                if(instruction[1] == datatype[0]):
                    datatype.append(instruction[2])
                    match = True
            # no match -> create new entry
            if(match == False):
                self.logcache.append([instruction[1],instruction[2]])

        # no log block in progress => log normally.
        elif(self.logblock_in_progress == False):
            timestamp = str(time.time())

            writeline = timestamp + "," + instruction[1] + "," + instruction[2] + "\n"
            self.log_output_file.write(writeline)


    #   --------------------------------
    #
    #   execute program update
    #
    #   --------------------------------
    def update(self):

        # exit cleanly.
        if(self.exit == True):
            self.log_output_file.close()
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
            self.log_data(instruction)

        # otherwise, add it to the current buffer
        else:
            self.current_buffer.append(instruction)