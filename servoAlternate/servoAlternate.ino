/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo servos[2];
// create servo object to control a servo
// twelve servo objects can be created on most boards

int pos[2] = {0,0};  // variable to store the servo position
int rangealt[2][2] ={{05,120},{05,120}};
int range[2][2] ={{72,120},{72,120}};
int diralt[2] ={5,-5};
int dir[2] ={1,-1};
int delayt = 300;

void setup() {
  
  Serial.begin(9600);
  Serial.println("BEGIN");
  servos[0].attach(9);  // attaches the servo on pin 9 to the servo object
  servos[1].attach(10);
  delay(10000);
}

void loop() {
  humanMusic();
  delay(500);
//  runservo(1,1);
  
}

void runservoalt(int servo, int dirIndex){
   for (int p = rangealt[servo][dirIndex]; p <= rangealt[servo][1] && p >= rangealt[servo][0]; p += diralt[dirIndex]) {
    // in steps of 1 degree
    Serial.println(p);
    servos[servo].write(p);              // tell servo to go to position in variable 'pos'
    delay(5);                       // waits 15ms for the servo to reach the position
  }
}

void runservo(int servo,int dirIndex){
  for (int p = range[servo][dirIndex]; p <= range[servo][1] && p >= range[servo][0]; p += dir[dirIndex]) {
    // in steps of 1 degree
    Serial.println(p);
    servos[servo].write(p);              // tell servo to go to position in variable 'pos'
    delay(1);                       // waits 15ms for the servo to reach the position
  }
  dirIndex = (dirIndex +1)%2;
  for (int p = range[servo][dirIndex]; p <= range[servo][1] && p >= range[servo][0]; p += dir[dirIndex]) {
    // in steps of 1 degree
    Serial.println(p);
    servos[servo].write(p);              // tell servo to go to position in variable 'pos'
    delay(1);                       // waits 15ms for the servo to reach the position
  }
}

void humanMusic(){

  runservo(0,1);
  delay(delayt);
  runservoalt(0,1);
  delay(delayt);
  runservoalt(0,0);
  delay(delayt);
}

