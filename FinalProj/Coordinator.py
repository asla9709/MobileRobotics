import time
from arduino import Arduino
from app import App
from camera import Camera

class Status():
    AUTO = 1
    AUTO_OBSTACLE = 2
    AUTO_RED_LIGHT = 3
    MANUAL = 4


class Coordinator():
    def __init__(self, arduino: Arduino, camera: Camera, app: App):
        self.arduino = arduino
        self.camera = camera
        self.app = app
        self.status = Status.MANUAL

    def send_command(self):
        if self.app.manual:
            self.arduino.sendmove(self.app.joystick_move)
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
    arduino = Arduino(app)

    app.wait_for_connection()

    camera.run()
    app.run()
    arduino.run()

    coordinator = Coordinator(arduino,camera,app)
    counter = 0
    while True:
        coordinator.send_command()
        time.sleep(0.05)
        if counter > 100:
            counter = 0
            print(app.joystick_move)
        counter = counter + 1
