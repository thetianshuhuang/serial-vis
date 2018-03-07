# base_graphics.py
# base graphics window; reusable for most graphics applications

import pygame
import time


#   --------------------------------
#
#   Reusable graphics window
#
#   --------------------------------

class base_graphics:

    """
    Pygame window class; base graphics window with basic utility methods

    Attributes
    ----------
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
        error_handler: error_handler object
            object containing error handling methods
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
    #   Check events; return list of events
    #
    #   --------------------------------
    def check_events(self):

        """
        Returns a list of the names of current events.

        Returns
        -------
        array
            List of triggered events as defined by settings.events
        """

        triggered_events = []
        for current_event in pygame.event.get():
            if(current_event.type == pygame.KEYDOWN and
               current_event.key in self.settings.events):
                triggered_events.append(
                    self.settings.events[current_event.key])
            if(current_event.type == pygame.QUIT):
                triggered_events.append(
                    self.settings.events[pygame.QUIT])

        return(triggered_events)

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

        if(len(self.frame_times) < 2):
            return(0)

        return(len(self.frame_times) /
               (self.frame_times[-1] - self.frame_times[0]))
