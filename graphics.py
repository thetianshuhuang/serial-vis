import pygame


# graphics class
class graphics:


    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
	def __init__(self,controls,colors,settings,user_functions):
        
        # program state information
        self.mode = 1
        self.current_frame = 0
        self.force_redraw = False

		# main draw buffer
		self.current_buffer = []

		# frame history for oscilloscope-like functions:
		self.frame_queue = []
        self.frame_queue_end = 0

        self.store_frames = store_frames
        self.controls = controls

        # draw settings
        self.colors = colors
        self.scale = settings["scale"]
        self.offset = settings["offset"]

        # user defined functions
        self.user_functions = user_functions

        # set up graphics
        pygame.init()
        screen = pygame.display.set_mode(settings["window_size"])


    #   --------------------------------
    #
    #   execute the instruction buffer
    #
    #   --------------------------------
    def execute_buffer(self,mode):

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
    def draw_buffer(target_buffer):

        for instruction in target_buffer:

            # run default functions
            # todo

            # run user functions
            self.user_functions(instruction)

            # todo:
            # save the buffer to the buffer history




    #   --------------------------------
    #
    #   check for keyboard input
    #
    #   --------------------------------
    def check_input(self, mode):

        for event in pygame.event.get():

            # check for exit command
            if event.type == pygame.QUIT:
                self.exit = True

            # go through controls
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls["pause"]:
                    mode = -mode
                elif event.key == self.controls["forward"]:
                    self.change_frame(1)
                elif event.key == self.controls["superforward"]:
                    self.change_frame(10)
                elif event.key == self.controls["backward"]:
                    self.change_frame(-1)
                elif event.key == self.controls["superforward"]:
                    self.change_frame(-10)

        return(mode)


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