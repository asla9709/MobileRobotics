
int redLightPin = 13; //LED connected to digital pin 13
int yellowLightPin = 12; //LED connected to digital pin 12
int greenLightPin = 11; //LED connected to digital pin 11
int modePin = 7;
int analogSpeedPin = 1;
int oneSecond = 1000; //one second in millis
volatile int mode;
volatile int modeChanged;
int analogValue;

void setup() {
  // put your setup code here, to run once:
  pinMode(redLightPin, OUTPUT); // sets the digital pin as output
  pinMode(yellowLightPin, OUTPUT); // sets the digital pin as output
  pinMode(greenLightPin, OUTPUT); // sets the digital pin as output
  

  mode = 0;
  modeChanged = 0;
  attachInterrupt(digitalPinToInterrupt(modePin), changeMode, HIGH);
  Serial.begin(9600);      // open the serial port at 9600 bps:
}

void loop() {
  // put your main code here, to run repeatedly:
  analogValue = analogRead(analogSpeedPin);
  Serial.println(analogValue);
  
  if (mode == 0)
  {
    digitalWrite(greenLightPin, HIGH); // turn on LED
    delay(10 * analogValue); // waits for 4 seconds
    digitalWrite(greenLightPin, LOW); // turn off LED
    digitalWrite(yellowLightPin, HIGH); // turn on LED
    delay(analogValue); // waits for a second
    digitalWrite(yellowLightPin, LOW); // turn off LED
    digitalWrite(redLightPin, HIGH); // turn on LED
    delay(5 * analogValue); // waits for 3 seconds
    digitalWrite(redLightPin, LOW); // turn off LED
    delay(analogValue); // waits for a second
  }
  if (mode == 1)
  {
    digitalWrite(redLightPin, HIGH); // turn on LED
    delay(5 * analogValue); // waits for a second
    digitalWrite(redLightPin, LOW); // turn on LED
    delay(5 * analogValue); // waits for a second
  }

  modeChanged = 0;
  
  
}

void changeMode()
{
  //flip the mode, but only if it has not been changed this cycle
  if (modeChanged == 0)
  {
    if (mode == 1)
    {
      mode = 0;
    }
    else if(mode == 0)
    {
      mode = 1;
    }
    modeChanged = 1;
  }
  
}

