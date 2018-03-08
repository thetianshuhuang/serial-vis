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

    frame_times = {}

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
        self.screen = pygame.display.set_mode(
            self.settings["main"].window_size)
        pygame.display.set_caption(self.settings["main"].caption)
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
               current_event.key in self.settings["main"].events):
                triggered_events.append(
                    self.settings["main"].events[current_event.key])
            if(current_event.type == pygame.QUIT):
                triggered_events.append(
                    self.settings["main"].events[pygame.QUIT])

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
    def update_fps(self, instruction, device_name):

        """
        Check whether the instruction triggers an fps update.

        Parameters
        ----------
        instruction: array following instruction form
            instruction to be checked
        """

        # initialize frame times for new device
        if device_name not in self.frame_times:
            self.frame_times.update({device_name: []})

        # update frame times
        if(instruction[0] == self.settings[device_name].fps_count_keyword):
            self.frame_times[device_name].append(time.time())
            if(len(self.frame_times[device_name]) >
               self.settings[device_name].fps_smooth_size):
                del self.frame_times[device_name][0]

    #   --------------------------------
    #
    #   Compute fps from the registry
    #
    #   --------------------------------

    def compute_fps(self, device):

        """
        Returns the current fps.

        Returns
        -------
        float
            fps, smoothed over settings.frame_smooth_size frames
        """

        if(device not in self.frame_times):
            return(0)

        elif(len(self.frame_times[device]) < 2):
            return(0)

        return(len(self.frame_times[device]) /
               (self.frame_times[device][-1] - self.frame_times[device][0]))
