/*
	PhotoSensor.h 
	Created for lab 4
*/
	
#ifndef PhotoSensor_h
#define PhotoSensor_h
#include "Arduino.h"

#define LIGHT 		0
#define DARK		1

#define INITIAL_THRESHOLD		825 //best guess value to start, ideal value
#define SENSOR_MAX			1023
#define SENSOR_MIN			512
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
		//sensor thresholds
		int _leftThreshold;
		int _centerThreshold;
		int _rightThreshold;
		
	public:
		PhotoSensor(int leftPin, int centerPin, int rightPin);
		void calibrateSensors(bool leftStart = LIGHT, bool centerStart = LIGHT, bool rightStart = LIGHT);
		PSData getSensorData();
		PSData getThresholdData();
		int getLeftStatus();
		int getCenterStatus();
		int getRightStatus();
	
};

#endif	