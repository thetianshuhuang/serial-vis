import pygame
import math


# graphics draw methods. No control flow here.
class graphics_window:


    #   --------------------------------
    #
    #   Attributes
    #
    #   --------------------------------

	# graphics state information
    current_frame = 0
    force_redraw = False

    # initialize color dictionary; default background color is white
    colors = {"black": (0,0,0), 
              "white": (255,255,255), 
              "background": (255,255,255)}

    # graphics settings
    settings = {"window_size":(800,600),
	            "scale":1.0,
	            "offset":(0,0),
	            "store_frames":100,
	            "frame_limit":60,
	            "line_width":2,
	            "font":"arial"}

	# controls
    controls = {"pause":pygame.K_SPACE,
                "forward":pygame.K_PERIOD,
                "superforward":pygame.K_LEFTBRACKET,
                "backward":pygame.K_COMMA,
                "superbackward":pygame.K_RIGHTBRACKET}


    #   --------------------------------
    #
    #   Initialization (dummy function; overwritten by graphics.py)
    #
    #   --------------------------------
	def __init__():
		pass


	#   --------------------------------
    #
    #   draw functions
    #
    #   --------------------------------

    def definecolor(self,instruction):
        # first, attempt to overwrite an existing definition
        try:
            self.colors[instruction[1]] = instruction[2]
        except:
            self.colors.append({instruciton[1]:instruction[2]}) 

    def setscale(self,instruction):
        self.scale = instruction[1]

    def setoffset(self,instruction):
        self.offset = instruction[1]

    def drawline(self,instruction):
        pygame.draw.line(screen,
            self.colors[instruction[3]],
            (instruction[1][0]*self.scale+self.offset[0],
                instruction[1][1]*self.scale+self.offset[1]),
            (instruction[2][0]*self.scale+self.offset[0],
                instruction[2][1]*self.scale+self.offset[1]),
            self.line_width)

    def drawlinep(self,instruction):
        pygame.draw.line(screen,
            self.colors[instruction[3]],
            instruction[1],
            instruction[2],
            self.line_width)

    def drawcircle(self,instruction):
        pygame.draw.circle(screen,
            self.colors[instruction[3]],
            (instruction[1][0]*self.scale+self.offset[0],
                instruction[1][1]*self.scale+self.offset[1]),
            instruction[2]*self.scale,
            self.line_width)

    def drawray(self,instruction):
        pygame.draw.line(screen,
            self.colors[instruction[4]],
            (instruction[1][0]*self.scale+self.offset[0],
                instruction[1][1]*self.scale+self.offset[1]),
            ((instruction[1][0] + instruction[3]*math.cos(instruction[2]))
                *self.scale+self.offset[0],
            (instruction[1][1] + instruction[3]*math.sin(instruction[2]))
                *self.scale+self.offset[1]),
            self.line_width)

    def text(self,instruction):
        # create font
        textfont = pygame.font.SysFont(self.font, instruction[3])
        # create surface
        textframe = textfont.render(instruction[1], False, 
            self.colors[instruction[4]])
        # merge surface
        self.screen.blit(frametext,
            instruction[2][0]*self.scale+self.offset[0],
            instruction[2][1]*self.scale+self.offset[1])


    #   --------------------------------
    #
    #   check for keyboard input
    #
    #   --------------------------------
    def check_input(self, mode):

        for event in pygame.event.get():

            # check for exit command
            if event.type == pygame.QUIT:
            	# 0 mode is the exit state
                mode = 0

            # go through controls
            elif event.type == pygame.KEYDOWN:
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

        # the runmode is stored in the main class
        return(mode)