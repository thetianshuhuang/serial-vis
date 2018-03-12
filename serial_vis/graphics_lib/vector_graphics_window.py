# vector_graphics_window.py
# vector graphics base class

import time
from .base_graphics import *


#   --------------------------------
#
#   Vector graphics window
#
#   --------------------------------

class vector_graphics_window(base_graphics):

    """
    Pygame window class; creates vector graphics rendering window
    Extends base_graphics
    """

    #   --------------------------------
    #
    #   Update screen
    #
    #   --------------------------------
    def update_screen(self, frame_buffers, command_mode, command_line):

        """
        Update a screen with the given frame_buffer.

        Parameters
        ----------
        frame_buffers: dict
            dictionary of target names and instruction buffers to be displayed
        """

        # clear pygame buffer
        self.screen.fill(self.settings["main"].colors["background"])

        # show underlay
        self.show_underlay()

        # draw each frame buffer
        for device, frame_buffer in frame_buffers.items():

            # render each instruction
            for instruction in frame_buffer.instructions:

                # run through default draw functions
                try:
                    draw_function = getattr(self, instruction[0])
                    draw_function(instruction, device)
                # raise AttributeError
                # if the requested instruction doesn't exist.
                except AttributeError:
                    self.error_handler.raise_error(
                        "onf", instruction, instruction[0])

        # show frame id and fps
        if(self.settings["main"].show_frame_id):
            self.show_frame_id(frame_buffers)
        if(self.settings["main"].show_fps):
            self.show_fps()

        # show overlay
        self.show_overlay()

        # add in command line state
        if(command_mode):
            self.screen.blit(
                command_line,
                (10,
                 self.settings["main"].window_size[1] -
                 command_line.get_size()[1] - 10))

        # display pygame buffer
        pygame.display.flip()

        # limit the fps
        self.clock.tick(self.settings["main"].frame_limit)

    #   --------------------------------
    #
    #   Display fps and frame id
    #
    #   --------------------------------
    def show_frame_id(self, frame_buffers):

        """
        Display the frame information at the top left.
        """

        info = [["device", "fps", "frame_id", "timestamp", "path"]]

        textfont = pygame.font.SysFont(
            self.settings["main"].font, self.settings["main"].font_size)

        # display information for each buffer
        for device, frame_buffer in frame_buffers.items():

            # generate time string
            timef = time.localtime(frame_buffer.timestamp)
            timel = (str(timef.tm_hour), str(timef.tm_min), str(timef.tm_sec))
            for value in timel:
                if(len(value) == 1):
                    value = "0" + value
            timestr = timel[0] + ":" + timel[1] + ":" + timel[2]

            # get fps
            fps = str(round(self.compute_fps(device), 2))

            # build information array
            info.append([
                device, fps, str(frame_buffer.frame_id),
                timestr, self.settings[device].path])

        # render each entry
        line = 0
        for info_line in info:

            # pad with spaces as defined in settings.display_spacing
            assembled_string = ""
            for i in range(5):
                if(len(info_line[i]) <
                   self.settings["main"].display_spacing[i]):
                    info_line[i] += (
                        " " * (self.settings["main"].display_spacing[i] -
                               len(info_line[i])))
                assembled_string += info_line[i]

            textframe = textfont.render(
                assembled_string,
                False,
                self.settings["main"].colors["black"])

            # move down by settings.font_size each time
            self.screen.blit(
                textframe, (10, 10 + line * self.settings["main"].font_size))
            line += 1

    def show_fps(self):

        """
        Display the current fps at the bottom left.
        """

        textfont = pygame.font.SysFont(
            self.settings["main"].font, self.settings["main"].font_size)
        textframe = textfont.render(
            "fps = " + str(round(self.clock.get_fps(), 2)),
            False,
            self.settings["main"].colors["black"])
        self.screen.blit(
            textframe,
            (self.settings["main"].window_size[0] -
             10 -
             textframe.get_size()[0],
             10))

    #   --------------------------------
    #
    #   dummy function for overlay support
    #
    #   --------------------------------
    def show_overlay(self):
        pass

    #   --------------------------------
    #
    #   dummy function for underlay support
    #
    #   --------------------------------
    def show_underlay(self):
        pass

    #   --------------------------------
    #
    #   get color; safely retrieve color. defaults to black.
    #
    #   --------------------------------
    def get_color(self, colorname, target):

        """
        Safely get the color specified by colorname.

        Parameters
        ----------
        colorname : str
            Name of the desired color
        target : str
            Name of target device

        Returns
        -------
        int[3]: (R,G,B)
            Tuple specifing the color definition
        """

        try:
            return(self.settings[target].colors[colorname])
        except KeyError:
            return(self.settings[target].colors["black"])
