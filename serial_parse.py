# serial command parsing subroutines


#   --------------------------------
#
#   parse command into opcode and arguments
#
#   --------------------------------
def parse_line(code_line):
    
    # intialize args as an empty array
    arguments = []
    
    # if a colon is not found, then the opcode has no args       
    opcode_end = code_line.find(":")
    if(opcode_end == -1):
        arguments.append(code_line)

    # else, strip out the opcode
    else:
        arguments.append(code_line[0:opcode_end])
        previous_arg_end = opcode_end
        current_arg_end = code_line.find(":",opcode_end + 1)
        
        # then separate the arguments
        while(current_arg_end != -1):
            arguments.append(code_line[previous_arg_end+1:
                                       current_arg_end])
            previous_arg_end = current_arg_end
            current_arg_end = code_line.find(":",current_arg_end + 1)
            
        arguments.append(code_line[previous_arg_end+1:len(code_line)])

    return(arguments)


#   --------------------------------
#
#   process arguments into an array
#
#   --------------------------------
def process_args(raw_arguments,commands):

    arguments = []
    opcode = raw_arguments[0]
    arguments.append(raw_arguments[0])

    n = 1
    while(n<len(raw_arguments)):

        try:
            argument_type = commands[opcode][n-1]
        except:
            print("Error: unrecognized opcode")
            print(opcode)
            argument_type = "ERR"

        # single argument types:
        # integer type
        if(argument_type == "d"):
            try:
                arguments.append(int(raw_arguments[n]))
            except:
                arguments.append(0)
        # string type
        elif(argument_type == "s"):
            arguments.append(raw_arguments[n])
        # float type
        elif(argument_type == "f"):
            try:
                arguments.append(float(raw_arguments[n]))
            except:
                arguments.append(0)
        # long type
        elif(argument_type == "l"):
            try:
                arguments.append(int(raw_arguments[n])*1000 +
                                 int(raw_arguments[n+1]))
            except:
                arguments.append(0)

        # array argument types:
        elif(len(argument_type) == 2):
            # separate array elements first
            argument_array_raw = []
            previous_arg_end = 0
            while(current_arg_end != -1):
                current_arg_end = raw_arguments[n].find(",",previous_arg_end)
                if(current_arg_end != -1):
                    argument_array_raw.append(raw_arguments[n][previous_arg_end:current_arg_end]) 
                    previous_arg_end = current_arg_end + 1
                else:
                    argument_array_raw.append(raw_arguments[n][previous_arg_end:])

            # parse each element in the array
            argument_array = []
            for element in argument_array_raw:
                if(argument_type) == "dd":
                    try:
                        argument_array.append(int(element))
                    except:
                        argument_array.append(0)
                elif(argument_type) == "ss":
                    argument_array.append(element)
                elif(argument_type) == "ff":
                    try:
                        argument_array.append(float(element))
                    except:
                        argument_array.append(0)
                elif(argument_type) == "ll":
                    try:
                        argument_array.append(int(raw_arguments[n])*1000 +
                                              int(raw_arguments[n+1]))
                    except:
                        argument_array.append(0)

            # finally, append the array to the arguments
            arguments.append(argument_array)

        # empty type, for when one arg takes up two spaces
        elif(argument_type == "_"):
            arguments.append(0)
        # error type, when the type doesn't match
        else:
            arguments.append("ERR")
            
        n += 1
            
    return(arguments)