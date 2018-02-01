# sv_settings.py
# settings storage class

import pygame


#   --------------------------------
#
#   Settings class
#
#   --------------------------------

class sv_settings:

    """
    Settings class

    Attributes
    ----------
    Documented in README.md, under Default Settings.
    """

    # main
    quit_on_disconnect = True
    enable_graphics = True

    # serial_device
    path = ""
    baudrate = 115200
    seek_timeout = 60
    rx_timeout = 0.1
    tx_timeout = 0.1
    encoding = "ascii"
    verify = 2
    confirmation = True

    # vector_graphics_window
    window_size = (800, 600)
    scale = 1.000
    offset = (0, 0)
    frame_limit = 60
    line_width = 2
    font = "arial"
    show_frame_id = True
    show_fps = True
    fps_count_keyword = "draw"
    fps_smooth_size = 30
    events = {
        pygame.QUIT: "quit",
        pygame.K_SPACE: "pause",
        pygame.K_PERIOD: "fwd",
        pygame.K_LEFTBRACKET: "backplus",
        pygame.K_COMMA: "back",
        pygame.K_RIGHTBRACKET: "fwdplus"
    }
    colors = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "background": (255, 255, 255)
    }

    # csv_log
    log_output_name = "serial_log.csv"
    time_format = "epoch"

    # buffer_db
    max_size_forward = 100
    max_size_backward = 100

    # serial_parser
    number_mode = "hex"

    # error_handler
    error_codes = {
        "chk": True,
        "tma": True,
        "nea": True,
        "uro": True,
        "tts": True,
        "unk": True,
        "wto": True,
        "onf": True
    }

    #   --------------------------------
    #
    #   initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        """
        Initialize sv_settings object, and merge preliminary settings

        Parameters
        ----------
        kwargs : dict
            merged with object attributes (settings).
        """

        self.attr_merge(kwargs)

    #   --------------------------------
    #
    #   update
    #
    #   --------------------------------
    def update(self, settings):
        """
        Update settings.

        Parameters
        ----------
        settings : dict
            merged with object attributes
        """

        self.attr_merge(settings)

    #   --------------------------------
    #
    #   attr_merge
    #
    #   --------------------------------
    def attr_merge(self, settings):
        """
        Update attributes of obj with corresponding values in dict.

        Parameters
        ----------
        obj
            Object to be updated
        kwargs
            dictionary to update from
        """

        for key, value in settings.items():
            setattr(self, key, value)
