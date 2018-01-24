#include "serial-vis.h"

double counter;
char outstr;



void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);

  counter = 1;

}

void loop() {
  // put your main code here, to run repeatedly:

  counter += 3.14159265;

  logf(counter);

  delay(1000);

}


