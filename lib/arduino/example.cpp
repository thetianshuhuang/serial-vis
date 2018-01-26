#include <Arduino.h>

#include "serial-vis.h"
#include <stdlib.h>

int counter;
char outstr;
serialVis sv;

int main() {

  init();
  Serial.begin(115200);
  counter = 0;

  pinMode(LED_BUILTIN, OUTPUT);

  while(true){
    counter += 100;

    char buffer[10];
    itoa(counter, buffer, 10);
    sv.logs("counter", buffer);

    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
  }
}
