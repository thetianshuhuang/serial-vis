# sv_command.py
# centralized command handling

import serial_lib


#   --------------------------------
#
#   serial vis commands
#
#   --------------------------------
class sv_command:

    """
    Serial vis commands class, to be mixed in with serial_vis.
    All internal commands are prefixed with an underscore.
    """

    def _ELSE(self, arguments, command):
        self.error_handler.raise_error("stx", [], command)

    def _quit(self, arguments, command):

        """
        Quit serial vis cleanly
        """

        self.quit_sv()

    def _disconnect(self, arguments, command):

        """
        Disconnect the current device.
        """

        self.connect_device = False
        self.serial_device.done = True

    def _connect(self, arguments, command):

        # close existing device if it exists
        if(self.connect_device):
            self.serial_device.done = True

        # update path with arguments[1] if it exists
        if(arguments[1] != ""):
            self.settings.path = arguments[1]

        # create new serial device instance
        self.serial_device = serial_lib.threaded_serial(
            self.settings,
            self.error_handler,
            self.user_commands)
        self.serial_device.start()

        # register serial device
        self.connect_device = True

    def _save(self, arguments, command):

        # if no output is specified, use the default
        if(arguments[2] == ""):
            arguments[2] = self.settings.default_save_name

        # if no output mode is specified, use the default
        if(arguments[3] == ""):
            arguments[3] = self.settings.default_save_mode

        # save buffers (executed through file manager)
        self.buffer_manager.save(
            eval(arguments[1]),
            arguments[2],
            arguments[3])

    def _set(self, arguments, command):

        try:
            self.settings.update({arguments[1]: eval(arguments[2])})

        # handle errors
        except SyntaxError:
            self.error_handler.raise_error("stx", [], command)
        except Exception as e:
            self.error_handler.raise_error("unk", [], str(e))

    def _exec(self, arguments, command):
        try:
            eval(arguments[1])

        # handle errors
        except SyntaxError:
            self.error_handler.raise_error("stx", [], command)
        except Exception as e:
            self.error_handler.raise_error("unk", [], str(e))

    def _pause(self, arguments, command):
        self.buffer_manager.change_buffer(0)

    def _view(self, arguments, command):
        self.buffer_manager.change_buffer(arguments[1])
