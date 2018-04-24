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
const unsigned long DELAY_TIME = 20; 

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
  startMillis = millis();
}



void loop() 
{
  currentMillis = millis();
  if (start_motion){
    car.forwardInchesStart(1000, 50);
    start_motion = false;
  }

  if((currentMillis - startMillis) > DELAY_TIME){
    car.correctDrift();
    startMillis = currentMillis;
  }

  
  if(car.detectObstacle()){
    if (rand() % 2 == 0) //randomly choose left or right
    {
      car.turnRight90();
    }
    else
    {
      car.turnLeft90();
    }
    start_motion = true;
  }
}
 



