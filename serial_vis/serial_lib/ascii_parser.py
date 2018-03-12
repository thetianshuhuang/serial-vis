# serial_parser.py
# serial command interpretation class

from .hexutil import *


#   --------------------------------
#
#   ASCII Serial command parser
#
#   --------------------------------

class ascii_parser:

    """
    ASCII Serial command parser class

    Attributes
    ----------
    commands : dict
        Format for registered commands

    Created by __init__:
    error_handler : error_handler object
        Centralized error handling
    settings : sv_settings object
        Program settings
    """

    # default command dictionary
    commands = {
        # control commands:
        # draw
        "draw": [],
        # trigger immediate pause
        "trigger": [],
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
    def __init__(self, commands, settings, error_handler):

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

        self.error_handler = error_handler

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
                self.error_handler.raise_error(
                    "tma", raw_arguments, raw_arguments[0])
                argument_type = "ERR"
            except KeyError:
                self.error_handler.raise_error(
                    "onr", raw_arguments, raw_arguments[0])
                argument_type = "ERR"
            # protection against insufficient arguments
            if(n >= len(raw_arguments)):
                self.error_handler.raise_error(
                    "nea", raw_arguments, raw_arguments[0])
                raw_arguments.append(0)

            # single argument type
            if(argument_type == "d"):
                arguments.append(
                    to_int(raw_arguments[n], self.settings.number_mode))
            elif(argument_type == "s"):
                arguments.append(raw_arguments[n])
            elif(argument_type == "f"):
                arguments.append(
                    to_float(raw_arguments[n], self.settings.number_mode))
            elif(argument_type == "l"):
                arguments.append(
                    to_long(
                        raw_arguments[n],
                        raw_arguments[n + 1],
                        self.settings.number_mode))

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
                        argument_array.append(
                            to_int(element, self.settings.number_mode))
                    elif(argument_type == "ss"):
                        argument_array.append(element)
                    elif(argument_type == "ff"):
                        argument_array.append(
                            to_float(element, self.settings.number_mode))
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
