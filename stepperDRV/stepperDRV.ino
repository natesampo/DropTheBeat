int wait = 10; 
#include <AccelStepper.h>
//AccelStepper Xaxis(1, 11, 10); // pin 3 = step, pin 6 = direction
void setup()
{
//  
  pinMode(11, OUTPUT);

  //Xaxis.setMaxSpeed(50);
  //Xaxis.setSpeed(20);
  
   
}

void loop()
{
  //Xaxis.runSpeed();
  digitalWrite(11,HIGH);
  delay(100);
  digitalWrite(11,LOW);
  delay(100);
//  
}
