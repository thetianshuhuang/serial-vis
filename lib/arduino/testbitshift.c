#include <stdio.h>
#include <stdarg.h>

// print command
void printcommand(char* input) {
	printf("%s", input);
}

// tohex
// supports up to 64 bit / 8 byte numbers
// outputs hex in ascii
// returns a string with number in hex format written to outstr
char* toHex(void * input, char* outstr) {

	// Hex key with hex characters in order
	char* hex = "0123456789ABCDEF";
	// Bitmask for isolating last four bits
	int mask = 0xF;

	// Assign type of void* (cast to int)
	long long *number;
	number = (long long*) input;
	int size = sizeof(*number) * 2;
	
	for(int i = 1; i <= size; i++) {
		char outchar = hex[(*number & mask)];
		outstr[size-i] = outchar;
		*number = *number >> 4;
	}

	// null termination
	outstr[size] = '\0';
}

// commandHandler
// handler for printing out commands
// format: commandHandler("opcode", command_format, args)
// where command_format is something like "s[dd]f".
void commandHandler(int num_args, ...) {

	// set up variable arguments
	va_list arguments;
	va_start(arguments, num_args);

	// print out opcode
	printcommand(va_arg(arguments, char*));

	// set up formatting
	char* format = va_arg(arguments, char*);
	int format_index = 0;
	char* current_separator = ":";
	char buffer[17];

	int i = 1;

	while(i < (num_args - 1)) {

		if(format[format_index - 1] != '[' && format[format_index] != ']') {
			printcommand(current_separator);
		}

		// check for formatting changes
		if(format[format_index] == '[') {
			current_separator = ",";
		}
		else if(format[format_index] == ']') {
			current_separator = ":";
		}

		// print commands
		else if(format[format_index] == 's') {
			printcommand(va_arg(arguments, char*));
			i += 1;
		}
		else if(format[format_index] == 'd') {
			long long rawint = va_arg(arguments, long long);
			toHex(&rawint, buffer);
			printcommand(buffer);
			i += 1;
		}
		else if(format[format_index] == 'f') {
			double rawfloat = va_arg(arguments, double);
			toHex(&rawfloat, buffer);
			printcommand(buffer);
			i += 1;
		}
		format_index += 1;
	}

	va_end(arguments);
	printcommand("\n");
}