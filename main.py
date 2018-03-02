from tkinter import *
from tkinter import ttk

from board import Board
from user import User
from game import Game
from gui_game import GuiBoard

if __name__ == '__main__':

    BOARD_INIT_FILE = 'init.csv'

    user1 = User(1)
    user2 = User(2)
    board = Board()
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

    # start game
    game.start_game()
    game.end_game()
