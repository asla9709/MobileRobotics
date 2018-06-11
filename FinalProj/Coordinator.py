import time
from enum import Enum
from arduino import Arduino
from app import App
from camera import Camera

class Status(Enum):
    AUTO = 1
    AUTO_OBSTACLE = 2
    AUTO_RED_LIGHT = 3
    MANUAL = 4


class Coordinator():
    def __init__(self, arduino, camera, app):
        self.arduino = arduino
        self.camera = camera
        self.app = app
        self.status = Status.MANUAL

    def send_command(self):
        if self.app.manual:
            self.arduino.sendmov(self.app.joystick_move)
            self.app.set_status(Status.MANUAL)
        else:
            if self.arduino.obstacle:
                self.arduino.sendmove((0, 0))
                self.app.set_status(Status.AUTO_OBSTACLE)

            elif self.camera.stoplight_detected:
                self.arduino.sendmove((0, 0))
                self.app.set_status(Status.AUTO_RED_LIGHT)

            else:
                self.arduino.sendmove(self.camera.suggested_move)
                self.app.set_status(Status.AUTO)

if __name__ == '__main__':
    camera = Camera()
    app = App()
    arduino = Arduino()

    app.wait_for_connection()

    camera.run()
    app.run()
    arduino.run()

    coordinator = Coordinator(arduino,camera,app)
    while True:
        coordinator.send_command()
        time.sleep(0.05)