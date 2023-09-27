from OneThreadClient import OneThreadClient
from config import host_port


class TicTacToeClient(OneThreadClient):
    def __init__(self, host_port):
        super().__init__(host_port)
        self.at_game = False
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.type = 0
        self.step = 1

    def send_move(self, x, y):
        self.send(f"move {x} {y}")

    def update(self):
        msg = self.recv()
        if msg == "win":
            print("WIN")
        elif msg == "lose":
            print("LOSE")
        elif msg.startswith("type"):
            self.type = int(msg.split()[1])
            self.at_game = True
            print("start game")
        elif msg.startswith("board"):
            st, bo = msg.split()[1:]
            self.step = int(st)
        elif msg == "end":
            self.at_game = False
            print("end game")

    def is_at_game(self):
        return self.is_at_game()

    def get_board(self):
        return self.board

    def get_type(self):
        return self.type

    def get_step(self):
        return self.step

    def load_board(self, line):
        for y in range(3):
            for x in range(3):
                self.board[y][x] = int(line[y * 3 + x])


if __name__ == '__main__':
    client = TicTacToeClient(host_port)

    client.load_board("111000000")
    assert client.get_board() == [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
    client.load_board("111210021")
    assert client.get_board() == [[1, 1, 1], [2, 1, 0], [0, 2, 1]]

    print("All tests passed")
