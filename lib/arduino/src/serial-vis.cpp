// serial-vis specific API

#include "serial-vis.h"
#include "serial-command.h"

// Constructor
serialVis::serialVis(int timeout)
{
	timeout_us = timeout;
}

// Function definitions at
// github.com/thetianshuhuang/serial-vis

// control commands

// draw buffer
uint8_t serialVis::draw()
{
	return(command(2, "draw", ""));
}

// log commands
uint8_t serialVis::logs(char * label, char * datastring)
{
	return(command(4, "logs", "ss", label, datastring));
}
uint8_t serialVis::logf(char * label, double datadouble)
{
	return(command(4, "logf", "sF", label, datadouble));
}
uint8_t serialVis::logstart()
{
	return(command(2, "logstart", ""));
}	
uint8_t serialVis::logend()
{
	return(command(2, "logend", ""));
}

// echo
uint8_t serialVis::echo(char * text)
{
	return(command(3, "echo", "s", text));
}


// draw commands

// definecolor
uint8_t serialVis::definecolor(char * color, int r, int g, int b)
{
	return(command(6, "definecolor", "s[ddd]", color, r, g, b));
}

// setscale
uint8_t serialVis::setscale(float scale) {
	return(command(3, "setscale", "f", scale));
}

// setoffset
uint8_t serialVis::setoffset(int x, int y) {
	return(command(4, "setoffset", "[dd]", x, y));
}

// drawline
uint8_t serialVis::drawline(float x_1, float y_1, float x_2, float y_2, char* color) {
	return(command(7, "drawline", "[ff][ff]s", x_1, y_1, x_2, y_2, color));
}

// drawlinep
uint8_t serialVis::drawlinep(int x_1, int y_1, int x_2, int y_2, char* color) {
	return(command(7, "drawlinep", "[dd][dd]s", x_1, y_1, x_2, y_2, color));
}

// drawcircle
uint8_t serialVis::drawcircle(float x, float y, float r, char* color) {
	return(command(6, "drawcircle", "[ff]fs", x, y, r, color));
}

// drawray
uint8_t serialVis::drawray(float x, float y, float angle, float length, char* color) {
	return(command(7, "drawray", "[ff]ffs", x, y, angle, length, color));
}

// text
uint8_t serialVis::text(char* label, float x, float y, int size, char* color) {
	return(command(7, "text", "s[ff]ds", label, x, y, size, color));
}

// textp
uint8_t serialVis::textp(char* label, int x, int y, int size, char* color) {
	return(command(7, "textp", "s[dd]ds", label, x, y, size, color));
}
