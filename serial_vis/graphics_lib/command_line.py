# command_line.py
# command line interface inside a pygame window

import pygame
import time


#   --------------------------------
#
#   Command line
#
#   --------------------------------
class command_line:

    """
    Command line class

    Attributes
    ----------
    is_capslock
        Toggles if capslock is enabled or disabled
    """

    # track capslock mode
    is_capslock = False

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, settings):

        """
        Create new command line instance.

        Parameters
        ----------
        settings
            settings object
        """

        self.settings = settings
        self.cursor_pwm = 0

        self.font = pygame.font.SysFont(
            self.settings.font, self.settings.font_size)
        self.line_contents = ""

    #   --------------------------------
    #
    #   Update
    #
    #   --------------------------------
    def update(self):

        """
        Update command line

        Returns
        -------
        bool
            Is done
        str
            Line contents
        """

        str_to_add = ""
        caps = self.is_capslock

        for event in pygame.event.get():

            # check control keys
            if(event.type == pygame.KEYDOWN):

                # backspace
                if(event.type == pygame.K_BACKSPACE):
                    if(len(self.line_contents) > 0):
                        self.line_contents = self.line_contents[:-1]

                # escape
                if(event.type == pygame.K_ESCAPE):
                    # return a blank line and exit command line mode
                    return((True), "")

                # enter
                if(event.type == pygame.K_RETURN):
                    # return the line and exit command line mode
                    return((True), self.line_contents)

                # left arrow
                if(event.type == pygame.K_LEFT):
                    if(self.current_index > 0):
                        self.current_index -= 1

                # right arrow
                if(event.type == pygame.K_RIGHT):
                    if(self.current_index < len(self.line_contents)):
                        self.current_index += 1

                # shift
                if(event.type == pygame.K_RSHIFT or
                   event.type == pygame.K_LSHIFT):
                    caps = not caps

                # capslock
                if(event.type == pygame.K_CAPSLOCK):
                    self.is_capslock = not self.is_capslock

            # append key to the string
            if event.type in self.keymap:
                str_to_add += self.keymap[event.type]
                self.current_index += 1

        # make caps if applicable
        if(caps):
            str_to_add.upper()

        # add in string at the cursor location
        self.line_contents = (
            self.line_contents[:self.current_index] +
            str_to_add +
            self.line_contents[self.current_index:])

        # blinking cursor, once every second
        # blank out the current_index character
        if(time.time() % 1 < 0.5):
            self.line_contents[self.current_index] = " "

        # return a not done string
        return((False, ""))

    #   --------------------------------
    #
    #   Get text object
    #
    #   --------------------------------
    def get_text_object(self):

        """
        Get text object corresponding to the current line

        Returns
        -------
        surface
            Pygame surface object containing the command line text
        """

        textframe = self.font.render(
            self.line_contents, False, self.settings.colors["black"])

        return(textframe)
