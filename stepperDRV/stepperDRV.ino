void setup()
{
  pinMode(4, OUTPUT); 
  pinMode(3, OUTPUT);// sets the digital pin 13 as output
  digitalWrite(3, HIGH);   
}

void loop()
{
  digitalWrite(4, HIGH);       // sets the digital pin 13 on
  delay(5);                  // waits for a second
  digitalWrite(4, LOW);        // sets the digital pin 13 off
  delay(5);                  // waits for a second
}
