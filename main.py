from board import Board
from user import User
from game import Game

if __name__ == '__main__':

    BOARD_INIT_FILE = 'init.csv'

    user1 = User(1)
    user2 = User(2)
    board = Board()
    board.init_board(BOARD_INIT_FILE)
    game = Game()
    game.set_user(user1, 1)
    game.set_user(user2, 2)
    game.set_board(board)
    # start game
    game.start_game()
    game.end_game()
