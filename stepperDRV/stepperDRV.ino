int wait = 10; 
#include <AccelStepper.h>
AccelStepper sheets(1, 11,10); // pin 3 = step, pin 6 = direction
//AccelStepper wheel(1, 12,9); // pin 3 = step, pin 6 = direction

void setup()
{
  sheets.setMaxSpeed(400);
  sheets.setSpeed(320);
//  analogWrite(9, 60);
  digitalWrite(6,HIGH);
   
}

void loop()
{
  if(digitalRead(5)){
    sheets.setSpeed(320);
    sheets.runSpeed();
  }else if(digitalRead(7)){
    long currentMillis = millis();
//

     if (currentMillis % 3000 < 0){
        analogWrite(9, 80);
     }else{
        analogWrite(9, 40);
     }
     sheets.setSpeed(0);
   }else{
      analogWrite(9, 0);
      sheets.setSpeed(0);
   }
//  
}
