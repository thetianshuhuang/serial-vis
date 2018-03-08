# buffer_manager.py
# serial_vis specific buffer management

from buffer import *
import buffer_io


#   --------------------------------
#
#   Serial-vis specific buffer manager
#
#   --------------------------------
class buffer_manager:

    """
    Serial-vis specific buffer management

    Attributes
    ----------
    is_live : bool
        Is the current display buffer live?
    display_buffer_id : int
        id of currently displayed buffer, relative to the current center buffer
        (most recent, or where the stream was paused)
    """

    is_live = True
    display_buffer_id = {"main": 0}

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, settings, error_handler):

        """
        Create buffer manager

        Parameters
        ----------
        settings : settings object
            settings object for serial vis
        error_handler : error_handler object
            centralized error handler
        """

        # set up settings
        self.settings = settings

        # set up buffer db
        self.buffer_db = {"main": buffer_db(self.settings["main"])}

        # set up error handler
        self.error_handler = error_handler

        # set up initial frame buffer
        self.current_buffer = frame_buffer()

    #   --------------------------------
    #
    #   Update current buffer
    #
    #   --------------------------------
    def update(self, target, instruction):

        """
        Update the current buffer.

        Parameters
        ----------
        target : str
            string naming the target buffer db
        instruction : array
            array containing the instruction to be processed
        """

        # check for new target
        if target not in self.buffer_db:
            self.buffer_db.update({target: buffer_db(self.settings[target])})

        # check for control instructions:
        if(instruction[0] == "draw" and self.settings["main"].enable_graphics):

            # live => create new buffer
            # set the current view
            if(self.is_live):
                self.buffer_db[target].new_buffer(self.current_buffer)
                self.buffer_db[target].set_current_view()
            # not live => create new buffer
            # do not set current view
            else:
                self.buffer_db[target].new_buffer(self.current_buffer)

            # create new frame buffer
            self.current_buffer = frame_buffer()

        # trigger instruction
        elif(instruction[0] == "trigger"):
            self.is_live = False
            self.display_buffer_id.update({target: 0})

        # otherwise, add it to current buffer
        else:
            self.current_buffer.add_instruction(instruction)

    #   --------------------------------
    #
    #   Get the currently selected buffer
    #
    #   --------------------------------
    def get_buffer(self, target):

        """
        Get the currently selected buffer.

        Returns
        -------
        buffer object
            buffer object corresponding to the current buffer ID
        """

        return(
            self.buffer_db[target].get_buffer(
                self.display_buffer_id[target], relative=True))

    #   --------------------------------
    #
    #   Buffer controls
    #
    #   --------------------------------
    def change_buffer(self, index, target):

        """
        Change the current buffer.

        parameters
        ----------
        index : int
            relative change in index. If index=0, toggle live mode.
        """

        if(index == 0):
            self.is_live = not self.is_live
            if(self.is_live):
                self.display_buffer_id[target] = 0

        else:
            # can only change buffer when not live
            if not self.is_live:
                self.display_buffer_id[target] += index

            # check for out of bounds
            if(self.display_buffer_id[target] >
               self.settings[target].max_size_forward):

                self.display_buffer_id[target] = (
                    self.settings[target].max_size_forward)

            if(self.display_buffer_id[target] <
               -self.settings[target].max_size_backward):

                self.display_buffer_id[target] = (
                    -self.settings[target].max_size_backward)

            if(self.buffer_db[target].view_buffer +
               self.display_buffer_id[target] < 0):

                self.display_buffer_id[target] = (
                    -self.buffer_db[target].view_buffer)

    #   --------------------------------
    #
    #   Save a selection of buffers
    #
    #   --------------------------------
    def save(self, index, filename, mode):

        """
        Save a selection of buffers

        parameters
        ----------
        index : int or int[2]
            buffer ID(s) to write
        filename : str
            filename to open and write to
        mode : str
            "a" or "w", to append or overwrite
        """

        # direct passthrough to buffer_io
        status = buffer_io.save(index, filename, self.buffer_db["main"], mode)

        # raise error if failed
        if(status in ("ioe", "stx", "nub")):
            self.error_handler.raise_error(status, [], "")

        elif(status != ""):
            self.error_handler.raise_error("unk", [], "")
