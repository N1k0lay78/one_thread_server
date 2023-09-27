from config import board_size


class TicTacToeGameLogic:
    def __init__(self):
        self.step = 1
        self.board = [[0 for x in range(board_size[0])] for y in range(board_size[1])]

    def get_step(self):
        """
        return step O or X
        """
        return self.step % 2 + 1

    def get_board(self):
        """
        return board inline string
        """
        return "".join(map(lambda x: "".join(map(str, x)), self.board))

    def make_step(self, player, x, y):
        """
        check can make step or not
        :return True or False
        """
        if player == self.get_step() and not self.board[y][x]:
            self.board[y][x] = player
            self.step += 1
            return True
        return False

    def set_board(self, board):
        """
        set board for tests
        """
        self.board = board

    def check_win(self):
        """
        0 - if no winner
        2 - if O winner
        1 - if X winner
        """
        # check horizontal
        # check vertical
        # check main diagonal
        # check additional diagonal
        if (([1, 1, 1] in self.board or
             [1, 1, 1] in [[self.board[x][y] for x in range(board_size[0])] for y in range(board_size[1])] or
             [1, 1, 1] == [self.board[0][0], self.board[1][1], self.board[2][2]] or
             [1, 1, 1] == [self.board[2][0], self.board[1][1], self.board[0][2]])):
            return 1
        elif ([2, 2, 2] in self.board or
              [2, 2, 2] in [[self.board[x][y] for x in range(board_size[0])] for y in range(board_size[1])] or
              [2, 2, 2] == [self.board[0][0], self.board[1][1], self.board[2][2]] or
              [2, 2, 2] == [self.board[2][0], self.board[1][1], self.board[0][2]]):
            return 2
        return 0


if __name__ == '__main__':
    # --- tests ---
    game_logic = TicTacToeGameLogic()

    # --- test make_step() ---
    board = [[1, 1, 1],
             [0, 2, 0],
             [0, 0, 0]]
    game_logic.set_board(board)
    assert game_logic.make_step(2, 0, 0) == False, "test 1: make step at 0 0"
    assert game_logic.make_step(2, 2, 0) == False, "test 2: make step at 2 0"
    assert game_logic.make_step(2, 1, 1) == False, "test 3: make step at 1 1"
    assert game_logic.make_step(2, 2, 1) == True,  "test 4: make step at 2 1"

    # --- test get_board() ---
    board = [[1, 1, 1],
             [0, 0, 0],
             [0, 0, 0]]
    game_logic.set_board(board)
    assert game_logic.get_board() == "111000000", "test 1: need 111000000"

    board = [[1, 1, 1],
             [0, 1, 0],
             [0, 0, 1]]
    game_logic.set_board(board)
    assert game_logic.get_board() == "111010001", "test 2: need 111010001"

    board = [[1, 1, 1],
             [2, 1, 0],
             [0, 2, 1]]
    game_logic.set_board(board)
    assert game_logic.get_board() == "111210021", "test 3: need 111210021"

    # --- test check_win() ---
    board = [[1, 1, 1],
             [0, 0, 0],
             [0, 0, 0]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 1, "test 1: row 1 win 1"

    board = [[2, 2, 2],
             [0, 0, 0],
             [0, 0, 0]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 2, "test 2: row 1 win 2"

    board = [[0, 0, 0],
             [0, 0, 0],
             [1, 1, 1],]
    game_logic.set_board(board)
    assert game_logic.check_win() == 1, "test 3: row 3 win 1"

    board = [[0, 0, 0],
             [2, 2, 2],
             [0, 0, 0]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 2, "test 4: row 2 win 2"

    board = [[1, 0, 1],
             [0, 0, 0],
             [0, 0, 0]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 0, "test 5: no row 1 win 0"

    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 0, "test 6: empty win 0"

    board = [[1, 0, 0],
             [0, 1, 0],
             [0, 0, 1]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 1, "test 7: main diagonal win 1"

    board = [[0, 0, 1],
             [0, 1, 0],
             [1, 0, 0]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 1, "test 8: additional diagonal win 1"

    board = [[0, 0, 2],
             [0, 2, 0],
             [2, 0, 0]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 2, "test 9: additional diagonal win 2"

    board = [[1, 1, 2],
             [1, 2, 1],
             [2, 1, 1]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 2, "test 10: additional diagonal win 2"

    board = [[1, 1, 2],
             [1, 2, 1],
             [0, 1, 1]]
    game_logic.set_board(board)
    assert game_logic.check_win() == 0, "test 11: fight win 0"

    print("All tests passed")
