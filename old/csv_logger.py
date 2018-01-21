import time


# csv logging class
class csv_logger:


    #   --------------------------------
    #
    #   Attributes
    #
    #   --------------------------------
    settings = {"log_output_name": "serial_log.csv"}

    #   --------------------------------
    #
    #   initialization
    #
    #   --------------------------------
	def __init__(self,settings)

        # update user settings
        self.settings.update(settings)

		# set up caching information
		self.logblock_in_progress = False
        self.logcache = []
        self.logcache_time = "0"

        # open the output file
        self.log_output_file = open(self.settings["log_output_name"],'w')


    #   --------------------------------
    #
    #   clean exit
    #
    #   --------------------------------
    def closefile(self):
    	self.log_output_file.close()


    #   --------------------------------
    #
    #   log data given in a log opcode.
    #
    #   --------------------------------
    def log_data(self,instruction):

        # logstart opcode is called
        if(instruction[0] == "logstart"):
            # set flag
            self.logblock_in_progress == True
            # record start time
            self.logcache_time = str(time.time())
            # clear cache
            self.logcache = []

        # logend opcode is called, 
        elif(instruction[0] == "logend"):
            # clear flag
            self.logblock_in_progress == False
            
            # write each entry
            for datatype in self.logcache:
                self.log_output_file.write(self.logcache_time)
                for entry in datatype:
                    self.log_output_file.write(",",entry)
                self.write("\n")

        # if a log block is in progress:
        elif(self.logblock_in_progress == True):

            # see if it matches an existing entry in the cache
            match = False
            for datatype in self.logcache:
                # match -> insert
                if(instruction[1] == datatype[0]):
                    datatype.append(instruction[2])
                    match = True
            # no match -> create new entry
            if(match == False):
                self.logcache.append([instruction[1],instruction[2]])

        # no log block in progress => log normally.
        elif(self.logblock_in_progress == False):
            timestamp = str(time.time())

            writeline = timestamp + "," + instruction[1] + "," + instruction[2] + "\n"
            self.log_output_file.write(writeline)