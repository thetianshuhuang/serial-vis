# serial_parser.py
# serial command interpretation class

from error_handler import *
from hexutil import *


#   --------------------------------
#
#   ASCII Serial command parser
#
#   --------------------------------

class bin_parser:

    """
    ASCII Serial command parser class

    Attributes
    ----------
    opcodes : dict
        Definition of each opcode. Opcodes are one byte, 0x00 to 0xFF.
    commands : dict
        Format for registered commands

    Created by __init__:
    error_handler : error_handler object
        Centralized error handling
    """

    # default opcode dictionary
    opcodes = {
        0x00: "draw",
        0x01: "logs",
        0x02: "logf",
        0x03: "logstart",
        0x04: "logend",
        0x05: "echo",
        0x06: "null",
        0x07: "definecolor",
        0x08: "setscale",
        0x09: "setoffset",
        0x0A: "drawline",
        0x0B: "drawlinep",
        0x0C: "drawcircle",
        0x0D: "drawray",
        0x0E: "text",
        0x0F: "textp"
    }

    # default command dictionary
    commands = {
        # control commands:
        # draw
        "draw": [],
        # logs: label, datastring
        "logs": ["s", "s"],
        # logf: label, data (float)
        "logf": ["s", "f"],
        # start log block
        "logstart": [],
        # end log block
        "logend": [],
        # print to console
        "echo": ["s"],
        # null argument
        "null": [],

        # drawing commands:
        # define color: name, (r,g,b)
        "definecolor": ["s", "dd"],
        # set scale: ratio
        "setscale": ["f"],
        # set offset: (x,y)
        "setoffset": ["dd"],
        # draw line: (x_1,y_1),(x_2,y_2),color
        "drawline": ["ff", "ff", "s"],
        # draw line (pixel mode): (x_1,y_1),(x_2,y_2),color
        "drawlinep": ["dd", "dd", "s"],
        # draw circle: (x,y),r,color
        "drawcircle": ["ff", "f", "s"],
        # draw ray: (x,y),angle,radius,color
        "drawray": ["ff", "f", "f", "s"],
        # draw text: text,(x,y),size,color
        "text": ["s", "ff", "d", "s"],
        # draw text (pixel mode): text,(x,y),size,color
        "textp": ["s", "dd", "d", "s"],
    }

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, commands, settings):

        """
        Create a serial parser object

        Parameters
        ----------
        commands : dict
            User defined command formats; merged with commands.
        settings : sv_settings object
            Object containing program settings
        """

        self.commands.update(commands)
        self.settings = settings

        self.error_handler = error_handler(settings)
