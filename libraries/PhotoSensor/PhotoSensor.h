/*
	PhotoSensor.h 
	Created for lab 4
*/
	
#ifndef PhotoSensor_h
#define PhotoSensor_h
#include "Arduino.h"

struct PSData_t
{
	double leftRes;
	double centerRes;
	double rightRes;
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
		
};

#endif	