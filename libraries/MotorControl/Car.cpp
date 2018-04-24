#include "Arduino.h"
#include "Motor.h"
#include "Car.h"
#include "I2CEncoder.h"
#include "Wire.h"
#include "NewPing.h"
#include "time.h"
#include "stdlib.h"

//temporary fix to offset motor difference
const int wheelOffset = 7;
const double ticksPerRot = 627.2;
const double wheelDiam = 10.16; //10.16 cm, 4 inches 

Car::Car(Motor *leftMotor, Motor *rightMotor, I2CEncoder *leftEncoder, I2CEncoder *rightEncoder, NewPing *sonar)
{
	_motorLeft = leftMotor;
	_motorRight = rightMotor;
	_encoderLeft = leftEncoder;
	_encoderRight = rightEncoder;
	_sonar = sonar;
	srand(time(NULL)); //initialize random generator for autonomous decisions
}

void Car::forward(int speed)
{
	_motorRight->forward(speed);
	_motorLeft->forward(speed - wheelOffset);
}

void Car::backward(int speed)
{
	_motorRight->backward(speed);
	_motorLeft->backward(speed - wheelOffset);
}

void Car::stop()
{
	_motorRight->stop();
	_motorLeft->stop();
}

bool Car::forwardInches(int inchesToTravel, int speed)
{
	//bool return true if car senses obstacle
	
	
	
	
	//old code
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

void Car::backwardInches(int inchesToTravel, int speed)
{
	float wheelCir = 12.56;
	float seconds = (inchesToTravel)/ (wheelCir) / (_motorRight->getRPS(speed));
	//Calculate how long to to activate motors to travel a distance
	
	_motorRight->backward(speed);
	_motorLeft->backward(speed - wheelOffset);
	
	delay(seconds * 1000);
	stop();
}

void Car::wait(int pin)
{
	pinMode(pin,INPUT);
  
	while(digitalRead(pin)==LOW){
		delay(3);
	}
}

void Car::turnLeft90()
{
	
}
void Car::turnRight90()
{
	
}

bool Car::detectObstacle()
{
	int detectionThreshold = 8; //8 inch threshold;
	int distance = _sonar->ping_in();
	if (distance > 0 && distance <= detectionThreshold)
	{
		return true;
	}
	return false;
}
void Car::semiAutonomous()
{
	//make semi-autonomous decisions if obstacles are detected
	while (1)
	{
		if (!forwardInches(24, 50))
		{
			//if an obstacle was detected, go backwards a little and turn
			backwardInches(5, 50);
			if (rand() % 2 == 0) //randomly choose left or right
			{
				turnRight90();
			}
			else
			{
				turnLeft90();
			}
		}
	}
	
}