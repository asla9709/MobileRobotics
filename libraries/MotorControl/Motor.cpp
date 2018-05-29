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
	//analogWrite(_s_pin,conv_speed);
	analogWrite(_s_pin, speed);
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