from socket import socket
from time import time

from loguru import logger

from config import host_port


class OneThreadClient:
    def __init__(self, host_port):
        self.conn = None
        self.__running = True
        self.host_port = host_port
        self.pint_msg = "ping"
        self.buffer = ""
        self.separator = "\t"
        self.is_connected = False
        self.connect_timer = 0
        self.ping_delta = 7
        self.ping_time = 0

    def start(self):
        """
        connecting to the server
        """
        try:
            if not self.is_connected:
                self.conn = socket()
                self.conn.connect(self.host_port)
                self.conn.setblocking(False)
                logger.info("CONNECTED TO THE SERVER")
                self.is_connected = True
                self.ping_time = time()
        except OSError:
            self.is_connected = False

    def update(self):
        """
        what does the client do
        """
        if not self.is_connected and time() - self.connect_timer > 5:
            print("TRY TO CONNECT")
            self.start()
            self.connect_timer = time()
        if time() - self.ping_time > self.ping_delta and self.is_connected:
            self.on_connection_lost()

    def send(self, msg, encoding="utf-8", auto_disconnect=True):
        """
        send message to server
        """
        self.conn.send(bytes(msg+self.separator, encoding))
        if auto_disconnect:
            self.recv(size=1, auto_disconnect=True)

    def recv(self, size=1024, encoding="utf-8", auto_disconnect=True):
        """
        recv message from server
        """
        try:
            if self.is_connected:
                self.buffer += self.conn.recv(size).decode(encoding)
                if f"{self.pint_msg}{self.separator}" in self.buffer:
                    self.ping_time = time()
                    self.buffer.replace(f"{self.pint_msg}{self.separator}", "")
        except BlockingIOError:
            pass
        except ConnectionAbortedError:
            if auto_disconnect:
                self.on_connection_lost()
        except ConnectionResetError:
            if auto_disconnect:
                self.on_connection_lost()

    def get_msg(self, emp_msg=""):
        """
        return first message from buffer
        """
        msgs = self.buffer.split(self.separator)
        if len(msgs) > 1:
            msg = msgs[0]
            self.buffer = self.separator.join(msgs[1:])
            return msg
        return emp_msg

    def on_connection_lost(self):
        """
        execute when lost connection with server
        """
        self.stop()

    def stop(self):
        """
        disconnecting from the server
        """
        self.conn.close()
        logger.info("DISCONNECTED FROM THE SERVER")
        self.is_connected = False


if __name__ == '__main__':
    client = OneThreadClient(host_port)
    client.start()
    input()
    client.stop()
