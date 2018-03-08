# sv_settings.py
# settings storage class

import pygame
from settings_template import *


#   --------------------------------
#
#   Settings class
#
#   --------------------------------

class sv_settings(settings_template):

    """
    Settings class

    Attributes
    ----------
    Documented on the Settings wiki page.
    """

    # main
    name = "main"
    caption = "Serial Visualization"
    quit_on_disconnect = False
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
    font = "freemono"
    show_frame_id = True
    show_fps = True
    fps_count_keyword = "draw"
    fps_smooth_size = 30
    font_size = 15
    display_spacing = [10, 10, 10, 10, 10]
    events = {
        pygame.QUIT: ("quit",),
        pygame.K_SPACE: ("pause",),
        pygame.K_PERIOD: ("view", 1),
        pygame.K_LEFTBRACKET: ("view", -10),
        pygame.K_COMMA: ("view", -1),
        pygame.K_RIGHTBRACKET: ("view", 10),
        pygame.K_BACKQUOTE: ("cmd",)
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
    default_save_name = "saved_buffer.svb"
    default_save_mode = "a"

    # serial_parser
    serial_mode = "ascii"
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
        "onf": True,
        "nas": True,
        "stx": True,
        "ioe": True,
        "cto": True,
        "ddc": True,
        "nub": True,
    }
