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

class GuiBoard(ttk.Frame):

    BK_IMG = "board/img/black1.gif"
    WH_IMG = "board/img/white1.gif"
    PT_IMG = "board/img/puttable1.gif"
    BG_IMG = "board/img/background.gif"

    def __init__(self, board, master=None, **kwargs):
        super().__init__(master)
        self._board = board
        self._put_flag = False
        self._window_size = 800
        self._grid_size = int( (self._window_size*0.8)/self._board.get_board_size() )
        self.coor_list = []

    def set_board(self, board):
        self._board = board

    def get_coor(self, x, y):
        print("{}, {}".format(x,y))
        return x, y

    def append_coor(self, coor):
        self.coor_list.append(coor)
        print(self.coor_list)

    def get_opponent(self, bow):
        """
        敵ユーザの番号を返す
        """
        return bow % 2 + 1

    def put_stone(self, x, y, bow):
        if self._board.is_puttable(x, y):
            self._board.put_stone(x, y, bow)
            opp = self.get_opponent(bow)
            self._board.listing_puttable(opp)
            self.display_board(opp)

    def display_board(self, bow):
        bsize = self._board.get_board_size()
        grid_size = self._grid_size

        tmp_board = copy.copy(self._board)

        for i in range(bsize):
            for j in range(bsize):
                img = None
                if tmp_board.get_stone(i, j, 1) == 1:
                    tmp_img = Image.open(GuiBoard.BK_IMG)
                    tmp_img = tmp_img.resize((grid_size, grid_size), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(tmp_img)
                    btn = Button(self, image=img)
                    btn.config(height = grid_size, width = grid_size)
                    btn.image = img
                    btn.grid(column=i, row=j)
                elif tmp_board.get_stone(i, j, 2) == 1:
                    tmp_img = Image.open(GuiBoard.WH_IMG)
                    tmp_img = tmp_img.resize((grid_size, grid_size), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(tmp_img)
                    btn = Button(self, image=img)
                    btn.config(height = grid_size, width = grid_size)
                    btn.image = img
                    btn.grid(column=i, row=j)
                elif tmp_board.is_puttable(i, j):
                    tmp_img = Image.open(GuiBoard.PT_IMG)
                    tmp_img = tmp_img.resize((grid_size, grid_size), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(tmp_img)
                    btn = Button(self, image=img, command=lambda row=i,col=j: self.put_stone(row, col, bow))
                    btn.config(height = grid_size, width = grid_size)
                    btn.image = img
                    btn.grid(column=i, row=j)
                else:
                    tmp_img = Image.open(GuiBoard.BG_IMG)
                    img = ImageTk.PhotoImage(tmp_img)
                    btn = Button(self, image=img)
                    btn.config(height = grid_size, width = grid_size)
                    btn.image = img
                    btn.grid(column=i, row=j)

        self.grid(column=0, row=0)


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
