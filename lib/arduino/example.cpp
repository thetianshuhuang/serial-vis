#include <Arduino.h>

#include "src/serial-vis.h"
#include <stdlib.h>

float counter;
serialVis sv(0);

int main() {

  init();
  Serial.begin(115200);
  counter = 0;

  sv.setoffset(400,300);
  sv.setscale(2);
  sv.definecolor("red", 255, 0, 0);

  while(true){
    
    sv.drawcircle(0, 0, counter, "red");
    sv.draw();
    counter += 1;
    
    if(counter >= 200) {
      counter = 0;
    }
    delay(10);
  }
}
