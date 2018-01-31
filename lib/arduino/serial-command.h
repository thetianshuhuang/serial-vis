/*
  Serial-command.h - Library for managing serial commands. Used by serial-vis.
*/

#ifndef SERIAL_COMMAND_H
#define SERIAL_COMMAND_H

#include "Arduino.h"
#include <stdarg.h>

class commandHandler
{
  public:
    void command(int num_args, ...);
  private:
  	long long checksum;
    void printCommand(const char * input);
    void toHex(void * input, int outsiz, char * outstr);
    void printCheckSum();
    uint8_t getReply();
};

#endif
