#include "Motor.h"
#include "Car.h"
#include "I2CEncoder.h"
#include "Wire.h"
#include "NewPing.h"
#include "PhotoSensor.h"
#include "TimerOne.h"


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
int forwardBit = 0;
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
  Timer1.initialize(10000L); //10 milliseconds (10 * 1000 microseconds)
  Timer1.attachInterrupt(Timer1_ISR);//attach our ISR to the timer interrupt
}

void loop() 
{
  //PSData sensorData = lightSensor.getS  ensorData();
  car.correctDrift(forwardBit);
}

void Timer1_ISR()
{
  //
}



