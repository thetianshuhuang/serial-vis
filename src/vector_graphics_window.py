# vector_graphics_window.py
# vector graphics base class

import pygame
import collections
import time


class vector_graphics_window:

    """
    Pygame window class; creates vector graphics rendering window

    Attributes
    ----------
    settings : dict
        Contains window settings. Documented in README.md
    current_buffer_id : int
        current buffer being displayed. -1 = error.
    events_previous : str[]
        previously registered events
    frame_times : float[]
        log of the past settings["fps_smooth_size"] frames.
    """

    settings = {
        "window_size": (800, 600),
        "scale": 1.000,
        "offset": (0, 0),
        "frame_limit": 60,
        "line_width": 2,
        "font": "arial",
        "show_frame_id": True,
        "show_fps": True,
        "fps_count_keyword": "draw",
        "fps_smooth_size": 30,
        "events": {
            pygame.QUIT: "quit",
            pygame.K_SPACE: "pause",
            pygame.K_PERIOD: "fwd",
            pygame.K_LEFTBRACKET: "fwdplus",
            pygame.K_COMMA: "back",
            pygame.K_RIGHTBRACKET: "backplus"
        },
        "colors": {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "background": (255, 255, 255)
        },
    }

    current_buffer_id = -1
    events_previous = {}
    frame_times = []

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        """
        Create a pygame graphics window.

        Parameters
        ----------
        kwargs: dict
            passed on to settings
        """
        dict_merge(self.settings, kwargs)

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.settings["window_size"])
        self.clock = pygame.time.Clock()

        # set up previous event states
        for key in self.settings["events"]:
            self.events_previous.update({key: False})

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
            self.screen.fill(self.settings["colors"]["background"])

            for instruction in frame_buffer.instructions:

                # run through default draw functions
                try:
                    draw_function = getattr(self, instruction[0])
                    draw_function(instruction)
                # raise AttributeError
                # if the requested instruction doesn't exist.
                except AttributeError:
                    self.instruction_error(instruction)

            # show frame id and fps
            if(self.settings["show_frame_id"]):
                self.show_frame_id()
            if(self.settings["show_fps"]):
                self.show_fps()

            # display pygame buffer
            pygame.display.flip()

            # limit the fps
            self.clock.tick(self.settings["frame_limit"])

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

        current_events_hold = []
        current_events_press = []
        for event_key in self.settings["events"]:
            if event_key in pygame.event.get():
                # key pressed -> is being held
                current_events_hold += self.settings["events"][event_key]
                # previously key is not pressed -> begin keypresspas
                if(not self.events_previous[event_key]):
                    current_events_press += self.settings["events"][event_key]
                # set previous state
                self.events_previous[event_key] = True
            else:
                # set previous state
                self.events_previous[event_key] = False

        return((current_events_hold, current_events_press))

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
    #   Display Error
    #
    #   --------------------------------
    def instruction_error(self, instruction):

        """
        Display an unrecognized opcode error.

        Parameters
        ----------
        instruction: array following instruction form
            instruction containing an opcode error
        """

        print("Unrecognized Opcode: " + instruction[0])

    #   --------------------------------
    #
    #   Display fps and frame id
    #
    #   --------------------------------
    def show_frame_id(self):

        """
        Display the frame ID at the bottom left.
        """

        textfont = pygame.font.SysFont(self.settings["font"], 12)
        textframe = textfont.render(
            str(self.current_buffer_id),
            False,
            self.settings["colors"]["black"])
        self.screen.blit(textframe, (10, 10))

    def show_fps(self):

        """
        Display the current fps at the bottom.
        """

        textfont = pygame.font.SysFont(self.settings["font"], 12)
        textframe = textfont.render(
            str(self.compute_fps()),
            False,
            self.settings["colors"]["black"])
        self.screen.blit(textframe, (10, self.settings["window_size"][1] - 12))

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

        if(instruction[0] == self.settings["fps_count_keyword"]):
            self.frame_times.append(time.time())
            if(len(self.frame_times) > self.settings["fps_smooth_size"]):
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
            fps, smoothed over settings["frame_smooth_size"] frames
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
        try:
            return(self.settings["colors"][colorname])
        except KeyError:
            return(self.settings["colors"]["black"])

#   --------------------------------
#
#   dict_merge
#
#   --------------------------------

#   written by https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead
    of updating only top-level keys, dict_merge recurses down into dicts
    nested to an arbitrary depth, updating keys. The ``merge_dct`` is
    merged into ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.iteritems():
        if(k in dct and
           isinstance(dct[k], dict) and
           isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
