from tkinter import *
from tkinter import ttk

from board.board import Board
from board.bit_board import BitBoard
from user.user import User
from game.game import Game
from board.gui_board import GuiBoard

#import eval_test

if __name__ == '__main__':

    BOARD_INIT_FILE = 'init/init.csv'

    user1 = User(1)
    user2 = User(2)
    board = BitBoard()
    board.init_board(BOARD_INIT_FILE)
    root = Tk()
    root.title("Othello")
    root.geometry("800x800")
    gui_board = GuiBoard(board=board, master=root)
    game = Game()
    game.set_user(user1, 1)
    game.set_user(user2, 2)
    game.set_board(board)
    game.set_gui_board(gui_board)

    #evaluate = eval_test.MidEvaluator(board, 1)
    #print(evaluate.evaluate(board, 1, 1))

    # start game
    game.start_game(board)
    game.end_game()
