#include <Motor.h>
#include <Car.h>
#include <I2CEncoder.h>
#include <Wire.h>

const int startButton = 10;

const int LOOP_DELAY = 10; //ms
const double circum_inches = 12.56637; //inches

Motor leftMotor(2,3);
Motor rightMotor(4,5);
I2CEncoder leftEncoder;
I2CEncoder rightEncoder;
Car car(&leftMotor,&rightMotor, &leftEncoder, &rightEncoder);


void setup() {
  // put your setup code here, to run once: 
  Wire.begin();
  leftEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA,627);
  leftEncoder.unTerminate();
  leftEncoder.setReversed(true);
  rightEncoder.init(MOTOR_393_SPEED_ROTATIONS,MOTOR_393_TIME_DELTA,627);

  leftEncoder.zero();
  rightEncoder.zero();

  Serial.begin(9600);
  car.wait(startButton);
  Serial.println("Hi");
}

void loop() 
{
  forwardInchesTest(12, 50);
  delay(5000);
}


void forwardInchesTest(int inchesToTravel, int power){
  // get initial encoder positions
  double start_pos_left = Car::getDistanceInches(&leftEncoder); //in inches
  
  int right_power = power; // initially, right power is set to left power
  rightMotor.forward(right_power);
  leftMotor.forward(power);
  
  double distance = Car::getDistanceInches(&leftEncoder) - start_pos_left;
  double left_speed;
  double right_speed;
  
  while(distance < inchesToTravel){
    left_speed = leftEncoder.getSpeed();
    right_speed = rightEncoder.getSpeed();

    if(right_speed < left_speed){
      right_power += 1;
    } else if (right_speed > left_speed){
      right_power -= 1;
    }
    rightMotor.forward(right_power);
    
    delay(LOOP_DELAY);
    distance = Car::getDistanceInches(&leftEncoder) - start_pos_left;
  }
  car.stop();
}
