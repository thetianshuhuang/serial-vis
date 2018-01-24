# serial_parser.py
# serial command interpretation class

import struct


# serial parser class

# methods:
# __init__              - takes commands
#                       - a dictionary containing command bindings
# process_command       - fully processes a command
#                       - from string into correctly typed array
# parse_line            - separate string into arguments
# process_args          - convert arguments into correct types
class parser:

    #   --------------------------------
    #
    #   Attributes
    #
    #   --------------------------------

    # default command dictionary
    commands = {
        # control commands:
        # draw
        "draw": [],
        # log: label, datastring
        "log": ["s", "s"],
        # start log block
        "logstart": [],
        # end log block
        "logend": [],
        # print to console
        "echo": ["s"],

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
        "number_mode": "HEX",
    }

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, commands):
        self.commands.update(commands)

    #   --------------------------------
    #
    #   full package of parsing and processing
    #
    #   --------------------------------
    def process_command(self, code_line):
        return self.process_args(self.parse_line(code_line))

    #   --------------------------------
    #
    #   parse command into opcode and arguments
    #
    #   --------------------------------
    def parse_line(self, code_line):

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
    #   process arguments into an array
    #
    #   --------------------------------
    def process_args(self, raw_arguments):

        arguments = []
        opcode = raw_arguments[0]
        arguments.append(raw_arguments[0])

        n = 1
        while(n < len(raw_arguments)):

            try:
                # n-1 indexed since the opcode isn't included in self.commands
                argument_type = self.commands[opcode][n - 1]
            except IndexError:
                print("Error: insufficient arguments")
                argument_type = "ERR"

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
                        argument_array.append(self.to_int(raw_arguments[n]))
                    elif(argument_type == "ss"):
                        argument_array.append(raw_arguments[n])
                    elif(argument_type == "ff"):
                        argument_array.append(self.to_float(raw_arguments[n]))
                    elif(argument_type == "ll"):
                        argument_array.append(
                            self.to_long(
                                raw_arguments[n], raw_arguments[n + 1]))

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
        if(self.settings["number_mode"] == "dec"):
            try:
                return(int(string))
            except ValueError:
                return(0)
            return(0)
        elif(self.settings["number_mode"] == "hex"):
            try:
                return(int(string, 16))
            except ValueError:
                return(0)
        return(0)

    def to_float(self, string):
        if(self.settings["number_mode"] == "dec"):
            try:
                return(float(string))
            except ValueError:
                return(0.0)
            return(0.0)
        elif(self.settings["number_mode"] == "hex"):
            try:
                return(struct.updack('d', string.decode("hex")))
            except TypeError:
                return(0.0)
        return(0)

    # deprecated conversion for embedded systems that do not support long
    # no longer used since hex conversion is now supported.
    def to_long(self, big_string, small_string):
        return(self.to_int(big_string) * 10000 + self.to_int(small_string))
