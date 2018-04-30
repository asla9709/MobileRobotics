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
  lightSensor.calibrateSensors();
}

void loop() 
{
  Serial.print("L");
  Serial.print("\t");
  Serial.print("C");
  Serial.print("\t");
  Serial.print("R");
  Serial.println("");
  for (int i = 0; i < 1000; i++)
  {
    //Status uses Light=0 and Dark=1 keywords
    Serial.print(lightSensor.getLeftStatus() ? "Dark" : "Light");
    Serial.print("\t\t");
    Serial.print(lightSensor.getCenterStatus() ? "Dark" : "Light");
    Serial.print("\t\t");
    Serial.print(lightSensor.getRightStatus() ? "Dark" : "Light");
    Serial.println("");

    PSData sensorData = lightSensor.getThresholdData();
    Serial.print(sensorData.leftRes);
    Serial.print("\t\t");
    Serial.print(sensorData.centerRes);
    Serial.print("\t\t");
    Serial.print(sensorData.rightRes);
    Serial.println("");

    sensorData = lightSensor.getSensorData();
    Serial.print(sensorData.leftRes);
    Serial.print("\t\t");
    Serial.print(sensorData.centerRes);
    Serial.print("\t\t");
    Serial.print(sensorData.rightRes);
    Serial.println("");
    delay(100);
  }
  
}



