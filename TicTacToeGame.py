import pygame as pg

from TicTacToeClient import TicTacToeClient
from config import board_size, source_image_path, tile_size, host_port


def load_tile(tile_set_name, x, y, tile_size):
    if tile_set_name.endswith(".png"):
        image = pg.image.load(source_image_path + tile_set_name)
    else:
        image = pg.image.load(source_image_path + tile_set_name + ".png")
    return image.subsurface((x * tile_size[0], y * tile_size[1], tile_size[0], tile_size[1]))


class TicTacToeGame:
    def __init__(self, board_size, tile_size):
        pg.init()

        # --- load tiles ---
        self.tile_set = []
        self.tile_size = tile_size
        for y in range(2):
            for x in range(2):
                self.tile_set.append(load_tile("TicTacToe", x, y, self.tile_size))

        # --- create game window ---
        self.board_size = board_size
        self.screen = pg.display.set_mode((self.tile_size[0] * self.board_size[0],
                                           self.tile_size[1] * self.board_size[1]))
        pg.display.set_icon(self.tile_set[3])
        pg.display.set_caption("Tic Tac Toe")
        self.clock = pg.time.Clock()
        self.FPS = 60

        # --- connect to server ---
        self.client = TicTacToeClient(host_port)

        # --- game board ---
        # TODO:
        # server chose ur type
        self.game_board = [[0 for x in range(self.board_size[0])] for y in range(self.board_size[1])]
        self.type = 2  # 1 if input("chose X or O: ").lower() == "x" else 2
        self.step_type = 2
        self.mouse_press_cell = (-1, -1)

        # --- start game ---
        self.running = True
        self.run()

    def run(self):
        while self.running:
            # --- events ---
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                # --- choose cell ---
                if event.type == pg.MOUSEBUTTONDOWN:
                    """
                    event.button
                    1 - left click
                    2 - middle click
                    3 - right click
                    4 - scroll up
                    5 - scroll down
                    """
                    if event.button == 1:
                        self.mouse_press_cell = (event.pos[0] // self.tile_size[0],
                                                 self.board_size[1] - event.pos[1] // self.tile_size[1] - 1)
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        cell = (event.pos[0] // self.tile_size[0],
                                self.board_size[1] - event.pos[1] // self.tile_size[1] - 1)
                        if cell == self.mouse_press_cell:
                            self.game_board[cell[1]][cell[0]] = self.type
                        self.mouse_press_cell = (-1, -1)

            # --- draw background ---
            for y in range(self.board_size[1] - 1, -1, -1):  # from top to bottom
                for x in range(self.board_size[0]):
                    self.draw(self.tile_set[0], x, y)

            # --- draw board ---
            for y in range(self.board_size[1] - 1, -1, -1):  # from top to bottom
                for x in range(self.board_size[0]):
                    if self.game_board[y][x]:
                        self.draw(self.tile_set[self.game_board[y][x]], x, y)

            # --- update screen and control fps ---
            pg.display.update()
            self.clock.tick(self.FPS)

    def draw(self, surface, x, y):
        self.screen.blit(surface, (self.tile_size[0] * x,
                                   self.tile_size[1] * (self.board_size[1] - y - 1)))


if __name__ == '__main__':
    TicTacToeGame(board_size, tile_size)
