import serial

class Arduino:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyACM0", 9600)
        self.ser.flushInput()
        self.obstacle = 0
        self.dist = 0
        self.light_sensor = (0, 0, 0)
        self.speed = 0

    def run(self):
        pass

    def send_move(self, sendTuple):
        dataLine = "X{0}V{1}\n".format(int(sendTuple[0]), int(sendTuple[1]))
        self.ser.write(dataLine.encode('utf-8'))

    def get_data(self):
