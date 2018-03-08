# buffer.py
# frame buffer storage class

import time


#   --------------------------------
#
#   Frame buffer
#
#   --------------------------------

class frame_buffer:

    """
    Frame buffer storage class; create and maintain a single frame buffer

    Attributes
    ----------
    frame_id : int
        Frame ID of the stored frame. Is set to -1 if unknown.
    timestamp : float
        time that the buffer was created
    instructions : instruction[]
        Mixed arrays containing instructions in the buffer.
    """

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        """
        Create a frame_buffer instance

        Parameters
        ----------
        kwargs: dict
            frame_id=: set frame ID if known; otherwise defaults to -1
        """

        # attributes
        self.frame_id = -1
        self.timestamp = time.time()
        self.instructions = []

        # add frame_id attribute if provided
        if("frame_id" in kwargs):
            self.frame_id = kwargs["frame_id"]

    #   --------------------------------
    #
    #   Add instruction to buffer class
    #
    #   --------------------------------
    def add_instruction(self, instruction):

        """
        Add instruction to buffer instance

        Parameters
        ----------
        instruction: mixed array
            instruction to be added to the buffer.
        """

        self.instructions += [instruction]


#   --------------------------------
#
#   Buffer database
#
#   --------------------------------

class buffer_db:

    """
    Buffer database; frame buffer tracking and storage class

    Attributes
    ----------
    input_buffer : int
        ID of the next buffer to be created
    view_buffer : int
        ID of the buffer that the current view is centered on
    frame_buffers : dict
        Frames currently being tracked, keyed by their frame ID
    """

    input_buffer = 0
    view_buffer = 0
    frame_buffers = {}

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, settings):

        """
        Initialize frame buffer database

        Parameters
        ----------
        settings : sv_settings object
            object containing program settings
        """

        self.settings = settings

    #   --------------------------------
    #
    #   Register new buffer
    #
    #   --------------------------------
    def new_buffer(self, frame_buffer):

        """
        Register a new buffer to the database, and delete old ones.

        Parameters
        ----------
        frame_buffer : instance of frame_buffer class
            frame_buffer to be added to the database

        Returns
        -------
        int
            ID of the registered buffer
        """

        # add new item if the current forward limit hasn't been exceeded
        # use the buffer ID as a key
        if(self.input_buffer <=
           self.view_buffer + self.settings.max_size_forward):
            # assign a frame id if not already assigned.
            if(frame_buffer.frame_id == -1):
                frame_buffer.frame_id = self.input_buffer
            # update frame buffers
            self.frame_buffers.update(
                {self.input_buffer: frame_buffer})

        # scan for old frame buffers and delete them
        for element in self.frame_buffers.keys():
            if(element < self.view_buffer - self.settings.max_size_forward):
                del self.frame_buffers[element]

        # increment the current input buffer ID
        self.input_buffer += 1

        # return the buffer ID that just got created
        return(self.input_buffer)

    #   --------------------------------
    #
    #   Get buffer at ID
    #
    #   --------------------------------
    def get_buffer(self, index, **kwargs):

        """
        Get buffer at the input ID in relative or absolute mode

        Parameters
        ----------
        index : int
            frame ID in either relative or absolute mode
        kwargs : dict
            relative=True if relative

        Returns
        -------
        frame_buffer
            Frame buffer class; is empty if the requested buffer does not exist
        """

        # build buffer index
        get_id = index
        if("relative" in kwargs and kwargs["relative"]):
            get_id += self.view_buffer

        # check for index out of bounds
        if(get_id > self.view_buffer + self.settings.max_size_forward):
            index = self.settings.max_size_forward
        elif(get_id < self.view_buffer - self.settings.max_size_backward):
            index = -self.settings.max_size_backward

        # fetch the actual buffer
        if(self.input_buffer == 0):
            return(frame_buffer(frame_id=-1))
        else:
            try:
                return(self.frame_buffers[get_id])
            # catch KeyErrors due to jumping to the most recent frame
            # before the frame has been built
            except KeyError:
                return(frame_buffer(frame_id=-1))

    #   --------------------------------
    #
    #   Set current view
    #
    #   --------------------------------
    def set_current_view(self, **kwargs):

        """
        Set the current view ID (not necessarily the display ID).

        Parameters
        ----------
        kwargs : dict
            Options - absolute= to set view ID to that value
                      relative= to set view ID to that value relative to input
            Leave kwargs blank to set view_buffer to input_buffer - 1
        """

        if "absolute" in kwargs:
            self.view_buffer = kwargs["absolute"]
        elif "relative" in kwargs:
            self.view_buffer = kwargs["relative"] + self.input_buffer
        else:
            self.view_buffer = self.input_buffer - 1

    #   --------------------------------
    #
    #   Get current ID
    #
    #   --------------------------------
    def get_buffer_info(self):

        """
        Get the current view buffer ID and input buffer ID.

        Returns
        -------
        int[]
            (view_buffer, input_buffer - 1)
        """

        # self.input_buffer is the next key to be created
        # not the most recently created key
        return((self.view_buffer, self.input_buffer - 1))
