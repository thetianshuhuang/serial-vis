/*
  Serial-command.h - Library for managing serial commands. Used by serial-vis.
*/

#ifndef SERIAL_COMMAND_H
#define SERIAL_COMMAND_H

#include <stdarg.h>
#include <stdio.h>

void command(int num_args, ...);
void printCommand(const char * input);
char* toHex(void * input, int outsiz, char * outstr);

#endif