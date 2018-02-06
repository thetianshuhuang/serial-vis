# vector_graphics_window.py
# vector graphics base class

from base_graphics import *


#   --------------------------------
#
#   Vector graphics window
#
#   --------------------------------

class vector_graphics_window(base_graphics):

    """
    Pygame window class; creates vector graphics rendering window
    Extends base_graphics

    Attributes
    ----------
    current_buffer_id : int
        current buffer being displayed. -1 = error.
    """

    current_buffer_id = -1

    #   --------------------------------
    #
    #   Update screen
    #
    #   --------------------------------
    def update_screen(self, frame_buffer):

        """
        Update a screen with the given frame_buffer.

        Parameters
        ----------
        frame_buffer: buffer.frame_buffer
            instruction buffer to be displayed

        Returns
        -------
        Bool
            True if the update operation redrew the screen; False otherwise
        """

        # return false if unsuccessful.
        if(frame_buffer.frame_id == self.current_buffer_id):
            return(False)

        # otherwise, draw the buffer
        else:
            self.current_buffer_id = frame_buffer.frame_id

            # clear pygame buffer
            self.screen.fill(self.settings.colors["background"])

            # show underlay
            self.show_underlay()

            for instruction in frame_buffer.instructions:

                # run through default draw functions
                try:
                    draw_function = getattr(self, instruction[0])
                    draw_function(instruction)
                # raise AttributeError
                # if the requested instruction doesn't exist.
                except AttributeError:
                    self.error_handler.raise_error(
                        "onf", instruction, instruction[0])

            # show frame id and fps
            if(self.settings.show_frame_id):
                self.show_frame_id()
            if(self.settings.show_fps):
                self.show_fps()

            # show overlay
            self.show_overlay()

            # display pygame buffer
            pygame.display.flip()

            # limit the fps
            self.clock.tick(self.settings.frame_limit)

            return(True)

    #   --------------------------------
    #
    #   Display fps and frame id
    #
    #   --------------------------------
    def show_frame_id(self):

        """
        Display the frame ID at the top left.
        """

        textfont = pygame.font.SysFont(self.settings.font, 12)
        textframe = textfont.render(
            "ID=" + str(self.current_buffer_id),
            False,
            self.settings.colors["black"])
        self.screen.blit(textframe, (10, 10))

    def show_fps(self):

        """
        Display the current fps at the bottom left.
        """

        textfont = pygame.font.SysFont(self.settings.font, 12)
        textframe = textfont.render(
            "fps=" + str(round(self.compute_fps(), 2)),
            False,
            self.settings.colors["black"])
        self.screen.blit(textframe, (10, self.settings.window_size[1] - 22))

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
    def get_color(self, colorname):

        """
        Safely get the color specified by colorname.

        Parameters
        ----------
        colorname : str
            Name of the desired color

        Returns
        -------
        int[3]: (R,G,B)
            Tuple specifing the color definition
        """

        try:
            return(self.settings.colors[colorname])
        except KeyError:
            return(self.settings.colors["black"])
