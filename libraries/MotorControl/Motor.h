/*
	Motor.h 
	Created for lab 2
*/
	
#ifndef Motor_h
#define Motor_h
#include "Arduino.h"

class Motor
{
	public:
		Motor (int d_pin, int s_pin);
		void forward (float speed); // speed is in the range 0 to 255
		void backward (float speed); // speed is in the range 0 to 255
		void stop();
	private:
		int _d_pin;
		int _s_pin;
};
#endif