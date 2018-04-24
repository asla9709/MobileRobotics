#include "Arduino.h"
#include "Motor.h"
#include "Car.h"
#include "I2CEncoder.h"
#include "Wire.h"

//temporary fix to offset motor difference
const int wheelOffset = 7;
const int LOOP_DELAY = 10; //ms
const double circum_inches = 12.56637; //inches

Car::Car(Motor *leftMotor, Motor *rightMotor, I2CEncoder *leftEncoder, I2CEncoder *rightEncoder)
{
	_motorLeft = leftMotor;
	_motorRight = rightMotor;
	_encoderLeft = leftEncoder;
	_encoderRight = rightEncoder;
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

void Car::forwardInches(int inchesToTravel, int power)
{
	// get initial encoder positions
	double start_pos_left = getDistanceInches(_encoderLeft); //in inches
	
	int right_power = power; // initially, right power is set to left power
	_motorRight->forward(right_power);
	_motorLeft->forward(power);
	
	double distance = getDistanceInches(_encoderLeft) - start_pos_left;
	double left_speed;
	double right_speed;
	
	while(distance < inchesToTravel){
		left_speed = _encoderLeft->getSpeed();
		right_speed = _encoderRight->getSpeed();

		if(right_speed < left_speed){
			right_power += 1;
		} else if (right_speed > left_speed){
			right_power -= 1;
		}
		_motorRight->forward(right_power);
		
		delay(LOOP_DELAY);
		distance = getDistanceInches(_encoderLeft) - start_pos_left;
	}
	
}

void Car::backwardInches(int inchesToTravel, int power)
{
	// get initial encoder positions
	double start_pos_left = getDistanceInches(_encoderLeft); //in inches
	
	int right_power = power; // initially, right power is set to left power
	_motorRight->backward(right_power);
	_motorLeft->backward(power);
	
	double distance = -(getDistanceInches(_encoderLeft) - start_pos_left);
	double left_speed;
	double right_speed;
	
	while(distance < inchesToTravel){
		left_speed = _encoderLeft->getSpeed();
		right_speed = _encoderRight->getSpeed();

		if(right_speed < left_speed){
			right_power += 1;
		} else if (right_speed > left_speed){
			right_power -= 1;
		}
		_motorRight->backward(right_power);
		
		delay(LOOP_DELAY);
		distance = -(getDistanceInches(_encoderLeft) - start_pos_left);
	}
	
}

void Car::wait(int pin)
{
	pinMode(pin,INPUT);
  
	while(digitalRead(pin)==LOW){
		delay(3);
	}
}

static double Car::getDistanceInches(I2CEncoder *encoder)
{
	return (encoder->getRawPosition() / TICKS_PER_REVOLUTION) * circum_inches;
}