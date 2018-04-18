#include <Car.h>
#include <Motor.h>

const int startButton = 12;

Motor leftMotor(2,3);
Motor rightMotor(4,5);
Car myCar(&leftMotor,&rightMotor);

void setup() {
   pinMode(startButton,INPUT);
  
  while(digitalRead(startButton)==LOW){
    delay(3);
  }
}

void loop() {
    
    //Right turn, radius 2.5 ish feet, 145 degrees 
    circleRight();
    delay(500);
    circleLeft();

    delay(20000000);


    
    myCar.forwardInches(30,50);
    
    //Left turn, radius 2 feet, 145 degrees
    leftMotor.forward(25);
    rightMotor.forward(50);
    delay(11000);
    leftMotor.stop();
    rightMotor.stop();

    myCar.forwardInches(30,50);
}

void circleRight()
{
    leftMotor.forward(50);
    rightMotor.forward(30);
    delay(12000);
    leftMotor.stop();
    rightMotor.stop();
  
} 

void circleLeft()
{
    leftMotor.forward(25);
    rightMotor.forward(50);
    delay(12000);
    leftMotor.stop();
    rightMotor.stop();
}


