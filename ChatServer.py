from loguru import logger

from OneThreadServer import connection_decorator, OneThreadServer
from config import host, port


class ChatServer(OneThreadServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.users = []

    def work(self):
        self.connect_user()

        # --- resending messages ---
        # get messages from all users
        messages = []
        for i in range(len(self.users)):
            user = self.users[i]
            msg = self.get_message(user)
            if msg:
                messages.append([user, msg])
        # send messages
        for user, msg in messages:
            self.send_message(user, msg)

    def send_message(self, user, msg):
        """
        sends messages from one user to all other
        """
        logger.debug(f"USER {user.getsockname()} SEND: {msg}")
        for i in range(len(self.users)-1, -1, -1):
            if self.users[i] != user:
                self.users[i].send(bytes(msg, encoding="utf-8"))

                # --- check user is connected ---
                try:
                    self.users[i].recv(1)
                except BlockingIOError:
                    pass
                except ConnectionAbortedError:
                    # if lost connection - disconnect
                    logger.info(f"USER DISCONNECTED {self.users[i].getsockname()}")
                    self.users[i].close()
                    self.users.pop(i)

    @connection_decorator(default="", is_ignore_abort=True)
    def get_message(self, conn, size=1024):
        """
        receiving a message from a user
        """
        return conn.recv(size).decode()

    @connection_decorator()
    def connect_user(self):
        """
        connect user to server
        """
        conn, _ = self.sock.accept()
        self.users.append(conn)
        logger.info(f"USER CONNECTED    {conn.getsockname()}")


if __name__ == '__main__':
    ChatServer(host, port).run()