#include <Motor.h>
#include "Car.h"

const int startButton = 12;
Motor leftMotor(2,3);
Motor rightMotor(4,5);
Car thisCar(&leftMotor, &rightMotor);

void setup() {
  // put your setup code here, to run once:
  
  
  pinMode(startButton,INPUT);
    
  while(digitalRead(startButton)==LOW){
    delay(3);
  }
}

void loop() {
  square80();

}

void square50()
{
  //the power fluctuates, so this may require adjustment
  thisCar.forwardInches(50, 50);
  delay(1000);
  leftTurn50();
  delay(1000);
}

void leftTurn50()
{
  thisCar.stop();
  leftMotor.backward(44);
  rightMotor.forward(50);
  delay(685);
  thisCar.stop();
}

void square80()
{
  //the power fluctuates, so this may require adjustment
  thisCar.forwardInches(50, 80);
  delay(1000);
  leftTurn50();
  delay(1000);
}

void leftTurn80()
{
  
  thisCar.stop();
  leftMotor.backward(73.5);
  rightMotor.forward(80);
  delay(800);
  thisCar.stop();
}

