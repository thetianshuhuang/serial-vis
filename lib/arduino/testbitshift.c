#include <stdio.h>

// tohex
// supports up to 64 bit / 8 byte numbers
// outputs hex in ascii
// returns a string with number in hex format
char* tohex(void * input) {

	// Hex key with hex characters in order
	char* hex = "0123456789ABCDEF";
	// Bitmask for isolating last four bits
	int mask = 0xF;

	// Assign type of void* (cast to int)
	long long *number;
	number = (long long*) input;
	int size = sizeof(*number) * 2;
	
	// Output string
	char outstr[16];

	for(int i = 1; i <= size; i++) {
		char outchar = hex[(*number & mask)];
		outstr[size-i] = outchar;
		*number = *number >> 4;
	}

	return(outstr);
}
