from tkinter import *
from tkinter import ttk

from board.board import Board
from board.bit_board import BitBoard
from user.user import User
from game.game import Game
from board.gui_board import GuiBoard

import eval_test

if __name__ == '__main__':

    BOARD_INIT_FILE = 'init/init.csv'

    user1 = User(1)
    user2 = User(2)
    board = BitBoard()
    board.init_board(BOARD_INIT_FILE)

    game = Game()
    game.set_user(user1, 1)
    game.set_user(user2, 2)
    game.set_board(board)

    evaluate = eval_test.MidEvaluator(board, 1)
    print('eval : ' + str(evaluate.evaluate(board, 1, 1)))

    # start game
    turn = 1
    attacker = 1
    while True:
        board.display_board()
        print("x")
        x = input()
        print("y")
        y = input()
        board.set_stone(int(x), int(y), attacker)
        game.set_nstone(board.count_stone(attacker), attacker)
        attacker = turn % 2 + 1