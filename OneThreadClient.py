from socket import socket
from loguru import logger

from config import host_port


class OneThreadClient:
    def __init__(self, host_port):
        self.conn = socket()
        self.__running = True
        self.host_port = host_port
        self.pint_msg = "ping"

    def start(self):
        """
        connecting to the server
        """
        self.conn.connect(self.host_port)
        self.conn.setblocking(False)
        logger.info("CONNECTED TO THE SERVER")

    def update(self):
        """
        what does the client do
        """
        pass

    def send(self, msg, encoding="utf-8", auto_disconnect=True):
        """
        send message to server
        """
        self.conn.send(bytes(msg, encoding))
        if auto_disconnect:
            self.recv(size=1, auto_disconnect=True)

    def recv(self, size=1024, encoding="utf-8", auto_disconnect=True, emp_msg="", err_msg=""):
        """
        recv message from server
        """
        try:
            msg = self.conn.recv(size).decode(encoding)
            if msg != self.pint_msg:
                return msg
            return ""
        except BlockingIOError:
            return emp_msg
        except ConnectionAbortedError:
            if auto_disconnect:
                self.on_connection_lost()
        except ConnectionResetError:
            if auto_disconnect:
                self.on_connection_lost()
        finally:
            return err_msg

    def on_connection_lost(self):
        logger.info(f"DISCONNECTED {self.conn.getsockname()}")
        self.conn.close()

    def stop(self):
        """
        disconnecting from the server
        """
        self.conn.close()
        logger.info("DISCONNECTED FROM THE SERVER")


if __name__ == '__main__':
    client = OneThreadClient(host_port)
    client.start()
    input()
    client.stop()
