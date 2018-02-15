# command_line.py
# command line interface inside a pygame window

import pygame
import time
from keyboard_keybinds import keyboard_keybinds


#   --------------------------------
#
#   Command line
#
#   --------------------------------
class command_line(keyboard_keybinds):

    """
    Command line class

    Attributes
    ----------
    is_capslock : bool
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
        settings : settings object
            settings object for serial vis
        """

        self.settings = settings
        self.cursor_pwm = 0
        self.current_index = 0

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

        keys_to_add = []
        str_to_add = ""

        for event in pygame.event.get():

            # check control keys
            if(event.type == pygame.KEYDOWN):

                # backspace
                if(event.key == pygame.K_BACKSPACE):
                    if(len(self.line_contents) > 0):
                        self.line_contents = (
                            self.line_contents[:self.current_index - 1] +
                            self.line_contents[self.current_index:])
                        if(self.current_index > 0):
                            self.current_index -= 1

                # delete
                if(event.key == pygame.K_DELETE):
                    if(len(self.line_contents) > 0):
                        self.line_contents = (
                            self.line_contents[:self.current_index - 1] +
                            self.line_contents[self.current_index:])

                # escape
                elif(event.key == pygame.K_ESCAPE or
                     event.key == pygame.K_BACKQUOTE):
                    # return a blank line and exit command line mode
                    return((True), "")

                # enter
                elif(event.key == pygame.K_RETURN):
                    # return the line and exit command line mode
                    return((True), self.line_contents)

                # left arrow
                elif(event.key == pygame.K_LEFT):
                    if(self.current_index > 0):
                        self.current_index -= 1

                # right arrow
                elif(event.key == pygame.K_RIGHT):
                    if(self.current_index < len(self.line_contents)):
                        self.current_index += 1

                # append key to the string
                elif event.key in self.keymap:
                    keys_to_add.append(event.key)
                    self.current_index += 1

            # check for quit
            if(event.type == pygame.QUIT):
                return((True), "quit")

        # handle capslock/shift
        if(pygame.key.get_pressed()[pygame.K_CAPSLOCK]):
            self.is_capslock = not self.is_capslock

        caps = self.is_capslock

        if(pygame.key.get_pressed()[pygame.K_RSHIFT] or
           pygame.key.get_pressed()[pygame.K_LSHIFT]):
            caps = not caps

        for key in keys_to_add:
            # make caps if applicable
            if(caps):
                str_to_add += self.keymap[key][1]
            else:
                str_to_add += self.keymap[key][0]

        # add in string at the cursor location
        self.line_contents = (
            self.line_contents[:self.current_index - 1] +
            str_to_add +
            self.line_contents[self.current_index - 1:])

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

        # blinking cursor, once every second
        # blank out the current_index character
        if(2 * time.time() % 1 < 0.3):
            display_line = (
                self.line_contents[:self.current_index - 1] +
                " " +
                self.line_contents[self.current_index:])
        else:
            display_line = self.line_contents

        textframe = self.font.render(
            display_line, False, self.settings.colors["black"])

        return(textframe)
