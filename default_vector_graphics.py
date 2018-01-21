# default_vector_graphics.py
# extension of vector_graphics_window
# contains default graphics commands for serial_vis

import math
from .vector_graphics_window import *


# class adding default draw functions

class default_vector_graphics(vector_graphics_window):

    #   --------------------------------
    #
    #   utility functions
    #
    #   --------------------------------
    def transform(self, coord):
        return(coord[0] * self.settings["scale"] + self.settings["offset"][0],
               coord[1] * self.settings["scale"] + self.settings["offset"][1])

    #   --------------------------------
    #
    #   draw functions
    #
    #   --------------------------------
    def definecolor(self, instruction):
        self.settings["colors"].update({instruction[1]: instruction[2]})

    def setscale(self, instruction):
        self.settings["scale"] = instruction[1]

    def setoffset(self, instruction):
        self.settings["offset"] = instruction[1]

    def drawline(self, instruction):
        pygame.draw.line(
            screen,
            self.settings["colors"][instruction[3]],
            self.transform(instruction[1]),
            self.transform(instruction[2]),
            self.settings["line_width"])

    def drawlinep(self, instruction):
        pygame.draw.line(
            screen,
            self.settings["colors"][instruction[3]],
            instruction[1],
            instruction[2],
            self.settings["line_width"])

    def drawcircle(self, instruction):
        pygame.draw.circle(
            screen,
            self.settings["colors"][instruction[3]],
            self.transform(instruction[1]),
            instruction[2] * self.scale,
            self.settings["line_width"])

    def drawray(self, instruction):
        pygame.draw.line(
            screen,
            self.settings["colors"][instruction[4]],
            self.transform(instruction[1]),
            self.transform((instruction[1][0] + math.cos(instruction[2]),
                           instruction[1][1] + math.sin(instruction[2]))),
            self.settings["line_width"])

    def text(self, instruction):
        # create font
        textfont = pygame.font.SysFont(self.font, instruction[3])
        # create surface
        textframe = textfont.render(
            instruction[1], False, self.colors[instruction[4]])
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
