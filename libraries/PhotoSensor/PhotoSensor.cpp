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

int PhotoSensor::getLeftStatus()
{
	if (analogRead(_leftSensor) >= LIGHT_THRESHOLD)
	{
		return Dark;
	}
	return Light;
}

int PhotoSensor::getCenterStatus()
{
	if (analogRead(_centerSensor) >= LIGHT_THRESHOLD)
	{
		return Dark;
	}
	return Light;
}

int PhotoSensor::getRightStatus()
{
	if (analogRead(_rightSensor) >= LIGHT_THRESHOLD)
	{
		return Dark;
	}
	return Light;
}