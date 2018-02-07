#ifndef SERIAL_VIS_H
#define SERIAL_VIS_H

#include "serial-command.h"

class serialVis: public commandHandler {
    public:
        // constructor
        serialVis(int timeout);

        // control commands
        // draw buffer
        uint8_t draw();
        // log commands
        uint8_t logs(char * label, char * datastring);
        uint8_t logf(char * label, double datadouble);
        uint8_t logstart();
        uint8_t logend();
        // echo
        uint8_t echo(char * text);
        
        // draw commands
        // definecolor
        uint8_t definecolor(char * color, int r, int g, int b);
        // setscale
        uint8_t setscale(float scale);
        // setoffset
        uint8_t setoffset(int x, int y);
        // drawline
        uint8_t drawline(float x_1, float y_1, float x_2, float y_2, char* color);
        // drawlinep
        uint8_t drawlinep(int x_1, int y_1, int x_2, int y_2, char* color);
        // drawcircle
        uint8_t drawcircle(float x, float y, float r, char* color);
        // drawray
        uint8_t drawray(float x, float y, float angle, float length, char* color);
        // text
        uint8_t text(char* label, float x, float y, int size, char* color);
        // textp
        uint8_t textp(char* label, int x, int y, int size, char* color);
};

#endif
