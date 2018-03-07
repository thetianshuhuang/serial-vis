# buffer_io.py
# buffer read and write to file functions


#   --------------------------------
#
#   Save buffer range
#
#   --------------------------------
def save(index, file, buffer_db, mode):

    """
    Save a buffer or set of buffers to file.

    parameters
    ----------
    index : int or int[2]
        buffer ID(s) to write
    file : str
        filename to write to
    buffer_db : buffer database object
        buffer_db to pull buffers from
    mode : str
        "a" or "w", to append or overwrite

    returns
    -------
    str
        error code; empty if success
    """

    # ensure that the mode is either 'a' (append) or 'w' (overwrite)
    if(mode not in ('a', 'w')):
        return("stx")

    # open file
    try:
        savefile = open(file, mode)
    except IOError:
        return("ioe")
    except Exception as e:
        return(str(e))

    # single frame save
    if(type(index) == int):
        status = save_buffer(savefile, buffer_db.get_buffer(index))

    # frame range save
    elif(type(index) == list and len(index) == 2):
        status = ""

        # write each buffer
        for i in range(index[0], index[1]):
            restatus = save_buffer(savefile, buffer_db.get_buffer(i))
            if(restatus != ""):
                status = restatus

    # syntax error
    else:
        status = "stx"

    # close file
    savefile.close()

    return(status)


#   --------------------------------
#
#   Save buffer
#
#   --------------------------------
def save_buffer(file, out_buffer):

    """
    Write a buffer to the input file.

    parameters
    ----------
    file : python file object
        file to write to
    out_buffer : buffer object
        buffer to be written

    returns
    -------
    str
        error code; returns empty on success
    """

    if(out_buffer.frame_id == -1):
        return("nub")

    else:
        # write buffer ID
        file.write(str(out_buffer.frame_id) + "\n")

        # write instructions
        for instruction in out_buffer.instructions:
            file.write(str(instruction))
            # newline to mark the end of the instruction
            file.write("\n")

        # write end tag
        file.write("end\n")

        return("")


#   --------------------------------
#
#   Load buffers
#
#   --------------------------------
def load(self, file, buffer_db):

    """
    """

    pass
