# error_handler.py
# error handling class; handles errors and error notifications

import time


#   --------------------------------
#
#   Error handler
#
#   --------------------------------

class error_handler:

    """
    Error handler class; handles settings for error reporting

    Attributes
    ----------
    error_id : int
        ID of the current error
    error_code_definitions : dict
        definitions for error names and descriptions
    """

    error_id = 0

    error_code_definitions = {
        "chk": (
            "Error: incorrect checksum",
            "The serial communication was either incorrectly transmitted or "
            "incorrectly received.\nchecksums: &"
        ),
        "tma": (
            "Error: too many arguments",
            "The serial command has provided too many arguments for the given "
            "opcode."
        ),
        "nea": (
            "Error: not enough arguments",
            "The serial command has not provided enough arguments for the "
            "given opcode."
        ),
        "onr": (
            "Error: unregistered opcode",
            "The opcode & does not correspond to a command format in the "
            "command registry."
        ),
        "onf": (
            "Error: opcode not found",
            "The opcode is registered, but does not correspond to a valid "
            "method in graphics_class."
        ),
        "tts": (
            "Error: tuple too short",
            "A tuple provided as an argument is too short for the intended "
            "argument."
        ),
        "unk": (
            "Error: unrecognized error",
            "name = &"
        ),
        "wto": (
            "Error: serial device sending not responding to verification",
            "device = &"
        ),
        "nas": (
            "Error: attempted to encode string with non-ascii character",
            "string = &"
        ),
        "stx": (
            "Error: invalid syntax",
            "command = &"
        )
    }

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, settings):

        """
        Create an error handler.

        Parameters
        ----------
        settings : sv_settings object
            Object containing program settings
        """

        self.settings = settings

    #   --------------------------------
    #
    #   Display error
    #
    #   --------------------------------
    def raise_error(self, error_name, instruction, message):

        """
        Display an error.

        Parameters
        ----------
        error_name : str
            Error code name
        opcode : str
            Opcode that triggered the error.
        """

        # update ID
        self.error_id += 1

        # process unrecognized opcode
        if(error_name not in self.error_code_definitions):
            error_name = "unk"

        # check if the error is silenced
        if(error_name in self.settings.error_codes and
           self.settings.error_codes[error_name]):

            # print error separator
            err_info = ("[" + time.strftime("%H:%M:%S") +
                        " ID=" + str(self.error_id) + "] ")
            print(err_info + ("-" * (64 - len(err_info))))

            # print primary message
            print(self.error_code_definitions[error_name][0])

            # print command
            print(instruction)

            # print description
            index = self.error_code_definitions[error_name][1].find("&")
            if(index == -1):
                print(self.error_code_definitions[error_name][1])
            else:
                # splice in opcode at the "&" character.
                print(
                    self.error_code_definitions[error_name][1][:index] +
                    message +
                    self.error_code_definitions[error_name][1][index + 1:])
