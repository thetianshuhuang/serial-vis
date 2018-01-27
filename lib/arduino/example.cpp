#include <Arduino.h>

#include "serial-vis.h"
#include <stdlib.h>

float counter;
char outstr;
serialVis sv;

int main() {

  init();
  Serial.begin(115200);
  counter = 0;

  pinMode(LED_BUILTIN, OUTPUT);

  while(true){
    counter += 1;

    sv.drawcircle(400, 300, counter, "black");
    sv.draw();

    if(counter >= 200) {
      counter = 0;
    }

    delay(10);
  }
}
