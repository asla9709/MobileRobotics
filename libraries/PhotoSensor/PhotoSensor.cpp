#include "Arduino.h"
#include "PhotoSensor.h"



PhotoSensor::PhotoSensor(int leftPin, int centerPin, int rightPin)
{
	_leftSensor = leftPin;
	_centerSensor = centerPin;
	_rightSensor = rightPin;
	
	_leftThreshold = INITIAL_THRESHOLD;
	_centerThreshold = INITIAL_THRESHOLD;
	_rightThreshold = INITIAL_THRESHOLD;
}

void PhotoSensor::calibrateSensors()
{
	//This takes an initial values and does
	//some math stuff to try to figure out some thresholds
	unsigned long sum[3]; 
	int avg[3];
	for (int index = 0; index <3; index++)
	{
		sum[index] = 0;
	}
	
	for (int index = 0; index < 20; index ++)
	{
		PSData sensorData = getSensorData();
		sum[0] += sensorData.leftRes;
		sum[1] += sensorData.centerRes;
		sum[2] += sensorData.rightRes;
	}
	for (int index = 0; index <3; index++)
	{
		
		avg[index] = sum[index] / 20;
	}


	//center sensor is on a line
	//adjust values based on read numbers
	double idealFloorAverage = 727; //value calculated in testing
	double darkTapeAverage = 911;
	_leftThreshold = INITIAL_THRESHOLD *(avg[0] / idealFloorAverage);
	_centerThreshold = INITIAL_THRESHOLD *(avg[1] / darkTapeAverage); //calibrate on tark
	_rightThreshold = INITIAL_THRESHOLD *(avg[2] / idealFloorAverage);

	
}

PSData PhotoSensor::getSensorData()
{
	PSData sensorData;
	
	sensorData.leftRes = analogRead(_leftSensor);
	sensorData.centerRes = analogRead(_centerSensor);
	sensorData.rightRes = analogRead(_rightSensor);
	
	return sensorData;
}

PSData PhotoSensor::getThresholdData()
{
	PSData sensorData;
	
	sensorData.leftRes = _leftThreshold;
	sensorData.centerRes = _centerThreshold;
	sensorData.rightRes = _rightThreshold;
	
	return sensorData;
}

int PhotoSensor::getLeftStatus()
{
	if (analogRead(_leftSensor) >= _leftThreshold)
	{
		return Dark;
	}
	return Light;
}

int PhotoSensor::getCenterStatus()
{
	if (analogRead(_centerSensor) >= _centerThreshold)
	{
		return Dark;
	}
	return Light;
}

int PhotoSensor::getRightStatus()
{
	if (analogRead(_rightSensor) >= _rightThreshold)
	{
		return Dark;
	}
	return Light;
}