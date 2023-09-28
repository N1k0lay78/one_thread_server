from socket import socket
from loguru import logger


class OneThreadServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__running = True
        self.sock = socket()
        self.buffers = {}
        self.pint_msg = "ping"
        self.separator = "\t"

    def run(self):
        """
        starts the main server loop
        """
        self.on_start()
        while self.__running:
            self.work()
        self.on_stop()

    def on_start(self):
        """
        starting the server
        """
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.sock.setblocking(False)
        logger.info("SERVER START")

    def work(self):
        """
        what does the server do
        """
        pass

    def on_stop(self):
        """
        executed when the server is shut down
        """
        self.sock.close()
        logger.info("SERVER CLOSED")

    def send(self, conn, msg, encoding="utf-8", auto_disconnect=True):
        """
        send message to client
        """
        try:
            conn.send(bytes(msg+self.separator, encoding))
            if auto_disconnect:
                self.recv(conn, size=1, auto_disconnect=True)
        except BlockingIOError:
            pass
        except ConnectionResetError:
            if auto_disconnect:
                self.on_connection_lost(conn)
        except OSError:
            if auto_disconnect:
                self.on_connection_lost(conn)

    def ping(self, conn, msg="ping", auto_disconnect=True):
        """
        ping client
        """
        self.send(conn, msg, auto_disconnect=auto_disconnect)

    def recv(self, conn, size=1024, encoding="utf-8", auto_disconnect=True):
        """
        recv message from client
        """
        try:
            self.buffers[conn] += conn.recv(size).decode(encoding)
            self.buffers[conn].replace(f"{self.pint_msg}{self.separator}", "")
        except BlockingIOError:
            pass
        except KeyError:
            pass
        except ConnectionAbortedError:
            if auto_disconnect:
                self.on_connection_lost(conn)
        except ConnectionResetError:
            if auto_disconnect:
                self.on_connection_lost(conn)

    def get_msg(self, conn, emp_msg=""):
        """
        return first message from buffer
        """
        if conn in self.buffers:
            msgs = self.buffers[conn].split(self.separator)
            if len(msgs) > 1:
                msg = msgs[0]
                self.buffers[conn] = self.separator.join(msgs[1:])
                return msg
        return emp_msg

    def on_connection_lost(self, conn):
        try:
            logger.info(f"CLIENT DISCONNECTED {conn.getsockname()}")
            self.buffers.pop(conn)
        except OSError:
            logger.info(f"CLIENT DISCONNECTED crashed")
        print(self.buffers)
        conn.close()

    def connect_clients(self):
        connections = []
        try:
            while True:
                connections.append(self.sock.accept()[0])
                logger.info(f"CLIENT CONNECTED    {connections[-1].getsockname()}")
        except BlockingIOError:
            pass
        for connection in connections:
            self.buffers[connection] = ""
        return connections

    def client_is_connected(self, conn):
        """
        check client is connected
        """
        try:
            conn.recv(1)
        except BlockingIOError:
            pass
        except ConnectionAbortedError:
            return False
        except ConnectionResetError:
            return False
        finally:
            return True

    def stop(self):
        """
        stops the server
        """
        self.__running = False
