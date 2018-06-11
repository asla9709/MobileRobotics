from select import select
import socket
import time
import _thread
import signal
from threading import Thread


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.255.255.255", 80))
    return s.getsockname()[0]


def init_socket(port):
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind(('', port))
    listen_sock.listen(10)

    return listen_sock

class App():
    def __init__(self):
        self.connected = False
        self.joystick_move = (0,0)
        self.manual = True

        self.connection = None

    def wait_for_connection(self):
        self.connected = False

        myip = get_ip()
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(('', 1234))


        s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        tcp_listener = init_socket(1236)

        while not self.connected:
            ready_to_read, _, _ = select([udp_socket, tcp_listener], [], [])
            for sock in ready_to_read:
                if sock == udp_socket:
                    msg, addr = udp_socket.recvfrom(1024)
                    print(msg.decode("utf-8"))
                    if "CAR?" in msg.decode("utf-8)"):
                        s2.sendto("CARIP:{}".format(myip).encode("utf-8"),
                                          (addr[0], 1235))
                elif sock == tcp_listener:
                    client, addr = tcp_listener.accept()
                    print("Got connection")
                    self.connected = True
                    self.connection = client

    def process_joystick(self,x,y):
        pass #todo process this crap


    def run_(self):
        while True:
            data = self.connection.recv(512)
            if data:
                data = data.decode("utf-8")
                data_split = data.split(',')
                x = y = None
                for i in range(len(data_split)):
                    if data_split[i] == "X":
                        x = data_split[i+1]
                    if data_split[i] == "Y":
                        y = data_split[i+1]
                        self.process_joystick(x,y)
                    if data_split[i] == "MODE":
                        self.manual = not self.manual
            else:
                self.connected = False
                self.connection.close()
                break

    def run(self):
        self.run_thread = Thread(target=self.run_)
        self.run_thread.start()

    def handle_exit(self):
        def exit_handler():
            self.connection.send("BYE".encode("utf-8"))
            time.sleep(0.1)
            print("BYE")
            self.connection.close()
        return exit


if __name__ == '__main__':

    while True:
        connection = wait_for_connection()
        try:
            while True:
                data = connection.recv(1024)
                if data:
                    print(data.decode("utf-8")+"\r")
                else:
                    connection.close()
                    break
        except KeyboardInterrupt:
            connection.send("BYE".encode(("UTF-8")))
            time.sleep(0.2)
            connection.close()
    # b_cast_ip()
