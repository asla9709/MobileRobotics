#include <Wire.h>
#include <Car.h>
#include <Motor.h>
#include <I2CEncoder.h>

const int startButton = 10;

Motor leftMotor(2,3);
Motor rightMotor(4,5);
Car myCar(&leftMotor,&rightMotor);

I2CEncoder leftEncoder;
I2CEncoder rightEncoder;

void setup() {
  // put your setup code here, to run once: 
  Wire.begin();
  leftEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  leftEncoder.unTerminate();
  rightEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  

  Serial.begin(9600);
  myCar.wait(startButton);
}

void loop() {
  leftMotor.forward(50);
  rightMotor.forward(50);
  
  int spdL = leftEncoder.getSpeed();
  int posL = leftEncoder.getRawPosition();

  int spdR = rightEncoder.getSpeed();
  int posR = rightEncoder.getRawPosition();

  Serial.print("Left Motor Speed:\t");
  Serial.println(spdL);
  Serial.print("Left Motor Position:\t");
  Serial.println(posL);
  Serial.println("");

  Serial.print("Right Motor Speed:\t");
  Serial.println(spdR);
  Serial.print("Right Motor Position:\t");
  Serial.println(posL);
  Serial.println("");
}
