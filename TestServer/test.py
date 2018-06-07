from select import select
import socket
import time
import signal

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


def b_cast_ip():
    myip = get_ip()
    udp_sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
    # udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
    while True:
        udp_sock.sendto("CARIP:{}".format(myip).encode("utf-8"),
                        #           ("255.255.255.255",5144))
                        ('192.168.1.129', 1234))
        time.sleep(1)


def listen_b_cast():
    myip = get_ip()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 1234))
    while True:
        msg, addr = s.recvfrom(4096)
        print(msg.decode("utf-8"))
        print(addr)
        s2.sendto("CARIP:{}".format(myip).encode("utf-8"), (addr[0], 1235))


def wait_for_connection():
    connected = False

    myip = get_ip()
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', 1234))


    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    tcp_listener = init_socket(1236)

    while not connected:
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
                connected = True
                return client

def handle_exit(socket):
    def exit_handler():
        socket.send("BYE".encode("utf-8"))
        time.sleep(0.1)
        print("BYE")
        socket.close()
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
