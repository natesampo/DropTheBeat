int wait = 10; 
#include <AccelStepper.h>
AccelStepper sheets(1, 11,10); // pin 3 = step, pin 6 = direction
AccelStepper wheel(1, 12,9); // pin 3 = step, pin 6 = direction

void setup()
{
  sheets.setMaxSpeed(400);
  sheets.setSpeed(320);
  wheel.setMaxSpeed(100);
  wheel.setSpeed(25);
   
}

void loop()
{
  wheel.runSpeed();

//  
}
