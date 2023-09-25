from loguru import logger

from OneThreadServer import OneThreadServer
from config import host, port, board_size

# TODO:
# сделать проверку на победу
# сделать класс игрока (человек или бот AI)
# продумать архитектуру


class Game:
    def __init__(self):
        self.player_o = None
        self.player_x = None
        self.board = [[0 for x in range(board_size[0])] for y in range(board_size[1])]


class TicTacToeServer(OneThreadServer):
    def __init__(self, host, port):
        super().__init__(host, port)
        # game - two client
        self.games = []

    def work(self):
        self.connect_players()

    def connect_players(self):
        players = self.connect_clients()
        # fill last game
        if self.games and len(self.games[-1]) == 1:
            self.games[-1].append(players[0])
            players = players[1:]
        # make new games
        while players:
            if len(players) >= 2:
                self.games.append([players[:2]])
                players = players[2:]
            else:
                self.games.append(players)


if __name__ == '__main__':
    TicTacToeServer(host, port).run()