import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

ledPins = {'green':11, 'yellow':13, 'red':15}
buttonPin = 16
GPIO.setup(buttonPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
for led_pin in ledPins.values():
    GPIO.setup(led_pin, GPIO.OUT)


blink_mode = False;
while True:
    if not GPIO.input(buttonPin):
        # button pressed
        blink_mode = not blink_mode
    if blink_mode:
        GPIO.output(ledPins['red'], False)
        GPIO.output(ledPins['green'], False)
        GPIO.output(ledPins['yellow'], False)
        time.sleep(0.5)
        GPIO.output(ledPins['red'],True)
        time.sleep(0.5)
    else:
        GPIO.output(ledPins['red'], False)
        GPIO.output(ledPins['green'], True)
        GPIO.output(ledPins['yellow'], False)
        time.sleep(1.5)
        GPIO.output(ledPins['green'], False)
        GPIO.output(ledPins['yellow'], True)
        time.sleep(1)
        GPIO.output(ledPins['yellow'], False)
        GPIO.output(ledPins['red'], True)
        time.sleep(1.5)

        
