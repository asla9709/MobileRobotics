#include <NewPing.h>

//Simple test for front mounted ultrasonic sensor (SR-04)


// defines pins numbers
const int trigPin = 12;
const int echoPin = 13;
//NewPing sonar(trigger_pin, echo_pin [, max_cm_distance]);
NewPing sonar(trigPin, echoPin);

void setup() 
{
    // put your setup code here, to run once:
    
    
    
    Serial.begin(9600); // serial output to show test data
  
  
}

void loop() 
{
    // put your main code here, to run repeatedly:
    int distance = sonar.ping_cm();
    Serial.print("Ping Distance: ");
    Serial.print(distance);
    Serial.print(" cm\r\n");
    delay(10);
}
