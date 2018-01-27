# error_handler.py
# error handling class; handles errors and error notifications

import dict_merge


class error_handler:

    settings = {
        "error_codes": {
            "tma": True,
            "nea": True,
            "uro": True,
            "tts": True,
            "unk": True
        }
    }

    error_code_definitions = {
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
        )
    }

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        dict_merge(self.settings, kwargs)

    #   --------------------------------
    #
    #   Display error
    #
    #   --------------------------------
    def raise_error(self, error_name, opcode):

        # process unrecognized opcode
        if(error_name not in self.settings["error_codes"]):
            error_name = "unk"

        # check if the error is silenced
        if(self.settings["error_codes"][error_name]):
            # print primary message
            print(self.error_code_definitions[error_name][0])

            # print description
            index = self.error_code_definitions[error_name][0].find("&")
            if(index == -1):
                print(self.error_code_definitions[error_name][1])
            else:
                # splice in opcode at the "&" character.
                print(
                    self.error_code_definitions[error_name][0][:index] +
                    opcode +
                    self.error_code_definitions[error_name][1][index + 1:])
