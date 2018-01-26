# csv_logger.py
# creates csv output log

import time


# csv logging class

# methods:
# __init__      - takes **kwargs with attributes
#               - log_output_name, time_format
# close_file    - cleanly close file
# log_data      - log data in csv; auto-generates timestamp
#               - input is in instruction format:
#               - [opcode, [data]]
#               - where opcode can be "log", "logstart", or "logend"

class csv_log:

    #   --------------------------------
    #
    #   Attributes
    #
    #   --------------------------------

    settings = {
        "log_output_name": "serial_log.csv",
        "time_format": "epoch"}

    #   --------------------------------
    #
    #   initialization
    #
    #   --------------------------------
    def __init__(self, **kwargs):

        # update settings with kwargs
        self.settings.update(kwargs)

        # set cache
        self.logblock_in_progress = False
        self.logcache = []
        self.logcache_time = 0

        # open output file
        self.log_output_file = open(self.settings["log_output_name"], 'w')

    #   --------------------------------
    #
    #   clean exit
    #
    #   --------------------------------
    def close_file(self):
        self.log_output_file.close()

    #   --------------------------------
    #
    #   log data
    #
    #   --------------------------------
    def log_data(self, instruction):

        # logstart opcode: start a log block
        if(instruction[0] == "logstart"):
            # set flag
            self.logblock_in_progress = True
            # record start time
            self.logcache_time = self.get_time()
            # clear cache
            self.logcache = []

        # logend opcode is called:
        elif(instruction[0] == "logend"):
            # clear flag
            self.logblock_in_progress = False

            # write each entry
            for datatype in self.logcache:
                self.log_output_file.write(self.logcache_time)
                for entry in datatype:
                    self.log_output_file.write(",", entry)
                self.log_output_file.write("\n")

        # if a log block is in progress:
        elif(self.logblock_in_progress):

            # see if it matches an existing entry in the cache
            match = False
            for datatype in self.logcache:
                # match -> insert
                if(instruction[1] == datatype[0]):
                    datatype.append(instruction[2])
                    match = True
            # no match -> create new entry
            if(not match):
                self.logcache.append([instruction[1], instruction[2]])

        # no log block in progress => log normally.
        elif(not self.logblock_in_progress):
            timestamp = self.get_time()

            writeline = (timestamp + "," +
                         instruction[1] + "," +
                         instruction[2] + "\n")

            self.log_output_file.write(writeline)

    #   --------------------------------
    #
    #   get time and format appropriately
    #
    #   --------------------------------
    def get_time(self):

        epoch_time = time.time()

        if(self.settings["time_format"] == "epoch"):
            return(str(epoch_time))

        # todo: other time formats
