// serial-vis specific API

#include "serial-vis.h"
#include "serial-command.h"

// Function definitions at
// github.com/thetianshuhuang/serial-vis

// control commands

// draw buffer
void draw()
{
	command(2, "draw", "");
}

// log commands
void logs(char * label, char * datastring)
{
	command(4, "logs", "ss", label, datastring);
}
void logf(char * label, double datadouble)
{
	command(4, "logf", "sF", label, datadouble);
}
void logstart()
{
	command(2, "logstart", "");
}	
void logend()
{
	command(2, "logend", "");
}

// echo
void echo(char * text)
{
	command(3, "echo", "s", text);
}


// draw commands

// definecolor
void definecolor(char * color, int r, int g, int b)
{
	command(6, "definecolor", "s[ddd]", color, r, g, b);
}

// setscale
void setscale(float scale) {
	command(3, "setscale", "f", scale);
}

// setoffset
void setoffset(int x, int y) {
	command(4, "setoffset", "[dd]", x, y);
}

// drawline
void drawline(float x_1, float y_1, float x_2, float y_2, char* color) {
	command(7, "drawline", "[ff][ff]s", x_1, y_1, x_2, y_2, color);
}

// drawlinep
void drawlinep(int x_1, int y_1, int x_2, int y_2, char* color) {
	command(7, "drawlinep", "[dd][dd]s", x_1, y_1, x_2, y_2, color);
}

// drawcircle
void drawcircle(float x, float y, float r, char* color) {
	command(6, "drawcircle", "[ff]fs", x, y, r, color);
}

// drawray
void drawray(float x, float y, float angle, float length, char* color) {
	command(7, "drawray", "[ff]ffs", x, y, angle, length, color);
}

// text
void text(char* label, float x, float y, int size, char* color) {
	command(7, "text", "s[ff]ds", label, x, y, size, color);
}

// textp
void textp(char* label, int x, int y, int size, char* color) {
	command(7, "textp", "s[dd]ds", label, x, y, size, color);
}
