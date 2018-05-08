#include "Motor.h"
#include "Car.h"
#include "I2CEncoder.h"
#include "Wire.h"
#include "NewPing.h"
#include "PhotoSensor.h"

const int startButton = 10;
const int trigPin = 12;
const int echoPin = 13;
const int leftPSensor = 2;
const int centerPSensor = 1;
const int rightPSensor = 0;

const int ledPin = 7;

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
  // put your setup code here, to run once:
  Wire.begin();
  leftEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  leftEncoder.unTerminate();
  rightEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  leftEncoder.zero();
  leftEncoder.setReversed(true);
  rightEncoder.zero();
  Serial.begin(9600);

  pinMode(ledPin,OUTPUT);
  
  car.wait(startButton);
  lightSensor.calibrateSensors(LIGHT,DARK,LIGHT);
  startMillis = millis();
  start_moving();
}

bool is_moving = false;
bool is_turning = false;
int lastHit = 0;
// -1 = left, 1 = right

unsigned long turning_timer = 0;

void start_moving(){
  is_moving = true;
  is_turning = false;
  car.forwardInchesStart(1000, 30);
}

void start_turning(){
  is_moving = false;
  is_turning = true;
}


void loop() 
{
  currentMillis = millis();

//  if we are moving
  while (car.detectObstacle(12))
  {
    car.stop();
  } //Stop the car if an obstacle is detected
  
  if (is_moving){
    //check drift
     if((currentMillis - startMillis) > DELAY_TIME){
      car.correctDrift();
      startMillis = currentMillis;
    }
    if(!(lightSensor.getCenterStatus() || lightSensor.getRightStatus() || lightSensor.getLeftStatus())){
      digitalWrite(ledPin,HIGH);
    }else{
      digitalWrite(ledPin,LOW);
    }
    if(lightSensor.getCenterStatus() && lightSensor.getRightStatus()){
      while (!lightSensor.getCenterStatus())
      {
        car.turnLeft();
      }
      car.stop();
      start_moving();
    }
    if(lightSensor.getCenterStatus() && lightSensor.getLeftStatus()){
      while (!lightSensor.getCenterStatus())
      {
        car.turnRight();
      }
      car.stop();
      start_moving();
    }
    //check light sensors
    if(lightSensor.getLeftStatus()){
      start_turning();
      while(!lightSensor.getCenterStatus() || lightSensor.getLeftStatus()){
        car.turnRight();
      }
      lastHit = -1;
    }
    if(lightSensor.getRightStatus()){
      while(!lightSensor.getCenterStatus() || lightSensor.getRightStatus()){
        car.turnLeft();
      }
      lastHit = 1;
    }
  }

  if(is_turning){
    int num_dark = lightSensor.getLeftStatus() + lightSensor.getRightStatus();
    if(num_dark == 0 && lightSensor.getCenterStatus()){
      start_moving();
    }
  }
}




 
 
