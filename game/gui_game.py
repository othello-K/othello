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
        self._window_size = 800
        self._grid_size = int( (self._window_size*0.8)/8 )
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


    def put_stone(self, x, y, bow):
        self._board.put_stone(x, y, bow)
        opp = self.get_opponent(bow)
        self._board.listing_puttable(opp)
        self.display_board(opp)


    def game_process(self, x, y, bow):
        self._board.put_stone(x, y, bow)
        opp = self.get_opponent(bow)
        self._board.listing_puttable(opp)
        if self._board.is_no_puttable():
            self._board.listing_puttable(bow)
            if self._board.is_no_puttable():
                print('game finished')
                self.end_game()
            else:
                print('nowhere to put stone')
                self.next_turn()
                self.display_board(bow)
        else:
            flag = False
            self.input_coord(opp)


    def display_board(self, bow):
        bsize = self._board.get_board_size()
        grid_size = self._grid_size

        tmp_board = copy.copy(self._board)

        for i in range(bsize):
            for j in range(bsize):
                img = None
                if tmp_board.get_stone(i, j, 1) == 1:
                    img = self._bk_img
                    btn = Button(self, image=self._bk_img)
                elif tmp_board.get_stone(i, j, 2) == 1:
                    btn = Button(self, image=self._wh_img)
                    img = self._wh_img
                elif tmp_board.is_puttable(i, j):
                    img = self._pt_img
                    btn = Button(self, image=self._pt_img, command=lambda row=i,col=j: self.game_process(row, col, bow))
                else:
                    img = self._bg_img
                    btn = Button(self, image=img)

                btn.config(height = grid_size, width = grid_size)
                btn.image = img
                btn.grid(column=i, row=j)
        self.grid(column=0, row=0)

    def start_game(self, root):
        """
        ゲームの流れが書いてあるメソッド
        """
        self._board.listing_puttable(self._attacker)
        #ボードを表示
        self.display_board(self._attacker)
        root.mainloop()

        print("player {}'s attack".format(self._attacker))

    def end_game(self):
        """
        ゲーム終了時の処理．勝敗と石の数を表示．
        """

        if nstone1 > nstone2:
            print("Black Win!")
        elif nstone1 < nstone2:
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
    g.display_board()
    root.mainloop()


if __name__ == '__main__':
    main()
