#include "Arduino.h"
#include "Motor.h"
#include "Car.h"

//temporary fix to offset motor difference
const int wheelOffset = 7;

Car::Car(Motor *leftMotor, Motor *rightMotor){
	_motorLeft = leftMotor;
	_motorRight = rightMotor;
}

void Car::forward(int speed){
	_motorRight->forward(speed);
	_motorLeft->forward(speed - wheelOffset);
}

void Car::backward(int speed){
	_motorRight->backward(speed);
	_motorLeft->backward(speed - wheelOffset);
}

void Car::stop(){
	_motorRight->stop();
	_motorLeft->stop();
}

void Car::forwardInches(int inchesToTravel, int speed){
	float wheelCir = 12.56;
	//calculate the number of seconds to activate the motors to travel a distance
	float seconds = (inchesToTravel)/ (wheelCir) / (_motorRight->getRPS(speed));
	
	//turn the motors on
	_motorRight->forward(speed);
	_motorLeft->forward(speed - wheelOffset);
	
	//travel the distance
	delay(seconds * 1000);
	stop();
	
}

void Car::backwardInches(int inchesToTravel, int speed){
	float wheelCir = 12.56;
	float seconds = (inchesToTravel)/ (wheelCir) / (_motorRight->getRPS(speed));
	//Calculate how long to to activate motors to travel a distance
	
	_motorRight->backward(speed);
	_motorLeft->backward(speed - wheelOffset);
	
	delay(seconds * 1000);
	stop();
}

void Car::wait(int pin){
	pinMode(pin,INPUT);
  
	while(digitalRead(pin)==LOW){
		delay(3);
	}
}