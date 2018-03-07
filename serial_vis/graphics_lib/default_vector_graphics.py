# default_vector_graphics.py
# extension of vector_graphics_window
# contains default graphics commands for serial_vis

import math
from vector_graphics_window import *


#   --------------------------------
#
#   Default vector graphics commands
#
#   --------------------------------

class default_vector_graphics(vector_graphics_window):

    """
    Vector graphics class with default commands.

    Attributes
    ----------
    All attributes inherited from vector_graphics_window
    """

    #   --------------------------------
    #
    #   utility functions
    #
    #   --------------------------------
    def transform(self, coord):

        """
        Transform a coordinate based on the current scale and offset.

        Parameters
        ----------
        coord : float[]
            (x_coord, y_coord) to be transformed

        Returns
        -------
        int[]
            (x_coord, y_coord), both integers
        """
        return(
            int(
                round(
                    coord[0] * self.settings.scale +
                    self.settings.offset[0], 0)),
            self.settings.window_size[1] -
            int(
                round(
                    coord[1] * self.settings.scale +
                    self.settings.offset[1], 0)))

    #   --------------------------------
    #
    #   draw functions
    #
    #   --------------------------------

    """
    Draw functions are selected automatically by
    update_screen in vector_graphics_window using their name, which must match
    the name given in the command registry.
    """

    def definecolor(self, instruction):
        if(len(instruction[2]) >= 3):
            self.settings.attr_merge(
                {"colors": {instruction[1]: instruction[2]}})
        else:
            self.error_handler.raise_error("tts", instruction[0])

    def setscale(self, instruction):
        self.settings.scale = instruction[1]

    def setoffset(self, instruction):
        self.settings.offset = instruction[1]

    def drawline(self, instruction):
        pygame.draw.line(
            self.screen,
            self.get_color(instruction[3]),
            self.transform(instruction[1]),
            self.transform(instruction[2]),
            self.settings.line_width)

    def drawlinep(self, instruction):
        pygame.draw.line(
            self.screen,
            self.get_color(instruction[3]),
            instruction[1],
            instruction[2],
            self.settings.line_width)

    def drawcircle(self, instruction):
        # width greater than radius protection
        radius = int(round(instruction[2] * self.settings.scale))
        if(radius < self.settings.line_width):
            radius = self.settings.line_width + 1

        pygame.draw.circle(
            self.screen,
            self.get_color(instruction[3]),
            self.transform(instruction[1]),
            radius,
            self.settings.line_width)

    def drawray(self, instruction):
        pygame.draw.line(
            self.screen,
            self.get_color(instruction[4]),
            self.transform(instruction[1]),
            self.transform((instruction[1][0] +
                            instruction[3] * math.cos(instruction[2]),
                            instruction[1][1] +
                            instruction[3] * math.sin(instruction[2]))),
            self.settings.line_width)

    def text(self, instruction):
        # create font
        textfont = pygame.font.SysFont(self.settings.font, instruction[3])
        # create surface
        textframe = textfont.render(
            instruction[1], False, self.get_color(instruction[4]))
        # merge surface
        self.screen.blit(textframe, self.transform(instruction[2]))

    def textp(self, instruction):
        # create font
        textfont = pygame.font.SysFont(self.font, instruction[3])
        # create surface
        textframe = textfont.render(
            instruction[1], False, self.colors[instruction[4]])
        # merge surface
        self.screen.blit(textframe, instruction[2])
