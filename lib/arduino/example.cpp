#include <Arduino.h>
#include "serial-vis.h"

double counter;
char outstr;

int main() {

  init();
  Serial.begin(115200);
  counter = 1;

  while(true){
    counter += 3.14159265;
  
    logf(counter);
  
    delay(1000);
  }
}
