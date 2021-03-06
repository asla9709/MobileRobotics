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
#include "NewPing.h"

#define TICKS_PER_REVOLUTION 627.2

class Car
{		
	private:
		Motor *_motorLeft;
		Motor *_motorRight;
		I2CEncoder *_encoderLeft;
		I2CEncoder *_encoderRight;
		NewPing *_sonar;
		int _goalDistance;
		double _startDistance;
		int _leftPower;
		int _rightPower;
		unsigned long _lastCheckMillis;
	public:
		Car(Motor *leftMotor, Motor *rightMotor, I2CEncoder *leftEncoder, I2CEncoder *rightEncoder, NewPing *sonar);
		void wait(int pin);
		void forward (int speed); // speed is in the range 0 to 100
		void backward (int speed); // speed is in the range 0 to 100
		void turnLeft();
		void turnRight();
		void stop();
		bool forwardInches(int inchesToTravel, int power);
		void backwardInches(int inchesToTravel, int power);	
		static double getDistanceInches(I2CEncoder *encoder);
		void turnLeft90();
		void turnRight90();
		bool detectObstacle(int detectionThreshold = 12);
		void semiAutonomous();
		bool checkDistance();
		void correctDrift();
		void forwardInchesStart(int inchesToTravel, int power);
};
#endif	