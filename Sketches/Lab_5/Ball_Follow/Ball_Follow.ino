#include "Motor.h"
#include "Car.h"
#include "I2CEncoder.h"
#include "Wire.h"
#include "NewPing.h"

const int startButton = 10;
const int trigPin = 12;
const int echoPin = 13;

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

const int targetX = 128;
const int targetY = 210;
int x;
int y;

int power = 0;
int targetPower = 0;

void move(int leftPower, int rightPower){
  if(leftPower >= 0){
    leftMotor.forwards(leftPower);
  } else {
    leftMotor.backwards(abs(leftPower));
  }

  if(rightPower >= 0){
    rightMotor.forwards(leftPower);
  } else {
    rightMotor.backwards(abs(leftPower));
  }
}

void loop() 
{
  // find out where the ball is
  // based on ball Y location, determine overall power
  // based on ball X location, determine turning power
  
  // move based on powers.
}
 



