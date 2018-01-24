// serial-vis specific API

#include "serial-command.h"
#include "serial-vis.h"

// Function definitions at
// github.com/thetianshuhuang/serial-vis

// control commands

// draw buffer
void draw() {
	commandHandler(2, "draw", "");
}

// log commands
void log(char * label, char * datastring) {
	commandHandler(3, "log", "s", datastring);
}
void logf(char * label, double datadouble) {
	commandHandler(3, "log", "F", datadouble);
}
void logstart() {
	commandHandler(2, "logstart", "");
}	
void logend() {
	commandHandler(2, "logend", "");
}

// echo
void echo(char * text) {
	commandHandler(3, "echo", "s", text);
}


// draw commands

// definecolor
void definecolor(char * color, int r, int g, int b) {
	commandHandler(6, "definecolor", "s[ddd]", color, r, g, b);
}

// setscale
void setscale(float scale) {
	commandHandler(3, "setscale", "f", scale);
}

// setoffset
void setoffset(int x, int y) {
	commandHandler(4, "setoffset", "[dd]", x, y);
}

// drawline
void drawline(float x_1, float y_1, float x_2, float y_2, char* color) {
	commandHandler(7, "drawline", "[ff][ff]s", x_1, y_1, x_2, y_2, color);
}

// drawlinep
void drawlinep(int x_1, int y_1, int x_2, int y_2, char* color) {
	commandHandler(7, "drawlinep", "[dd][dd]s", x_1, y_1, x_2, y_2, color);
}

// drawcircle
void drawcircle(float x, float y, float r, char* color) {
	commandHandler(6, "drawcircle", "[ff]fs", x, y, r, color);
}

// drawray
void dawray(float x, float y, float angle, float length, char* color) {
	commandHandler(7, "drawray", "[ff]ffs", x, y, angle, length, color);
}

// text
void text(char* label, float x, float y, int size, char* color) {
	commandHandler(7, "text", "s[ff]ds", label, x, y, size, color);
}

// textp
void textp(char* label, int x, int y, int size, char* color) {
	commandHandler(7, "textp", "s[dd]ds", label, x, y, size, color);
}
