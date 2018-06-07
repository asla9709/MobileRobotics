#include "Motor.h"
#include "Wire.h"

const int startButton = 10;
const int trigPin = 12;
const int echoPin = 13;
const int ledPin = 7;

//initialize car components
Motor leftMotor(2,3);
Motor rightMOtor(4,5);

//initialize car
bool start_motion = true;

unsigned long startMillis;
unsigned long currentMillis;
const unsigned long DELAY_TIME = 10;

void setup(){
  pinMode(ledPin, OUTPUT);
  //put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(startButton, INPUT);
  while(digitalRead(startButton)==LOW){
    delay(3);
  }
}

const int targetX = 128;
const int targetY = 170;
long x;
long y;

const float Kturning = 0.8;
const float Kmoving = 1.5;

void move(int leftPower, int rightPower){
  if(leftPower >= 0){
    leftMotor.forward(leftPower);
  } else {
    leftMotor.backward(abs(leftPower));
  }

  if(right  if(rightPower >= 0){
    rightMotor.forward(leftPower);
  } else {
    rightMotor.backward(abs(leftPower));
  }
}

void readSerial()
{
  while(Serial.available() > 0){
    //while(Serial.read() != 'X'){} //Skip chars until 'X'
    x = Serial.parseInt();
    //while(Serial.read() != 'Y'){} //Skip chars until 'Y'
    y = Serial.parseInt();
    while(Serial.read() != '\n'){}
    return;
  }
}

void loop() 
{
  // find out where the traffic light circle is
  readSerial();
  if(RED == true && GREEN == false){
    move(0,0);
  }
  else {
    // based on ball Y location, determine overall power
    int movePower = floor(-1 * Kmoving * (y - targetY));
    // based on ball X location, determine turning power
    int turnPower = floor(Kturning * (x - targetX));
    // move based on powers.
    move(movePower + turnPower, movePower - turnPower);
  }
}
