#include <Motor.h>
#include <Car.h>
#include <I2CEncoder.h>
#include <Wire.h>

const int startButton = 10;

Motor leftMotor(2,3);
Motor rightMotor(4,5);
I2CEncoder leftEncoder;
I2CEncoder rightEncoder;
Car myCar(&leftMotor,&rightMotor, &leftEncoder, &rightEncoder);


int testPower[100];
double testSpeedLeft[100];
double testSpeedRight[100];

void setup() {
  // put your setup code here, to run once: 
  Wire.begin();
  leftEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);
  leftEncoder.unTerminate();
  rightEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA);

  Serial.begin(9600);
  myCar.wait(startButton);
}

void loop() 
{
  int index = 0;
  for (int counter = 1; counter <= 10; counter++)
  {
    Serial.print("Test no. \t\t");
    Serial.println(index);
    //get speed data points withthe battery at different levels
    for (int spd = 10; spd <= 100; spd += 10)
    {
      Serial.print("Test no. \t\t");
      Serial.println(index);
      leftMotor.forward(spd);
      rightMotor.forward(spd);
      delay(2000); //delay 2 seconds before recording data;
      double leftSum = 0;
      double rightSum = 0;
      
      for (int i = 0; i < 10; i++)
      {
        leftSum += leftEncoder.getSpeed();
        rightSum += rightEncoder.getSpeed();
      }
      myCar.stop();
      double leftAvg = leftSum / 10;
      double rightAvg = rightSum / 10;
      
      testPower[index] = spd;
      testSpeedLeft[index] = leftAvg;
      testSpeedRight[index] = rightAvg;
      index++;
    }
    
  }

  while(1)
  {
    Serial.println("Throttle:\tLeft Wheel:\tRight Wheel:");
    for (int i = 0; i < 100; i++)
    {
      Serial.print(testPower[i]);
      Serial.print("\t");
      Serial.print(testSpeedLeft[i]);
      Serial.print("\t");
      Serial.println(testSpeedRight[i]);
    }
    delay(20000);
  }

}
