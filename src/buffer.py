# buffer.py
# frame buffer storage class


# structure containing buffer information

# methods:
# __init__              - create frame_buffer
#                       - optional: id= sets the frame ID; -1 = unknown
# add_instruction       - adds instruction to instruction list

class frame_buffer:

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        # attributes
        self.frame_id = -1
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
        self.instructions += [instruction]

# class containing a collection of frame buffers,
# along with related methods
class buffer_db:

    #   --------------------------------
    #
    #   Attributes
    #
    #   --------------------------------

    settings = {"max_size_forward": 100,
                "max_size_backward": 100}

    input_buffer = 0
    view_buffer = 0
    frame_buffers = {}

    #   --------------------------------
    #
    #   Initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        # update settings
        self.settings.update(kwargs)

    #   --------------------------------
    #
    #   Register new buffer
    #
    #   --------------------------------

    #   Adds a new frame_buffer object to the frame_buffers.
    def new_buffer(self, frame_buffer):

        # add new item if the current forward limit hasn't been exceeded
        # use the buffer ID as a key
        if(self.input_buffer <
           self.view_buffer + self.settings["max_size_forward"]):
            # assign a frame id if not already assigned.
            if(frame_buffer.frame_id == -1):
                frame_buffer.frame_id = self.input_buffer
            # update frame buffers
            self.frame_buffers.update(
                {self.input_buffer: frame_buffer})

        # scan for old frame buffers and delete them
        for element in self.frame_buffers.keys():
            if(element < self.view_buffer - self.settings["max_size_forward"]):
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

    #   takes in a buffer ID (optional: relative=True)
    #   returns ("id": absolute ID, "ops": frame_buffer)
    def get_buffer(self, index, **kwargs):

        # build buffer index
        get_id = index
        if("relative" in kwargs and kwargs["relative"]):
            get_id += self.view_buffer

        # check for index out of bounds
        if(get_id > self.view_buffer + self.settings["max_size_forward"]):
            index = self.settings["max_size_forward"]
        elif(get_id < self.view_buffer - self.settings["max_size_backward"]):
            index = -self.settings["max_size_backward"]

        # fetch the actual buffer
        if(self.input_buffer == 0):
            return(frame_buffer(frame_id=-1))
        else:
            return(self.frame_buffers[get_id])

    #   --------------------------------
    #
    #   Set current view
    #
    #   --------------------------------

    #   sets the current view ID
    #   kwargs: absolute= set buffer absolutely
    #           relative= set buffer relative to input_buffer
    def set_current_view(self, **kwargs):

        if "absolute" in kwargs:
            self.view_buffer = kwargs["absolue"]
        elif "relative" in kwargs:
            self.view_buffer = kwargs["relative"] + self.input_buffer
        else:
            self.view_buffer = self.input_buffer - 1

    #   --------------------------------
    #
    #   Get current ID
    #
    #   --------------------------------

    #   Returns (current displayed buffer, current input buffer)
    def get_buffer_info(self):

        # self.input_buffer is the next key to be created
        # not the most recently created key
        return((self.view_buffer, self.input_buffer - 1))
