# vector_graphics_window.py

import pygame
import collections


# methods:
# __init__              - takes **kwargs containing window settings
# update_screen         - updates the screen with the input frame_buffer object
# close_window          - cleanly close pygame
# instruction_error     - display error function

class vector_graphics_window:
    """ Pygame window class; creates vector graphics rendering window

    Attributes:
        settings:
            window_size - size of pygame window
            scale - scale from raw units to pixels
            offset - offset of origin from bottom left
            frame_limit - max fps
            line_width - width of drawn lines
            font - pygame text font
            events - events (keypresses) to be checked
            colors - colors for drawing things
    """

    #   --------------------------------
    #
    #   Attributes (default)
    #
    #   --------------------------------
    settings = {
        "window_size": (800, 600),
        "scale": 1.000,
        "offset": (0, 0),
        "frame_limit": 60,
        "line_width": 2,
        "font": "arial",
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

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        dict_merge(self.settings, kwargs)

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.settings["window_size"])
        self.clock = pygame.time.Clock()

        # set up previous event states
        for key in self.settings["events"]:
            self.events_previous.update({key}, False)

    #   --------------------------------
    #
    #   Update screen
    #
    #   --------------------------------
    def update_screen(self, frame_buffer):

        # return false if unsuccessful.
        if(frame_buffer.frame_id == self.current_buffer_id):
            return(False)

        # otherwise, draw the buffer
        else:
            self.current_buffer_id = frame_buffer.frame_id

            # clear pygame buffer
            self.screen.fill(self.colors["background"])

            for instruction in frame_buffer.instructions:

                # run through default draw functions
                try:
                    draw_function = getattr(self, instruction[0])
                    draw_function(instruction)
                # raise AttributeError
                # if the requested instruction doesn't exist.
                except AttributeError:
                    self.instruction_error(instruction)

        # display pygame buffer
        pygame.display.flip()

        # limit the fps
        self.clock.tick(self.frame_limit)

    #   --------------------------------
    #
    #   Check events; return list of events
    #
    #   --------------------------------
    def check_events(self):

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

        pygame.display.quit()
        pygame.quit()

    #   --------------------------------
    #
    #   Display Error
    #
    #   --------------------------------
    def instruction_error(self, instruction):

        print("Unrecognized Opcode: " + instruction[0])


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
