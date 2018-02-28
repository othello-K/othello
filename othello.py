#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
from tkinter import *
from tkinter import ttk

import numpy as np

from board import Board

class GuiBoard(ttk.Frame):

    def __init__(self, board, master=None, **kwargs):
        super().__init__(master)
        self.__board = board
        self.__window_size = 800

    def init_board(self):
        bsize = self.__board.get_board_size()
        grid_size = (self.__window_size*0.8)/bsize
        for i in range(bsize):
            for j in range(bsize):
                coor = np.array([i,j])
                if self.__board.get_stone(coor) == 1:
                    print("aaa")
                    img = PhotoImage(file="black1.gif")
                    img = img.resize((grid_size, grid_size), Image.ANTIALIAS)
                    btn = Button(self, text="{},{}".format(i,j), image=img)
                    btn.config(height = grid_size, width = grid_size)
                    btn.image = img
                    btn.grid(column=i, row=j)
                elif self.__board.get_stone(coor) == 2:
                    img = PhotoImage(file="white1.gif")
                    btn = Button(self, image=img)
                    btn.config(height = grid_size, width = grid_size)
                    btn.image = img
                    btn.grid(column=i, row=j)
                else:
                    img = PhotoImage(file="background.gif")
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
    g.init_board()
    root.mainloop()


if __name__ == '__main__':
    main()
