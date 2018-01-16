import pygame
import math
import graphics_window.py

# graphics management class
class graphics(graphics_window.graphics_window):


    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
	def __init__(self,controls,colors,settings,user_functions):
        
		# main draw buffer
		self.current_buffer = []

		# frame history for oscilloscope-like functions:
		self.frame_queue = []
        self.frame_queue_end = 0

        self.controls = controls


        # update settings
        self.colors.update(colors)
        self.settings.update(settings)
        self.controls.update(controls)

        self.scale = self.settings["scale"]
        self.offset = self.settings["offset"]
        self.line_width = self.settings["line_width"]
        self.font = self.settings["font"]
        self.store_frames = self.settings["store_frames"]
        self.frame_limit = self.settings["frame_limit"]

        # user defined functions
        self.user_functions = user_functions

        # set up graphics
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(settings["window_size"])
        self.clock = pygame.time.Clock()


    #   --------------------------------
    #
    #   execute the instruction buffer
    #
    #   --------------------------------
    def execute_buffer(self,mode):

        # clear the pygame buffer
        self.screen.fill(self.colors["background"])

        # in live mode
        if(mode == 1):
            self.draw_buffer(self.current_buffer)

        # in pause mode, and a redraw has been requested
        elif(mode == -1 and self.force_redraw == True):
            
            # get the buffer
            self.draw_buffer(self.get_buffer())

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

        # display pygame buffer
        pygame.display.flip()
        # limit framerate
        self.clock.tick(self.frame_limit)


    #   --------------------------------
    #
    #   check if there's an unsatisfied pause update request
    #
    #   --------------------------------
    def check_pause_update(self):
        if(self.force_redraw == True):

            # get the buffer
            self.draw_buffer(self.get_buffer())

            # acknowledge receipt of the redraw request.
            self.force_redraw = False


    #   --------------------------------
    #
    #   draw the instruction buffer
    #
    #   --------------------------------
    def draw_buffer(self,target_buffer):

        for instruction in target_buffer:

            try:
                # run default functions
                drawmethod = getattr(self,instruction[0])
                drawmethod(instruction)
            except:
                # run user functions
                self.user_functions(instruction)

            # todo:
            # save the buffer to the buffer history


    #   --------------------------------
    #
    #   change the current frame (with protection of course)
    #
    #   --------------------------------
    def change_frame(self,index):
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
    #   Add an instruction to the current buffer
    #
    #   --------------------------------
    def add_to_buffer(self,instruction):
        self.current_buffer.append(instruction)


    #   --------------------------------
    #
    #   Get the buffer at a certain index
    #
    #   --------------------------------
    def get_buffer(self):

    	# todo
        # takes in self.index
    	# get the indexed frame buffer from the frame queue.

    	return(frame)