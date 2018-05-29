#include "Motor.h"
#include "Car.h"
#include "I2CEncoder.h"
#include "Wire.h"
#include "NewPing.h"

const int startButton = 10;
const int trigPin = 12;
const int echoPin = 13;
const int ledPin = 7;

//initialize car components
Motor leftMotor(2,3);
Motor rightMotor(4,5);
NewPing sonar(trigPin, echoPin);
I2CEncoder leftEncoder;
I2CEncoder rightEncoder;
//initialize car
Car car(&leftMotor,&rightMotor, &leftEncoder, &rightEncoder, &sonar);

bool start_motion = true;

unsigned long startMillis;
unsigned long currentMillis;
const unsigned long DELAY_TIME = 10; 

void setup() 
{
  pinMode(ledPin, OUTPUT);
  // put your setup code here, to run once:
  Wire.begin();
  leftEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  leftEncoder.unTerminate();
  rightEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  leftEncoder.zero();
  leftEncoder.setReversed(true);
  rightEncoder.zero();
  Serial.begin(9600);
  
  car.wait(startButton);
}

//Define target
const int image_width = 640;
const int targetX = image_width / 2;
const int targetY = 140;
const int targetR = 20;

long x;
long y;
long r;

//Define Proportional Constants
const float Kturning = 0.3;
const float Kmoving = 0.5;
const float KmovingR = 5;

//Drive left and right motors
//if power is too low, don't move
void drive(int leftPower, int rightPower)
{
  if(abs(leftPower) > 10){
    if(leftPower >= 0){
      leftMotor.forward(leftPower);
    } else {
      leftMotor.backward(abs(leftPower));
    }
  } else {
    leftMotor.forward(0);
  }

  if(abs(rightPower) > 10){
    if(rightPower >= 0){
      rightMotor.forward(rightPower);
    } else {
      rightMotor.backward(abs(rightPower));
    }
  } else {
    rightMotor.forward(0);
  }
}

void readSerial()
{
  while(Serial.available() > 0){
    while(Serial.read() != 'X'){} //Skip chars until 'X'
    x = Serial.parseInt();
    while(Serial.read() != 'R'){} //Skip chars until 'Y'
    r = Serial.parseInt();
    while(Serial.read() != '\n'){}
    return;
  }
}

//store last turn and move powers, for smoothing
int lastMovePower=0;
int lastTurnPower=0;

void loop() 
{
  // find out where the ball is
  readSerial();
  if(x == -1){
    drive(0,0);
  }
  else{
    // based on ball size, determine overall power
    int movePower = floor(-1 * KmovingR * (r - targetR));
    movePower = ceil((lastMovePower + movePower + movePower)/3);

    //debug led
    if(r < targetR){
      digitalWrite(ledPin,HIGH);
    } else{
      digitalWrite(ledPin,LOW);
    }
    
    // based on ball X location, determine turning power
    int turnPower = floor(Kturning * (x - targetX));
    turnPower = ceil((lastTurnPower + turnPower + turnPower)/3);

    // move based on powers.
    drive(movePower + turnPower, movePower - turnPower);
    lastTurnPower = turnPower;
    lastMovePower = movePower;
  }
}




