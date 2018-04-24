#include "Arduino.h"
#include "Motor.h"

Motor::Motor(int d_pin, int s_pin)
{
	pinMode(d_pin,OUTPUT);
	pinMode(s_pin,OUTPUT);
	_d_pin = d_pin;
	_s_pin = s_pin;
}


void Motor::forward(float speed){
	int conv_speed = map(speed,0,100,0,255);
	digitalWrite(_d_pin,LOW);
	analogWrite(_s_pin,conv_speed);
}

void Motor::backward(float speed){
	int conv_speed = map(speed,0,100,0,255);
	digitalWrite(_d_pin,HIGH);
	analogWrite(_s_pin,conv_speed);
}

void Motor::stop(){
	analogWrite(_s_pin,0);
	delay(20);
}

float Motor::getRPS(float throttlePercent){
	float returnRPS = 2.8833 * (throttlePercent / 100) - 0.1541;
	//Graphed data to get best fit line for the rotations per second
	//at various motor outputs

	return returnRPS;
}

float Motor::getLeftWheelSpeed(float throttlePercent){
	
	float leftWheelSpeed = 0.9487 * (throttlePercent / 100) - 0.0276;
	//Graphed data to to get best fit line for adjusting
	//the left wheel to match the right wheel at nominal battery power
	
	return leftWheelSpeed;
}