/*
	Car.h 
	Created for lab 2
*/
	
#ifndef Car_h
#define Car_h
#include "Arduino.h"
#include "Motor.h"
#include "I2CEncoder.h"
#include "Wire.h"

class Car
{		
	private:
		Motor *_motorLeft;
		Motor *_motorRight;
		I2CEncoder *_encoderLeft;
		I2CEncoder *_encoderRight;
		
	public:
		Car(Motor *leftMotor, Motor *rightMotor, I2CEncoder *leftEncoder, I2CEncoder *rightEncoder);
		void forward (int speed); // speed is in the range 0 to 100
		void backward (int speed); // speed is in the range 0 to 100
		void stop();
		void forwardInches(int inchesToTravel, int speed);
		void backwardInches(int inchesToTravel, int speed);	
		void wait(int pin);
		
};
#endif	