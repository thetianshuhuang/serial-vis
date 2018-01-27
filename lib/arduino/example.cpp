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
    counter += 5;

    sv.drawcircle(300,400,counter,"black");
    sv.draw();

    if(counter >= 200) {
      counter = 0;
    }
    
    digitalWrite(LED_BUILTIN, HIGH);
    delay(250);
    digitalWrite(LED_BUILTIN, LOW);
    delay(250);
  }
}
