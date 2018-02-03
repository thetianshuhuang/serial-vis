# vector_graphics_window.py
# vector graphics base class

import pygame
import time


#   --------------------------------
#
#   Vector graphics window
#
#   --------------------------------

class vector_graphics_window:

    """
    Pygame window class; creates vector graphics rendering window

    Attributes
    ----------
    current_buffer_id : int
        current buffer being displayed. -1 = error.
    frame_times : float[]
        log of the past settings.fps_smooth_size frames.

    Created by __init__:
    screen : pygame.display
        main pygame display
    clock : pygame.clock
        pygame timing class
    error_handler : error_handler object
        error handler class
    """

    current_buffer_id = -1
    frame_times = []

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, settings, error_handler):

        """
        Create a pygame graphics window.

        Parameters
        ----------
        settings: sv_settings object
            object containing settings to be used
        """

        self.settings = settings

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.settings.window_size)
        pygame.display.set_caption(self.settings.path)
        self.clock = pygame.time.Clock()

        self.error_handler = error_handler

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

            # display pygame buffer
            pygame.display.flip()

            # limit the fps
            self.clock.tick(self.settings.frame_limit)

            return(True)

    #   --------------------------------
    #
    #   Check events; return list of events
    #
    #   --------------------------------
    def check_events(self):

        """
        Returns a list of the names of current events.
        """

        # get currently pressed keys
        current_events_hold = []
        pressed_keys = pygame.key.get_pressed()
        for event in self.settings.events:
            if(pressed_keys[event]):
                current_events_hold.append(
                    self.settings.events[event])

        # get just pressed keys
        current_events_keydown = []
        for current_event in pygame.event.get():
            if(current_event.type == pygame.KEYDOWN and
               current_event.key in self.settings.events):
                current_events_keydown.append(
                    self.settings.events[current_event.key])
            if(current_event.type == pygame.QUIT):
                current_events_keydown.append(
                    self.settings.events[pygame.QUIT])

        return((current_events_hold, current_events_keydown))

    #   --------------------------------
    #
    #   Close window
    #
    #   --------------------------------
    def close_window(self):

        """
        Cleanly closes the pygame window.
        """

        pygame.display.quit()
        pygame.quit()

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
    #   Check for update to fps registry
    #
    #   --------------------------------
    def update_fps(self, instruction):

        """
        Check whether the instruction triggers an fps update.

        Parameters
        ----------
        instruction: array following instruction form
            instruction to be checked
        """

        if(instruction[0] == self.settings.fps_count_keyword):
            self.frame_times.append(time.time())
            if(len(self.frame_times) > self.settings.fps_smooth_size):
                del self.frame_times[0]

    #   --------------------------------
    #
    #   Compute fps from the registry
    #
    #   --------------------------------

    def compute_fps(self):

        """
        Returns the current fps.

        Returns
        -------
        float
            fps, smoothed over settings.frame_smooth_size frames
        """
        if(self.frame_times[-1] == self.frame_times[0]):
            return(0)

        return(len(self.frame_times) /
               (self.frame_times[-1] - self.frame_times[0]))

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
