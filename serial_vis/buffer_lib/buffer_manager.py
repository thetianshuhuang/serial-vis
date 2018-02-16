# buffer_manager.py
# serial_vis specific buffer management

from buffer import *


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
    display_buffer_id = 0

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
        self.buffer_db = buffer_db(self.settings)

        # set up error handler
        self.error_handler = error_handler

        # set up initial frame buffer
        self.current_buffer = frame_buffer()

    def update(self, instruction):

        """
        Update the current buffer.

        Parameters
        ----------
        instruction : array
            array containing the instruction to be processed
        """

        # check for control instructions:
        if(instruction[0] == "draw" and self.settings.enable_graphics):

            # live => create new buffer
            # set the current view
            if(self.is_live):
                self.buffer_db.new_buffer(self.current_buffer)
                self.buffer_db.set_current_view()
            # not live => create new buffer
            # do not set current view
            else:
                self.buffer_db.new_buffer(self.current_buffer)

            # create new frame buffer
            self.current_buffer = frame_buffer()

        # trigger instruction
        elif(instruction[0] == "trigger"):
            self.is_live = False
            self.display_buffer_id = 0

        # otherwise, add it to current buffer
        else:
            self.current_buffer.add_instruction(instruction)

    def get_buffer(self):

        """
        Get the currently selected buffer.

        Returns
        -------
        buffer object
            buffer object corresponding to the current buffer ID
        """

        return(
            self.buffer_db.get_buffer(
                self.display_buffer_id, relative=True))

    def check_controls(self, events):

        """
        Check events to see if the current buffer or mode should be changed

        Parameters
        ----------
        events : [events_hold, events_press]
            processed event array containing the currently held keys and the
            most recently pressed keys
        """

        (events_hold, events_press) = events

        # press key events:
        if "pause" in events_press:
            self.is_live = not self.is_live
            if(self.is_live):
                self.display_buffer_id = 0

        # controls only enabled when not live
        if not self.is_live:
            if "fwd" in events_press:
                self.display_buffer_id += 1

            if "fwdplus" in events_press:
                self.display_buffer_id += 10

            if "back" in events_press:
                self.display_buffer_id += -1

            if "backplus" in events_press:
                self.display_buffer_id += -10

        # check for out of bounds
        if (self.display_buffer_id > self.settings.max_size_forward):
            self.display_buffer_id = self.settings.max_size_forward

        if (self.display_buffer_id < -self.settings.max_size_backward):
            self.display_buffer_id = -self.settings.max_size_backward
