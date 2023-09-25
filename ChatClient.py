from socket import socket
from config import host_port


class Client:
    def __init__(self, host_port, work=False):
        self.con = socket()
        self.con.connect(host_port)
        self.work = work

    def run(self):
        while True:
            msg = input()
            self.con.send(bytes(msg, encoding="utf-8"))
            if msg == "bb":
                break
            print(self.con.recv(1024))
        self.con.close()


if __name__ == '__main__':
    Client(host_port).run()
