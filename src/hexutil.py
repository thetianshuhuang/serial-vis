# hexutil.py
# hex processing utility functions

import struct


#   --------------------------------
#
#   argument conversion routines
#
#   --------------------------------

# If number_mode == "dec", run normal python routines.
# If number_mode == "hex", run conversion routines in hexutil.py

def to_int(string, number_mode):

    """
    Convert to integer

    Parameters
    ----------
    string : str
        Input string to be converted

    Returns
    -------
    int
        Converted string
    """

    if(number_mode == "dec"):
        try:
            return(int(string))
        except ValueError:
            return(0)
        return(0)
    elif(number_mode == "hex"):
        try:
            return(int(string, 16))
        except ValueError:
            return(0)
    return(0)


def to_float(string, number_mode):

    """
    Convert to float

    Parameters
    ----------
    string : str
        Input string to be converted

    Returns
    -------
    float
        Converted string
    """

    if(number_mode == "dec"):
        try:
            return(float(string))
        except ValueError:
            return(0.0)
        return(0.0)
    elif(number_mode == "hex"):
        try:
            if(len(string) == 8):
                return(struct.unpack('!f', string.decode("hex"))[0])
            elif(len(string) == 16):
                return(struct.unpack('!d', string.decode("hex"))[0])
        except TypeError:
            return(0.0)
    return(0)


# deprecated conversion for embedded systems that do not support long
# no longer used since hex conversion is now supported.
def to_long(big_string, small_string, number_mode):
    return(
        to_int(big_string, number_mode) * 10000 +
        to_int(small_string, number_mode))
