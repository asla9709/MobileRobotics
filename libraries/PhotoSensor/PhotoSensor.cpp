#include "Arduino.h"
#include "PhotoSensor.h"



PhotoSensor::PhotoSensor(int leftPin, int centerPin, int rightPin)
{
	_leftSensor = leftPin;
	_centerSensor = centerPin;
	_rightSensor = rightPin;
}

PSData PhotoSensor::getSensorData()
{
	PSData sensorData;
	
	sensorData.leftRes = analogRead(_leftSensor);
	sensorData.centerRes = analogRead(_centerSensor);
	sensorData.rightRes = analogRead(_rightSensor);
	
	return sensorData;
}