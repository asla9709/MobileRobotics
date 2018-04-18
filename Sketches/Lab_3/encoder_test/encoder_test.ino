#include <Wire.h>
#include <Car.h>
#include <Motor.h>
#include <I2CEncoder.h>

const int startButton = 12;

Motor leftMotor(2,3);
Motor rightMotor(4,5);
Car myCar(&leftMotor,&rightMotor);

I2CEncoder encoder;
I2CEncoder encoder2;
I2CEncoder encoder3;

void setup() {
  // put your setup code here, to run once: 
  Wire.begin();
  encoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  encoder.unTerminate();
  encoder2.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  

  Serial.begin(9600);
  myCar.wait(startButton);
}

void loop() {
  leftMotor.forward(50);
  delay(1500);
  int i = encoder.getSpeed();
  Serial.print("Speed = ");
  Serial.println(i);
  i = encoder2.getSpeed();
  Serial.print("Speed2 = ");
  Serial.println(i);
}
