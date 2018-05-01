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
  
  car.wait(startButton);
  lightSensor.calibrateSensors(LIGHT,DARK,LIGHT);
  startMillis = millis();
  start_moving();
}

bool is_moving = false;
bool is_turning = false;

unsigned long turning_timer = 0;

void start_moving(){
  is_moving = true;
  is_turning = false;
  car.forwardInchesStart(1000, 50);
}

void start_turning(){
  is_moving = false;
  is_turning = true;
}


void loop() 
{
  currentMillis = millis();

  //if we are moving
  if (is_moving){
    //check drift
     if((currentMillis - startMillis) > DELAY_TIME){
      car.correctDrift();
      startMillis = currentMillis;
    }
    if(lightSensor.getCenterStatus() && lightSensor.getRightStatus()){
      car.forwardInches(4,50);
      car.turnRight90();
      start_moving();
    }
    if(lightSensor.getCenterStatus() && lightSensor.getLeftStatus()){
      car.forwardInches(4,50);
      car.turnLeft90();
      start_moving();
    }
    //check light sensors
    if(lightSensor.getLeftStatus()){
      start_turning();
      car.turnRight();
    }
    if(lightSensor.getRightStatus()){
      start_turning();
      car.turnLeft();
    }
    while(car.detectObstacle(12)){} //Stop the car if an obstacle is detected
  }

  if(is_turning){
    int num_dark = lightSensor.getLeftStatus() + lightSensor.getRightStatus();
    if (num_dark > 0){
      
    }
    if (num_dark == 0){
      start_moving();
    }
    //else if(num_dark == 2){
    //  car.stop();
    //  car.turnRight90();
    //  car.turnRight90();
    //  start_moving();
    //}
  }
}




 
 
