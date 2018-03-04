import numpy as np
from board import Board

class BitBoard():

    def __init__(self):
        #石の数
        self.__nstone = 0
        #ボードのサイズ 変更できるようにする予定
        self.__board_size = 8
        #黒ボード
       self.__bl_board = 0x0000000000000000
        #白ボード
       self.__wh_board = 0x0000000000000000
        #石を置ける場所が入っている
        self.__puttable_list = []


    def get_opponent(self, bow):
        """
        敵ユーザの番号を返す
        """
        return bow % 2 + 1

    def set_stone(self, coord_sum, bow):
        """
        x座標とy座標の和coord_sumの位置に，bowで指定された石をおく
        """
        if bow == 1:
            self.__bl_board = self.__bl_board & (1 << coord_sum)
        elif bow == 2:
            self.__wh_board = self.__wh_board & (1 << coord_sum)

    def get_stone(self, coord_sum, bow):
        """
        指定されたbowの盤面のcoord_sumの状態を判定
        """
        if bow == 1:
            return (self.__bl_board >> coord_sum) & 0b1
        elif bow == 2:
            return (self.__wh_board >> coord_sum) & 0b1

    def get_board_size(self):
        """
        ボードのサイズをゲット
        """
        return self.__board_size

    def init_board(self, board):
        """
        Boardオブジェクトを元に盤面を初期化
        """
        board_size = board.get_board_size()
        for i in range(board_size):
            for j in range(board_size):
                stone = board.get_stone(np.array([i,j]))
                if stone == 1:
                    self.__bl_board = self.__bl_board | (1<<(i+j))
                elif stone == 2:
                    self.__bl_board = self.__bl_board | (1<<(i+j))

    def is_puttable(self, coord_sum, bow):
        """
        coorddinateにbowの石を置けるか判定
        """
        pass

