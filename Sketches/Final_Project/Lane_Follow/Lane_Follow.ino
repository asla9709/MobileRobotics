#include "Motor.h"
#include "Car.h"
#include "I2CEncoder.h"
#include "Wire.h"
#include "NewPing.h"
#include "PhotoSensor.h"

const int startButton = 10;
const int trigPin = 12;
const int echoPin = 13;
const int ledPin = 7;
const int leftPSensor = 2;
const int centerPSensor = 1;
const int rightPSensor = 0;

//initialize car components
Motor leftMotor(2,3);
Motor rightMotor(4,5);
NewPing sonar(trigPin, echoPin);
I2CEncoder leftEncoder;
I2CEncoder rightEncoder;
PhotoSensor lightSensor(leftPSensor, centerPSensor, rightPSensor);
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

  lightSensor.calibrateSensors(LIGHT,LIGHT,LIGHT);
  //car.wait(startButton);
}

//Define target



//Define Proportional Constants
const float turn_K = 0.6;
const float mov_K = 1;

const float targetX = 100;
const float targetV = 100;

long x = targetX;
long v = targetV;


void drive(int leftPower, int rightPower)
{
  if(leftPower >= 0)
  {
    leftMotor.forward(leftPower);
  } 
  else 
  {
    leftMotor.backward(abs(leftPower));
  }
  
  if(rightPower >= 0)
  {
    rightMotor.forward(rightPower);
  } 
  else 
  {
    rightMotor.backward(abs(rightPower));
  }
}

void readSerial()
{
  while(Serial.available() > 0){
    while(Serial.read() != 'X'){} //Skip chars until 'X'
    x = Serial.parseInt();
    while(Serial.read() != 'V'){} //Skip chars until 'V'
    v = Serial.parseInt();
    while(Serial.read() != '\n'){}
    return;
  }
}

void writeSerial()
{
  int ultrasonic_threshold = 20; //cm
  int distance = sonar.ping_cm();
  bool obstacle = distance <= ultrasonic_threshold;
  bool leftStatus = lightSensor.getLeftStatus();
  bool centerStatus = lightSensor.getCenterStatus();
  bool rightStatus = lightSensor.getRightStatus();
  int rps = leftEncoder.getSpeed();

  String outputString = "";
  outputString += (obstacle) ? "1" : "0";
  outputString += "::";
  outputString += distance;
  outputString += "::";
  outputString += (leftStatus) ? "1" : "0";
  outputString += "::";
  outputString += (centerStatus) ? "1" : "0";
  outputString += "::";
  outputString += (rightStatus) ? "1" : "0";
  outputString += "::";
  outputString += rps;
  outputString += "\n";

  Serial.println(outputString); 
  
}

//store last turn and move powers, for smoothing
int lastMovePower=0;
int lastTurnPower=0;

void loop() 
{
  // find out where the ball is
  readSerial();
  //writeSerial();
  if(x == -1){
    drive(0,0);
  }
  else{
    // based on ball size, determine overall power
    int movePower = round(mov_K * (v - targetV));
    movePower = round((lastMovePower + movePower + movePower)/3);

    //debug led
    if(x == 0){
      digitalWrite(ledPin,HIGH);
    } else{
      digitalWrite(ledPin,LOW);
    }
    
    // based on ball X location, determine turning power
    int turnPower = round(turn_K * (x- targetX));
    turnPower = round((lastTurnPower + turnPower + turnPower)/3);

    // move based on powers.
    drive(movePower + turnPower, movePower - turnPower);
    lastTurnPower = turnPower;
    lastMovePower = movePower;
  }
}




