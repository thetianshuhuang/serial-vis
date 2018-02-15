# buffer_manager.py
# serial_vis specific buffer management

from buffer import *


class buffer_manager:

    """
    """

    is_live = True
    display_buffer_id = 0

    def __init__(self, settings):
        """
        """

        # set up buffer db
        self.buffer_db = buffer_db(self.settings)

        # set up initial frame buffer
        self.current_buffer = frame_buffer()

    def update(self, instruction):

        """
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
            self.current_buffer = graphics_lib.frame_buffer()

        # trigger instruction
        elif(instruction[0] == "trigger"):
            self.is_live = False
            self.display_buffer_id = 0

        # otherwise, add it to current buffer
        else:
            self.current_buffer.add_instruction(instruction)

    def get_buffer(self):

        """
        """

        return(
            self.buffer_db.get_buffer(
                self.display_buffer_id, relative=True))

    def check_controls(self, events):

        """
        """

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
