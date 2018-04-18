/*:*******************************************************************
: CE-442 Intro to Mobile Robotics
: Instructor: Professor Tewolde
: Author: Caspian Peavyhouse and Amber Wackerly
: Lab 1: Introduction to Arduino and Programming
:
: Description: This program models a time based stoplight with two modes and 
: time/brightness control.  Mode 0 is a normal stoplight that cycles between green, 
: yellow and red. Mode 1 is a simple stoplight that only flashes the red light.  
: Control for the length and intesity of the lights is provided by 2 potentiometers 
: on the board.
:
: Hardware: The board used is a SainSmart Uno board. Additional components used:
: 3 Led's (RGY), 1 button, 2 10k potentiometers, 3 120 Ohm, 1 10k Ohm resistor
:
: Program input/output: The inputs of the program are are 
: Push button: Swithces the mode after a cycle
: Potentiometer 1:  (A1) Controls the delay between light transitions
: Potentiometer 2: (A2) Controls the intensity of the  the light
: Output: RGY Led light
: **********************************************************************
*/

int redLightPin = 11; //LED connected to digital/PWM pin 11
int yellowLightPin = 10; //LED connected to digital/PWM pin 10
int greenLightPin = 9; //LED connected to digital/PWM pin 9
int modePin = 2; //Input pin connected to the mode push button
int analogSpeedPin = 1; //A1 pin connected to the speed potentiometer
int analogBrightnessPin = 2; //A2 pin connected to the brighness potent.
int brightness; //Holds the brighness value sampled at the start of a cycle
int Speed; // Holds the speed value sampled at the start of a cycle
volatile int mode; //Holds the current mode of execution (set by interrupt)
volatile int modeChanged; //Ensures the mode is only changed once per cycle

void setup() {
  // put your setup code here, to run once:
  pinMode(redLightPin, OUTPUT); // sets the digital pin as output
  pinMode(yellowLightPin, OUTPUT); // sets the digital pin as output
  pinMode(greenLightPin, OUTPUT); // sets the digital pin as output
  

  mode = 0; //Set the initial mode to mode 0
  modeChanged = 0; //set initial value for modeChanged

  //attach an interrupt to execute when mode change button is pressed
  attachInterrupt(digitalPinToInterrupt(modePin), changeMode, HIGH);
  //debug output
  Serial.begin(9600);      // open the serial port at 9600 bps:
}

void loop() {
  // put your main code here, to run repeatedly:
  Speed = analogRead(analogSpeedPin); //sample the speed potentiometer

  //( /4 )  pull potentiometer (0-1023) into analog output range (0-255)
  brightness = analogRead(analogBrightnessPin) / 4; //sample the brightness
  //debug output
  //Serial.println("Speed:" + Speed);
  //Serial.println("Brightness:" + brightness);

  digitalRead
  
  if (mode == 0)
  {
    //Green Light
    analogWrite(greenLightPin, brightness); //Turn on the LED
    delay(10 * Speed); // waits for 10x milliseconds

    //Yellow Light
    analogWrite(greenLightPin, 0); //Turn off the LED
    analogWrite(yellowLightPin, brightness); //Turn on the LED
    delay(1000); // waits for x milliseconds

    //Red Light
    analogWrite(yellowLightPin, 0); //turn off the LED
    analogWrite(redLightPin, brightness); // turn on the led
    delay(5 * Speed); // waits for 5x milliseconds

    //Off
    analogWrite(redLightPin, 0); //turn LED off    
    delay(1 * Speed); // waits for x milliseconds
  }
  if (mode == 1)//(V1.2-1.4)
  {
    analogWrite(redLightPin, brightness); //Flash the LED on
    delay(5 * Speed); // waits for 5x millis
    
    analogWrite(redLightPin, 0); //Turn off the LED
    delay(5 * Speed); // waits for 5x millis
  }

  modeChanged = 0; //reset the modeChanged bit
   
}

void changeMode()
{
  //ISR called when the the change mode button is pressed.
  
  //flip the mode, but only if it has not been changed this cycle
  if (modeChanged == 0) // if the mode has been changed, ignore button press
  {
    if (mode == 1)
    {
      mode = 0;
    }
    else if(mode == 0)
    {
      mode = 1;
    }
    modeChanged = 1; //Set mode changed bit
  }
  
}

