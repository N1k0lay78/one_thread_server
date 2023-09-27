from loguru import logger
from time import time

from OneThreadServer import OneThreadServer
from TicTacToeGameLogic import TicTacToeGameLogic
from config import host, port

# TODO:
# сделать человек или бот AI


class TicTacToeServer(OneThreadServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.players = []
        self.games = []
        self.time = 0

    def work(self):
        # connecting players and generate games
        self.connect_players()

        # recv
        for conn in self.players:
            self.recv(conn)
            self.ping(conn)

    # --- server work ---

    def connect_players(self):
        """
        connecting players and create games
        """
        self.players.extend(self.connect_clients())
        if time() - self.time >= 60 and len(self.players) > 1:  # one minute and 2+ players
            self.generate_games()
            self.time = time()

    def recv(self, conn, size=1024, encoding="utf-8", auto_disconnect=True, emp_msg="", err_msg=""):
        msg = super().recv(conn, size, encoding, auto_disconnect, emp_msg, err_msg)
        # action move
        if msg.startswith("move") and len(msg.split()) == 3:
            x, y = msg.split()[1:]
            game = self.get_game(conn)
            if game and x.isdigit() and y.isdigit():
                self.check_move(conn, int(x), int(y), game)

    def on_connection_lost(self, conn):
        super().on_connection_lost(conn)
        # remove players from players list
        self.players.remove(conn)
        game = self.get_game(conn)
        # close game
        if game:
            self.close_game(game)

    def get_game(self, conn):
        """
        get game from conn
        """
        for game in self.games:
            if conn in game:
                return game

    # -- game logic ---

    def check_move(self, pl, x, y, game):
        """
        checking move of player
        checking winner of the game
        """
        t = 2 if pl == game[0] else 1

        game.make_step(t, x, y)

        win = game.check_win()
        if not win:
            self.send_board(game)
        else:
            self.send(game[0], "win" if win == 2 else "lose")
            self.send(game[1], "win" if win == 1 else "lose")
            self.close_game(game)

    def generate_games(self):
        """
        generating games
        """
        self.games = []
        players = self.players[:]
        # make new games
        while len(players) >= 2:
            # creating game and send types and board to players
            self.generate_game(*players[:2])
            players = players[2:]

    def generate_game(self, pl_o, pl_x):
        """
        creating game and send types and board to players
        """
        self.games.append([pl_o, pl_x, TicTacToeGameLogic()])
        self.send_type(self.games[-1])
        self.send_board(self.games[-1])

    def send_type(self, game):
        """
        sending types to players
        """
        pl_o, pl_x, game_logic = game
        self.send(pl_o, "type 2")
        self.send(pl_x, "type 1")

    def send_board(self, game):
        """
        sending boards to players
        """
        pl_o, pl_x, game_logic = game
        self.send(pl_o, f"board {game_logic.get_board()}")
        self.send(pl_x, f"board {game_logic.get_board()}")

    def close_game(self, game):
        self.send(game[0], "end")
        self.send(game[1], "end")
        self.games.remove(game)


if __name__ == '__main__':
    TicTacToeServer(host, port).run()
