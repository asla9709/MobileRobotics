import time
from threading import Thread


class Testo():
    def __init__(self):
        self.a = 0

    def run_(self):
        while True:
            self.a = self.a + 1
            time.sleep(1)

    def run(self):
        thread = Thread(target = self.run_)
        thread.start()

if __name__ == '__main__':
    testo = Testo()
    print(testo.a)
    testo.run()
    while True:
        print(testo.a)
        time.sleep(1.1)