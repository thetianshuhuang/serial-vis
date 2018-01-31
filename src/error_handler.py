# error_handler.py
# error handling class; handles errors and error notifications

from dict_merge import *


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
    settings : dict
        settings["error_codes"] specifies whether errors should be silenced
    error_code_definitions : dict
        definitions for error names and descriptions
    """

    settings = {
        "error_codes": {
            "chk": True,
            "tma": True,
            "nea": True,
            "uro": True,
            "tts": True,
            "unk": True,
            "wto": True
        }
    }

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
        )
    }

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        """
        Create an error handler.

        Parameters
        ----------
        kwargs : dict
            Merged with settings.
        """

        dict_merge(self.settings, kwargs)

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

        # process unrecognized opcode
        if(error_name not in self.settings["error_codes"]):
            error_name = "unk"

        # check if the error is silenced
        if(self.settings["error_codes"][error_name]):
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
