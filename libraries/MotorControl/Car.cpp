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

const int LOOP_DELAY = 10; //ms
const double circum_inches = 12.56637; //inches
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

void Car::turnRight()
{
	_motorLeft->backward(0);
	_motorRight->forward(40);
}

void Car::turnLeft()
{
	_motorLeft->forward(40);
	_motorRight->backward(0);
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


bool Car::forwardInches(int inchesToTravel, int power)
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
		
		if(detectObstacle()){
			stop();
			return false;
		}
		
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
	stop();
	return true;
}
void Car::forwardInchesStart(int inchesToTravel, int power)
{
	//set distances
	_startDistance = getDistanceInches(_encoderLeft); //in inches
	_goalDistance = inchesToTravel;
	//set power levels
	_rightPower = power; 
	_leftPower = power;
	//start motors
	_motorRight->forward(_rightPower);
	_motorLeft->forward(_leftPower);
}

bool Car::checkDistance()
{
	double distance = getDistanceInches(_encoderLeft) - _startDistance;
	if(distance > _goalDistance){
		return true;
	}
	else return false;
}

void Car::correctDrift()
{
	double left_speed = _encoderLeft->getSpeed();
	double right_speed = _encoderRight->getSpeed();
	
	double difference = right_speed - left_speed;
	//double difference = left_speed - right_speed;

	/**if(right_speed < left_speed){
		_rightPower += 1;
	} else if (right_speed > left_speed){
		_rightPower -= 1;
	}**/
	
	//_rightPower += (int) round(difference / 15.0);
	//_motorRight->forward(_rightPower);
		
	_leftPower += (int) round(difference / 15.0);
	_motorLeft->forward(_leftPower);
	
	/**Serial.print(left_speed);
	Serial.print("\t");
	Serial.print(right_speed);
	Serial.print("\t");
	Serial.println(_rightPower);**/
	
	
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
	stop();
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

void Car::turnLeft90()
{
	double turnRadius = 5.1478; //approximate value for the wheel
	double pi = 3.14159265359;
	double circumference = 2 * turnRadius * pi;
	double inchesToTravel = (90.0/75) * (90.0/ 360.0) * circumference;
	
	double start_pos_right = getDistanceInches(_encoderRight); //in inches
	double distance = getDistanceInches(_encoderRight) - start_pos_right;
	
	while (distance < inchesToTravel)
	{
		_motorLeft->backward(50);
		_motorRight->forward(50);
		delay(LOOP_DELAY);
		distance = getDistanceInches(_encoderRight) - start_pos_right;
	}
	
	stop();
}
void Car::turnRight90()
{
	double turnRadius = 5.1478; //approximate value for the wheel
	double pi = 3.14159265359;
	double circumference = 2 * turnRadius * pi;
	double inchesToTravel = (90.0/82) * (90.0/ 360.0) * circumference; //coefficient
	
	double start_pos_left = getDistanceInches(_encoderLeft); //in inches
	double distance = getDistanceInches(_encoderLeft) - start_pos_left;
	
	while (distance < inchesToTravel)
	{
		_motorLeft->forward(50);
		_motorRight->backward(50);
		delay(LOOP_DELAY);
		distance = getDistanceInches(_encoderLeft) - start_pos_left;
	}
	stop();
}

bool Car::detectObstacle(int detectionThreshold = 12)
{
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
		if (!forwardInches(240, 50))
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