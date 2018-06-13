import serial

class Arduino:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyACM0", 9600)
        self.ser.flushInput()

    def run(self):
        pass

