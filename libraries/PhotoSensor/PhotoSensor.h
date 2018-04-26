/*
	PhotoSensor.h 
	Created for lab 4
*/
	
#ifndef PhotoSensor_h
#define PhotoSensor_h
#include "Arduino.h"

#define Light 		0
#define Dark		1

#define LIGHT_THRESHOLD		825
//Above threshold, sense dark
//below, senses light

struct PSData_t
{
	int leftRes;
	int centerRes;
	int rightRes;
};
typedef struct PSData_t PSData;

class PhotoSensor
{		
	
	private:
		int _leftSensor;
		int _centerSensor;
		int _rightSensor;
		
	public:
		PhotoSensor(int leftPin, int centerPin, int rightPin);
		PSData getSensorData();
		int getLeftStatus();
		int getCenterStatus();
		int getRightStatus();
	
};

#endif	