#ifndef SERIAL_VIS_H
#define SERIAL_VIS_H

#include "serial-command.h"

class serialVis: public commandHandler {
  public:
    // control commands
    // draw buffer
    void draw();
    // log commands
    void logs(char * label, char * datastring);
    void logf(char * label, double datadouble);
    void logstart();
    void logend();
    // echo
    void echo(char * text);
    
    // draw commands
    // definecolor
    void definecolor(char * color, int r, int g, int b);
    // setscale
    void setscale(float scale);
    // setoffset
    void setoffset(int x, int y);
    // drawline
    void drawline(float x_1, float y_1, float x_2, float y_2, char* color);
    // drawlinep
    void drawlinep(int x_1, int y_1, int x_2, int y_2, char* color);
    // drawcircle
    void drawcircle(float x, float y, float r, char* color);
    // drawray
    void drawray(float x, float y, float angle, float length, char* color);
    // text
    void text(char* label, float x, float y, int size, char* color);
    // textp
    void textp(char* label, int x, int y, int size, char* color);
};

#endif
