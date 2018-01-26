#include <Arduino.h>

#include "serial-vis.h"

double counter;
char outstr;
serialVis sv;

int main() {

  init();
  Serial.begin(115200);
  counter = 1;

  pinMode(LED_BUILTIN, OUTPUT);

  while(true){
    counter += 3.14159265;
  
    sv.logf("counter", counter);

    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
  }
}
