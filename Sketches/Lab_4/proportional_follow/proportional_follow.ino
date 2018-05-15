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

void backwards(int speed)
{
  leftMotor.backward(speed);
  rightMotor.backward(speed);
}
void forwards(int speed)
{
  leftMotor.forward(speed);
  rightMotor.forward(speed);
}

const int targetDistance = 25; //cm
int distance = 0;
const float K = 1.8;

int power = 0;
int targetPower = 0;  

void loop() 
{
  //read distance
  distance = sonar.ping_cm();
  if(distance > 80 || distance < 5){
    forwards(0);
  }
  else{
    int error = targetDistance - distance;
    if(abs(error) < 5){
      forwards(0);
    }
    else if(error < 0){
      targetPower = -1 * K * error;
      forwards(floor(targetPower));
    }
    else if(error > 0){
      targetPower = K * error;
      backwards(floor(targetPower));
    }
  }
  delay(10);
}
 



