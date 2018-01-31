# serial_parser.py
# serial command interpretation class

import struct
from error_handler import *


#   --------------------------------
#
#   Serial command parser
#
#   --------------------------------

class parser:

    """
    Serial command parser class

    Attributes
    ----------
    commands : dict
        Format for registered commands
    settings : dict
        Settings for command parsing

    Created by __init__:
    error_handler : error_handler object
        Centralized error handling
    """

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

    # settings
    settings = {
        "number_mode": "hex"
    }

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, commands, **kwargs):

        """
        Create a serial parser object

        Parameters
        ----------
        commands : dict
            User defined command formats; merged with commands.
        kwargs : dict
            Merged with settings
        """

        self.commands.update(commands)
        self.settings.update(kwargs)

        self.error_handler = error_handler(**kwargs)

    #   --------------------------------
    #
    #   full package of parsing and processing
    #
    #   --------------------------------
    def process_command(self, code_line):

        """
        Parse and process a line of code

        Parameters
        ----------
        code_line : str
            Raw instruction to be processed

        Returns
        -------
        array
            Processed instruction
        """

        return self.process_args(self.parse_line(code_line))

    #   --------------------------------
    #
    #   parse command into opcode and arguments
    #
    #   --------------------------------
    def parse_line(self, code_line):

        """
        Separate a line of code into its consituent arguments

        Parameters
        ----------
        code_line : str
            Raw line of code

        Returns
        -------
        str[]
            Array, where the first element is the opcode and each subsequent
            element is an argument
        """

        # intialize args as an empty array
        arguments = []

        # if a colon is not found, then the opcode has no args
        opcode_end = code_line.find(":")
        if(opcode_end == -1):
            arguments.append(code_line)

        # else, strip out the opcode
        else:
            arguments.append(code_line[0:opcode_end])
            previous_arg_end = opcode_end
            current_arg_end = code_line.find(":", opcode_end + 1)

            # then separate the arguments
            while(current_arg_end != -1):
                arguments.append(
                    code_line[previous_arg_end + 1: current_arg_end])
                previous_arg_end = current_arg_end
                current_arg_end = code_line.find(":", current_arg_end + 1)

            arguments.append(code_line[previous_arg_end + 1: len(code_line)])

        return(arguments)

    #   --------------------------------
    #
    #   process arguments into an instruction
    #
    #   --------------------------------
    def process_args(self, raw_arguments):

        """
        Process separated arguments into the correct types

        Parameters
        ----------
        raw_arguments : str[]
            Arguments in a raw string form

        Returns
        -------
        mixed array
            Processed instruction
        """

        arguments = []
        opcode = raw_arguments[0]
        arguments.append(raw_arguments[0])

        if opcode in self.commands:
            command_length = len(self.commands[opcode]) + 1
        else:
            command_length = len(raw_arguments)

        n = 1
        while(n < command_length):

            try:
                # n-1 indexed since the opcode isn't included in self.commands
                argument_type = self.commands[opcode][n - 1]
            except IndexError:
                self.error_handler.raise_error("tma", raw_arguments)
                argument_type = "ERR"
            except KeyError:
                self.error_handler.raise_error("onr", raw_arguments)
                argument_type = "ERR"
            # protection against insufficient arguments
            if(n >= len(raw_arguments)):
                self.error_handler.raise_error("nea", raw_arguments)
                raw_arguments.append(0)

            # single argument type
            if(argument_type == "d"):
                arguments.append(self.to_int(raw_arguments[n]))
            elif(argument_type == "s"):
                arguments.append(raw_arguments[n])
            elif(argument_type == "f"):
                arguments.append(self.to_float(raw_arguments[n]))
            elif(argument_type == "l"):
                arguments.append(
                    self.to_long(raw_arguments[n], raw_arguments[n + 1]))

            # array argument type
            elif(len(argument_type) == 2):
                # separate array elements first
                argument_array_raw = []
                previous_arg_end = 0
                current_arg_end = 0
                while(current_arg_end != -1):
                    current_arg_end = raw_arguments[n].find(
                        ",", previous_arg_end)
                    if(current_arg_end != -1):
                        argument_array_raw.append(
                            raw_arguments[n]
                            [previous_arg_end: current_arg_end])
                        previous_arg_end = current_arg_end + 1
                    else:
                        argument_array_raw.append(
                            raw_arguments[n][previous_arg_end:])

                # parse each element in the array
                argument_array = []
                for element in argument_array_raw:
                    if(argument_type == "dd"):
                        argument_array.append(self.to_int(element))
                    elif(argument_type == "ss"):
                        argument_array.append(element)
                    elif(argument_type == "ff"):
                        argument_array.append(self.to_float(element))
                    elif(argument_type == "ll"):
                        pass
                        # unimplemented

                # padd errored out arrays to make then sufficiently long
                if(len(argument_array) <= 1):
                    argument_array += [0, 0]

                # finally, append the array to the arguments
                arguments.append(argument_array)

            # empty type, for when one arg takes up two spaces
            elif(argument_type == "_"):
                arguments.append(0)
            # error type, when the type doesn't match
            else:
                arguments.append("ERR")

            n += 1

        return(arguments)

    #   --------------------------------
    #
    #   argument conversion routines
    #
    #   --------------------------------

    # If number_mode == "dec", run normal python routines.
    # If number_mode == "hex", run conversion routines in hexutil.py

    def to_int(self, string):

        """
        Convert to integer

        Parameters
        ----------
        string : str
            Input string to be converted

        Returns
        -------
        int
            Converted string
        """

        if(self.settings["number_mode"] == "dec"):
            try:
                return(int(string))
            except ValueError:
                return(0)
            return(0)
        # todo: add signed int support
        elif(self.settings["number_mode"] == "hex"):
            try:
                return(int(string, 16))
            except ValueError:
                return(0)
        return(0)

    def to_float(self, string):

        """
        Convert to float

        Parameters
        ----------
        string : str
            Input string to be converted

        Returns
        -------
        float
            Converted string
        """

        if(self.settings["number_mode"] == "dec"):
            try:
                return(float(string))
            except ValueError:
                return(0.0)
            return(0.0)
        elif(self.settings["number_mode"] == "hex"):
            try:
                if(len(string) == 8):
                    return(struct.unpack('!f', string.decode("hex"))[0])
                elif(len(string) == 16):
                    return(struct.unpack('!d', string.decode("hex"))[0])
            except TypeError:
                return(0.0)
        return(0)

    # deprecated conversion for embedded systems that do not support long
    # no longer used since hex conversion is now supported.
    def to_long(self, big_string, small_string):
        return(self.to_int(big_string) * 10000 + self.to_int(small_string))
