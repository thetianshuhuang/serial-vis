#ifndef SERIAL_VIS_H
#define SERIAL_VIS_H

// Generic print command for easy 
void printCommand(const char* input);

// Raw hex converter
char* toHex(void * input, char* outstr);

// Command handlerportability
void commandHandler(int num_args, ...);

#endif
