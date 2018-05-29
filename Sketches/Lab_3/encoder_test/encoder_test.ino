#include <Motor.h>
#include <Car.h>
#include <I2CEncoder.h>
#include <Wire.h>

const int startButton = 10;

Motor leftMotor(2,3);
Motor rightMotor(4,5);
I2CEncoder leftEncoder;
I2CEncoder rightEncoder;
Car car(&leftMotor,&rightMotor, &leftEncoder, &rightEncoder);


int testPower[100];
double testSpeedLeft[100];
double testSpeedRight[100];

void setup() {
  // put your setup code here, to run once: 
  Wire.begin();
  leftEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  leftEncoder.unTerminate();
  leftEncoder.setReversed();
  rightEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);

  leftEncoder.zero();
  rightEncoder.zero();

  Serial.begin(9600);
  car.wait(startButton);
}

void loop() 
{
  car.forward(50);
  serial.print(leftEncoder.getRawPosition())
  serial.print("\t");
  serial.print(leftEncoder.getPosition())
  serial.print("\t");
  serial.println(leftEncoder.getSpeed())
}
