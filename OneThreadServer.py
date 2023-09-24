from socket import socket
from loguru import logger


def connection_decorator(default=None, is_ignore_abort=False, info=""):
    """
    decorator for functions working with connections
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except BlockingIOError:
                pass
            except ConnectionAbortedError as ex:
                if is_ignore_abort:
                    logger.error(f"LOST CONNECTION {info = }")
                else:
                    raise ex
            except ConnectionResetError as ex:
                if is_ignore_abort:
                    logger.error(f"USER HIMSELF DISCONNECTED {info = }")
                else:
                    raise ex
            return default
        return wrapper
    return decorator


class OneThreadServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__running = True
        self.sock = socket()

    def run(self):
        """
        starts the main server loop
        """
        self.on_start()
        while self.__running:
            self.work()
        self.on_stop()

    @connection_decorator()
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

    @connection_decorator()
    def on_stop(self):
        """
        executed when the server is shut down
        """
        self.sock.close()
        logger.info("SERVER CLOSED")

    def stop(self):
        """
        stops the server
        """
        self.__running = False
