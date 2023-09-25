from loguru import logger

from OneThreadServer import OneThreadServer
from config import host, port


class ChatServer(OneThreadServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.users = []

    def work(self):
        self.users.extend(self.connect_clients())

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
        for i in range(len(self.users) - 1, -1, -1):
            if self.users[i] != user:
                self.send(self.users[i], msg)

    def on_connection_lost(self, conn):
        super().on_connection_lost(conn)
        self.users.remove(conn)

    def get_message(self, conn, size=1024):
        """
        receiving a message from a user
        """
        return self.recv(conn, size)


if __name__ == '__main__':
    ChatServer(host, port).run()