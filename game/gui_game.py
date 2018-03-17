#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from tkinter import *
from tkinter import ttk

import copy

from PIL import Image
from PIL import ImageTk

import numpy as np

from board.board import Board
from game.base_game import BaseGame

class GuiGame(BaseGame, ttk.Frame):

    BK_IMG = "game/img/black1.gif"
    WH_IMG = "game/img/white1.gif"
    PT_IMG = "game/img/puttable1.gif"
    BG_IMG = "game/img/background.gif"

    def __init__(self, master=None, **kwargs):
        super(GuiGame, self).__init__()
        super(BaseGame, self).__init__(master)
        board = kwargs['board']
        if board is not None:
            self._board = board
            board_size = board.get_board_size()
        self._window_size = 800
        self._grid_size = int( (self._window_size*0.8)/board_size )
        self._button_map = []
        #button image settings
        tmp_img = Image.open(GuiGame.BK_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._bk_img = ImageTk.PhotoImage(tmp_img)
        tmp_img = Image.open(GuiGame.WH_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._wh_img = ImageTk.PhotoImage(tmp_img)
        tmp_img = Image.open(GuiGame.PT_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._pt_img = ImageTk.PhotoImage(tmp_img)
        tmp_img = Image.open(GuiGame.BG_IMG)
        tmp_img = tmp_img.resize((self._grid_size, self._grid_size), Image.ANTIALIAS)
        self._bg_img = ImageTk.PhotoImage(tmp_img)

    def print_state(self, x, y, bow):
        if bow == 1:
            color = 'black'
        elif bow ==2:
            color = 'white'

        print(color + ' player put stone on ' + '{}, {}'.format(x, y))
        self._board.display_board()

    def game_process(self, event, x, y, bow):
        print(self._board.is_puttable(x, y))
        self.append_history(np.array([x, y]), bow)
        self._board.put_stone(x, y, bow)
        self.set_nstone()
        opp = self.get_opponent(bow)
        self._board.listing_puttable(opp)
        self.print_state(x, y, bow)
        if self._board.is_no_puttable():
            self._board.listing_puttable(bow)
            if self._board.is_no_puttable():
                print('game finished')
                self.display_gui_board(opp)
                self.end_game()
            else:
                print('nowhere to put stone')
                print(str(opp) + ' pass')
                self.next_turn()
                self.display_gui_board(bow)
        else:
            self.input_coord(opp)

    def undo_process(self):
        input_list = self._input_history
        if len(input_list) != 0:
            self._board.undo_board()
            self._input_history.pop()
            bow = self._input_user_history.pop()
            if bow == 1:
                self._user1.pop_history()
            elif bow == 2:
                self._user2.pop_history()
            self._turn -= 1
            #when undo the first putting, error occur
            if len(self._input_user_history) != 0:
                self._attacker = self._input_user_history[-1]
            else:
                self._attacker = 1
            self.set_nstone()
            self._board.listing_puttable(self._attacker)
            self.display_gui_board(self._attacker)


    def init_gui_board(self):
        bsize = self._board.get_board_size()
        self._button_map = [[ Button() for i in range(bsize)] for j in range(bsize)]
        for x, btns in enumerate(self._button_map):
            for y, btn in enumerate(btns):
                btn.configure(height = self._grid_size, width = self._grid_size)
                btn.grid(column=x, row=y)

        self.grid(column=0, row=0)
        undo_button  = Button(text = 'UNDO', command=lambda: self.undo_process())
        undo_button.grid(column=bsize, row=3)

    def display_gui_board(self, bow):
        bsize = self._board.get_board_size()
        grid_size = self._grid_size

        tmp_board = self._board

        for i in range(bsize):
            for j in range(bsize):
                img = self._bg_img
                command = None
                if tmp_board.get_stone(i, j, 1) == 1:
                    img = self._bk_img
                elif tmp_board.get_stone(i, j, 2) == 1:
                    img = self._wh_img
                elif tmp_board.is_puttable(i, j):
                    img = self._pt_img
                    command = lambda event, row=i, col=j: self.game_process(event, row, col, bow)

                print(command)
                self._button_map[i][j].configure(image=img)
                self._button_map[i][j].bind("<Button-1>", command)

    def start_game(self, root):
        """
        ゲームの流れが書いてあるメソッド
        """
        self._board.listing_puttable(self._attacker)
        #ボードを表示
        self.init_gui_board()
        self.display_gui_board(self._attacker)
        root.mainloop()

        print("player {}'s attack".format(self._attacker))

    def end_game(self):
        """
        ゲーム終了時の処理．勝敗と石の数を表示．
        """

        if self._user1.get_nstone() > self._user2.get_nstone():
            print("Black Win!")
        elif self._user1.get_nstone() < self._user2.get_nstone():
            print("White Win!")
        else:
            print("DRAW!")

def main():
    root = Tk()
    root.title("Othello")
    root.geometry("800x800")
    b = Board()
    b.init_board('init.csv')
    g = GuiBoard(board=b, master=root)
    g.display_gui_board()
    hlsearch

    root.mainloop()


if __name__ == '__main__':
    main()
