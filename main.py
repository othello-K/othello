from tkinter import *
from tkinter import ttk

from board.board import Board
from board.bit_board import BitBoard
from user.user import User
from user.ai_user import AiUser
from game.gui_game import GuiGame

#import eval_test

if __name__ == '__main__':

    BOARD_INIT_FILE = 'init/init.csv'

    user1 = User(1)
    user2 = AiUser(2)
    board = BitBoard()
    board.init_board(BOARD_INIT_FILE)
    root = Tk()
    root.title("Othello")
    root.geometry("900x900")
    game = GuiGame(board=board, master=root)
    game.set_user(user1, 1)
    game.set_user(user2, 2)
    game.set_board(board)

    # start game
    game.start_game(root)
    root.mainloop()
    game.end_game()
