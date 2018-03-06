# buffer_io.py
# buffer read and write to file functions


#   --------------------------------
#
#   Save buffer range
#
#   --------------------------------
def save(index, file, buffer_db, mode):

    """
    """
    # todo: raise errors as appropriate

    # ensure that the mode is either 'a' (append) or 'w' (overwrite)
    if(mode not in ('a', 'w')):
        return(False)

    # open file
    savefile = open(file, mode)

    # single frame save
    if(type(index) == int):
        status = save_buffer(savefile, buffer_db.get_buffer(index))

    # frame range save
    elif(type(index) == list and len(index) == 2):
        status = True

        # write each buffer
        for i in range(index[0], index[1]):
            status &= save_buffer(savefile, buffer_db.get_buffer(i))

    # syntax error
    else:
        status = False

    # close file
    savefile.close()

    return(status)


#   --------------------------------
#
#   Save buffer
#
#   --------------------------------
def save_buffer(file, out_buffer):

    if(out_buffer.frame_id == -1):
        return(False)

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

        return(True)


#   --------------------------------
#
#   Load buffers
#
#   --------------------------------
def load(self, file, buffer_db):

    """
    """

    pass
