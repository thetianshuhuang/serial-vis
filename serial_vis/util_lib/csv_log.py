# csv_logger.py
# creates csv output log

import time


#   --------------------------------
#
#   CSV logging class
#
#   --------------------------------

class csv_log:

    """
    CSV logging class

    Attributes
    ----------

    Created by __init__:
    logblock_in_progress : bool
        Is a data block currently in progress?
    logcache : mixed array
        Cache of logged data in the current block (if it exists)
    logcache_time : float
        Start time of a log block
    log_output_file : io file, write mode
        CSV file
    """

    #   --------------------------------
    #
    #   initialization
    #
    #   --------------------------------
    def __init__(self, settings):

        """
        Create CSV log file

        Parameters
        ----------
        settings : sv_settings object
            Object containing program settings
        """

        # get settings
        self.settings = settings

        # set cache
        self.logblock_in_progress = False
        self.logcache = []
        self.logcache_time = 0

        # open output file
        self.log_output_file = open(self.settings.log_output_name, 'a')

    #   --------------------------------
    #
    #   clean exit
    #
    #   --------------------------------
    def close_file(self):

        """
        Cleanly exit; close the log file
        """

        self.log_output_file.close()

    #   --------------------------------
    #
    #   log data
    #
    #   --------------------------------
    def log_data(self, instruction):

        """
        Log one instruction line

        Parameters
        ----------
        instruction : mixed array
            instruction to be logged
        """

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
                         str(instruction[2]) + "\n")

            self.log_output_file.write(writeline)

    #   --------------------------------
    #
    #   get time and format appropriately
    #
    #   --------------------------------
    def get_time(self):

        """
        Get the current epoch time, and format it accordingly

        Returns
        -------
        str
            Formatted time
        """

        epoch_time = time.time()

        if(self.settings.time_format == "epoch"):
            return(str(epoch_time))

        if(self.settings.time_format == "hhmmss"):
            return(time.strftime("%H:%M:%S"))
