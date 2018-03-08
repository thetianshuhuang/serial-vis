# sv_command.py
# centralized command handling

import serial_lib
import graphics_lib


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

    #   --------------------------------
    #
    #   process command line command
    #
    #   --------------------------------
    def process_command(self, command):

        """
        Process command line instruction.

        Parameters
        ----------
        command : str
            Command line instruction
        """

        arguments = command.split(" ")

        # pad arguments with null strings
        for i in range(4 - len(arguments)):
            arguments.append("")

        try:
            command_function = getattr(self, "_" + arguments[0])
            command_function(arguments, command)
        except AttributeError:
            self._ELSE(arguments, command)

    #   --------------------------------
    #
    #   process event
    #
    #   --------------------------------
    def process_events(self, events):

        """
        Process keyboard instructions. Doesn't run in command mode

        Parameters
        ----------
        events : dict
            Event list from keyboard
        """

        for event in events:
            # pass to process_command
            try:
                command_function = getattr(self, "_" + event[0])
                command_function(event, "")
            except AttributeError:
                self._ELSE(event, "??")

    #   --------------------------------
    #
    #   Command line commands
    #
    #   --------------------------------
    def _ELSE(self, arguments, command):

        """
        Exception command
        """

        self.error_handler.raise_error("stx", [], command)

    def _quit(self, arguments, command):

        """
        Quit serial vis cleanly
        """

        self.quit_sv()

    def _cmd(self, arguments, command):

        """
        Enter command mode
        """

        self.command_mode = True
        # create new command line
        self.command_line = graphics_lib.command_line(self.settings["main"])

    def _disconnect(self, arguments, command):

        """
        Disconnect the current device.
        """

        # set to default if no parameter is passed
        if(arguments[1] == ""):
            arguments[1] = "main"

        if(arguments[1] in self.connect_device):
            self.connect_device[arguments[1]] = False
            self.serial_device[arguments[1]].done = True

    def _connect(self, arguments, command):

        """
        Connect a new device
        """

        # set default target to main
        if(arguments[2] == ""):
            arguments[2] = "main"

        # close existing device if it exists
        if(arguments[2] in self.connect_device and
           self.connect_device[arguments[2]]):
            self.serial_device[arguments[2]].done = True
        # otherwise, create a new entry
        else:
            # todo: separate settings
            self.settings.update({arguments[2]: self.settings["main"]})
            # declare serial advice as dict entry with None as value
            # None overwritten below
            self.serial_device.update({arguments[2]: None})
            self.connect_device.update({arguments[2]: True})

        # update path with arguments[1] if it exists
        if(arguments[1] != ""):
            self.settings[arguments[2]].path = arguments[1]

        # create new serial device instance
        self.serial_device[arguments[2]] = serial_lib.threaded_serial(
            self.settings[arguments[2]],
            self.error_handler,
            self.user_commands)
        self.serial_device[arguments[2]].start()

        # register serial device
        self.connect_device[arguments[2]] = True

    def _save(self, arguments, command):

        """
        Save a set of buffers
        """

        # if no output is specified, use the default
        if(arguments[2] == ""):
            arguments[2] = self.settings["main"].default_save_name

        # if no output mode is specified, use the default
        if(arguments[3] == ""):
            arguments[3] = self.settings["main"].default_save_mode

        # save buffers (executed through file manager)
        self.buffer_manager.save(
            eval(arguments[1]),
            arguments[2],
            arguments[3])

    def _set(self, arguments, command):

        """
        Change settings
        """

        try:
            self.settings["main"].update({arguments[1]: eval(arguments[2])})

        # handle errors
        except SyntaxError:
            self.error_handler.raise_error("stx", [], command)
        except Exception as e:
            self.error_handler.raise_error("unk", [], str(e))

    def _exec(self, arguments, command):

        """
        Execute arbitrary code
        """

        try:
            eval(arguments[1])

        # handle errors
        except SyntaxError:
            self.error_handler.raise_error("stx", [], command)
        except Exception as e:
            self.error_handler.raise_error("unk", [], str(e))

    def _pause(self, arguments, command):

        """
        Toggle live mode
        """

        self.buffer_manager.change_buffer(0, "main")

    def _view(self, arguments, command):

        """
        Change the current buffer
        """

        self.buffer_manager.change_buffer(int(float(arguments[1])), "main")
