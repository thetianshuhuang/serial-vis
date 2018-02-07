// Generic Serial Command subroutines

// TODO: add retry to commandHandler

#include "Arduino.h"
#include <stdarg.h>
#include "serial-command.h"

// initializer
commandHandler::commandHandler()
{
    timeout_us = 1000;
}

// print command
void commandHandler::printCommand(const char* input)
{
    Serial.print(input);

    if(timeout_us > 0)
    {  
        // Update checksum
        int i = 0;
        while(input[i] != '\0')
        {
            checksum += (uint8_t) input[i];
            i += 1;
        }  
    }
}

// print out checksum
void commandHandler::printCheckSum()
{
    char checksumout[3];
    toHex(&checksum, 1, checksumout);
    printCommand(checksumout);
}

// get reply
// 0xFF: success
// 0x00: failure
// other codes tbd
uint8_t commandHandler::getReply()
{
    long timeout = millis() + timeout_us;
    while(timeout > millis())
    {
        if(Serial.available())
        {
            if(Serial.read() == 0x00)
            {
                return(0x00);
            }
            else if(Serial.read() == 0xFF)
            {
                return(0xFF);
            }
            else
            {
                return(0x00);
            }
        }
    }
    return(0x0F);

}

// tohex
// supports up to 64 bit / 8 byte numbers
// outputs hex in ascii
// returns a string with number in hex format written to outstr
// outsize is the output number size in bytes
void commandHandler::toHex(void * input, int outsize, char* outstr) {

    // Hex key with hex characters in order
    char hex[] = "0123456789ABCDEF";
    // Bitmask for isolating last four bits
    uint8_t mask = 0xF;

    // Assign type of void* (cast to int)
    long long *number;
    number = (long long*) input;
    int size = outsize * 2;
  
    for(int i = 1; i <= size; i++)
    {
        char outchar = hex[(*number & mask)];
        outstr[size-i] = outchar;
        *number = *number >> 4;
    }

    // null termination
    outstr[size] = '\0';  
}

// command
// handler for printing out commands
// format: commandHandler("opcode", command_format, args)
// where command_format is something like "s[dd]f".
uint8_t commandHandler::command(int num_args, ...)
{
    // reset checksum
    checksum = 0;

    // set up variable arguments
    va_list arguments;
    va_start(arguments, num_args);

    // print out opcode
    printCommand(va_arg(arguments, char*));

    // set up formatting
    char* format = va_arg(arguments, char*);
    int format_index = 0;
    char* current_separator = ":";
    
    int i = 1;

    // main loop
    while(i < (num_args - 1))
    {
        // print separator between arguments
        if(format[format_index - 1] != '[' && format[format_index] != ']')
        {
            printCommand(current_separator);
        }

        // check for formatting changes
        if(format[format_index] == '[')
        {
            current_separator = ",";
        }
        else if(format[format_index] == ']')
        {
            current_separator = ":";
        }

        // print commands

        // string
        else if(format[format_index] == 's')
        {
            printCommand(va_arg(arguments, char*));
            i += 1;
        }
        // int
        else if(format[format_index] == 'd')
        {
            char buffer[5];
            long long rawint = va_arg(arguments, int);
            toHex(&rawint, 2, buffer);
            printCommand(buffer);
            i += 1;
        }
        // long
        else if(format[format_index] == 'l')
        {
            char buffer[9];
            long long rawint = va_arg(arguments, long);
            toHex(&rawint, 4, buffer);
            printCommand(buffer);
            i += 1;
        }
        // long long
        else if(format[format_index] == 'L')
        {
            char buffer[17];
            long long rawint = va_arg(arguments, long long);
            toHex(&rawint, 8, buffer);
            printCommand(buffer);
            i += 1;
        }
        // float
        else if(format[format_index] == 'f')
        {
            char buffer[9];
            double rawfloat = va_arg(arguments, double);
            toHex(&rawfloat, 4, buffer);
            printCommand(buffer);
            i += 1;
        }
        // double
        else if(format[format_index] == 'F')
        {
            char buffer[17];
            double rawfloat = va_arg(arguments, double);
            toHex(&rawfloat, 8, buffer);
            printCommand(buffer);
            i += 1;
        }

        // increment index
        format_index += 1;
    }

    // conclude function
    va_end(arguments);
    if(timeout_us > 0)
    {
        printCheckSum();
        printCommand("\n");
        return getReply();
    }
    else
    {
        printCommand("\n");
        return 0xFF;
    }
}
