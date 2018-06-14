import time
from app import App
import serial
from threading import Thread

def clamp(num, range):
    return min(max(num,range[0]),range[1])

class Arduino:
    def __init__(self, app):
        self.app = app
        self.ser = serial.Serial("/dev/ttyACM0", 9600)
        self.ser.flushInput()
        self.obstacle = False
        self.dist = 0
        self.light_sensor = (False, False, False)
        self.speed = 0
        self.data = ""

    def run_(self):
        while True:
            self.get_data()
            time.sleep(0.1)
            self.app.send_data(self)

    def run(self):
        self.run_thread = Thread(target=self.run_)
        self.run_thread.start()

    def sendmove(self, sendTuple):
        x = clamp(sendTuple[0], [-100, 100]) + 100
        y = clamp(sendTuple[1], [-100, 100]) + 100
        dataLine = "X{}V{}\n".format(x, y)
        self.ser.write(dataLine.encode('utf-8'))

    def get_data(self):
        data = self.ser.read()
        data = data.decode('utf-8')
        self.data = self.data + data
        if ("\n" in self.data):
            data_fields = self.data.split("::")
            self.obstacle = bool(data_fields[0])
            self.dist = int(data_fields[1])
            self.light_sensor = (bool(data_fields[2]), bool(data_fields[3]), bool(data_fields[4]))
            self.speed = int(data_fields[5])
            self.data = ""


