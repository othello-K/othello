import numpy as np
from board import Board

class BitBoard():

    PARSER = ','

    def __init__(self):
        #石の数
        self.__nstone = 0
        #ボードのサイズ 変更できるようにする予定
        self.__board_size = 8
        #黒ボード
        self.__bl_board = 0x0000000000000000
        #白ボード
        self.__wh_board = 0x0000000000000000
        #石を置ける場所だけフラグ
        self.__puttable_map = 0x0000000000000000
        #各ターンでボードを保存
        self.__bl_board_history = []
        self.__wh_board_history = []
        #石を置ける場所が入っている
        self.__puttable_list = []


    def get_opponent(self, bow):
        """
        敵ユーザの番号を返す
        """
        return bow % 2 + 1

    def set_stone(self, x, y, bow):
        """
        x座標とy座標の和coord_sumの位置に，bowで指定された石をおく
        """
        y *= self.__board_size

        if bow == 1:
            self.__bl_board = self.__bl_board & (1 << (x + 8*y))
        elif bow == 2:
            self.__wh_board = self.__wh_board & (1 << (x + 8*y))

    def get_stone(self, x, y, bow):
        """
        指定されたbowの盤面のcoord_sumの状態を判定
        """
        if bow == 1:
            return (self.__bl_board >> (x + 8*y)) & 0b1
        elif bow == 2:
            return (self.__wh_board >> (x + 8*y)) & 0b1

    def get_board_size(self):
        """
        ボードのサイズをゲット
        """
        return self.__board_size

    def set_board(self, board, bow):
        if bow == 1:
            self.__bl_board = board
        elif bow == 2:
            self.__wh_board = board

    def append_board_history(self, board, bow):
        if bow == 1:
            self.__bl_board_history.append(board)
        elif bow == 2:
            self.__wh_board_history.append(board)



    def init_board(self, file_path):
        """
        csvファイルを元に，ボードを初期化
        """
        with open(file_path) as f:
            for i, row in enumerate(f):
                col = row.split(self.PARSER)
                for j, stone in enumerate(col):
                    if stone == '1':
                        self.__bl_board |= (1<< (i+8*j))
                    elif stone == '2':
                        self.__wh_board |= (1<< (i+8*j))


    def init_board_from_board(self, board):
        """
        Boardオブジェクトを元に盤面を初期化
        """
        board_size = board.get_board_size()
        for i in range(board_size):
            for j in range(board_size):
                stone = board.get_stone(np.array([i,j]))
                if stone == 1:
                    self.__bl_board = self.__bl_board | (1<<(i+j*8))
                elif stone == 2:
                    self.__wh_board = self.__bl_board | (1<<(i+j*8))


    def get_board_half(self, bow):
        if bow == 1:
            return self.__bl_board
        elif bow == 2:
            return self.__wh_board


    def display_board(self):
        """
        boardを表示
        """

        tmp_bl_board = self.get_board_half(1)
        tmp_wh_board = self.get_board_half(2)

        for puttable in self.__puttable_list:
            tmp_board[puttable[0], puttable[1]] = -1

        print(" ", end="")
        for i in range(self.__board_size):
            print(" {}".format(i), end="")
        print("")
        bar = "-"*18
        print(bar)
        for i in range(self.__board_size):
            print("{}|".format(i), end="")
            for j in range(self.__board_size):
                coord = i + j*8
                stone = " "
                if tmp_bl_board >> coord & 1 == 1:
                    stone = "B"
                elif tmp_wh_board >> coord & 1 == 1:
                    stone = "W"
                elif coord == -1:
                    stone = "*"

                print("{}|".format(stone), end="")
            print("")


    def listing_puttable(self, bow):
        """
        石を置ける場所のリストを作成
        """
        atk_board = self.get_board_half(bow)
        opp = self.get_opponent(bow)
        opp_board = self.get_board_half(opp)

        #左右端の番人
        horizontal_watch_board = opp_board & 0x7e7e7e7e7e7e7e7e
        #上下端の番人
        vertical_watch_board = opp_board & 0x00FFFFFFFFFFFF00
        #全端の番人
        all_side_watch_board = opp_board & 0x007e7e7e7e7e7e00
        #空きマスにフラグがたったボード
        blank_board = ~(atk_board | opp_board)

        #8方向チェック (・一度に返せる石は最大6つ ・高速化のためにforを展開)
        #左方向
        tmp = horizontal_watch_board & (atk_board << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        tmp |= horizontal_watch_board & (tmp << 1)
        legal_board = blank_board & (tmp << 1)

        #右方向
        tmp = horizontal_watch_board & (atk_board >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        tmp |= horizontal_watch_board & (tmp >> 1)
        legal_board |= blank_board & (tmp >> 1)

        #上
        tmp = vertical_watch_board & (atk_board << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        tmp |= vertical_watch_board & (tmp << 8)
        legal_board |= blank_board & (tmp << 8)

        #下
        tmp = vertical_watch_board & (atk_board >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        tmp |= vertical_watch_board & (tmp >> 8)
        legal_board |= blank_board & (tmp >> 8)

        #右斜め上
        tmp = all_side_watch_board & (atk_board << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        tmp |= all_side_watch_board & (tmp << 7)
        legal_board |= blank_board & (tmp << 7)

        #左斜め上
        tmp = all_side_watch_board & (atk_board << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        tmp |= all_side_watch_board & (tmp << 9)
        legal_board |= blank_board & (tmp << 9)

        #右斜め下
        tmp = all_side_watch_board & (atk_board >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        tmp |= all_side_watch_board & (tmp >> 9)
        legal_board |= blank_board & (tmp >> 9)

        #左斜め下
        tmp = all_side_watch_board & (atk_board >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        tmp |= all_side_watch_board & (tmp >> 7)
        legal_board |= blank_board & (tmp >> 7)

        self.__puttable_map = legal_board


    def is_puttable(self, x, y):
       if self.__puttable_map >> (x + 8*y) & 0b1 == 1:
           return True
       else:
           return False


    def get_puttable_list(self):
        """
        石を置ける場所のリストをゲット
        """
        self.__puttable_list = []
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                if self.is_puttable(i, j):
                    self.__puttable_list.append(np.array([i,j]))

        return self.__puttable_list


    def transfer(self, put, way):
        if way == 0: #上
            return (put << 8) & 0xffffffffffffff00
        elif way == 1: #右上
            return (put << 7) & 0x7f7f7f7f7f7f7f00
        elif way == 2: #右
            return (put >> 1) & 0x7f7f7f7f7f7f7f7f
        elif way == 3: #右下
            return (put >> 9) & 0x007f7f7f7f7f7f7f
        elif way == 4: #下
            return (put >> 8) & 0x00ffffffffffffff
        elif way == 5: #左下
            return (put >> 7) & 0x00fefefefefefefe
        elif way == 6: #左
            return (put << 1) & 0xfefefefefefefefe
        elif way == 7: #左上
            return (put << 9) & 0xfefefefefefefe00
        else:
            return 0


    def is_in_puttable_list(self, x, y):
        if self.__puttable_map >> (x + 8*y) & 0b1 != 0:
            return True
        else:
            return False


    def is_no_puttable(self):
        if self.__puttable_map == 0:
            return True
        else:
            return False


    def count_stone(self, bow):
        if bow == 1:
            print(hex(self.__bl_board))
            nbit = (self.__bl_board & 0x5555555555555555) + (( self.__bl_board >> 1 ) & 0x5555555555555555)
            nbit = (nbit & 0x3333333333333333) + (( nbit >> 2 ) & 0x3333333333333333)
            nbit = (nbit & 0x0f0f0f0f0f0f0f0f) + (( nbit >> 4 ) & 0x0f0f0f0f0f0f0f0f)
            nbit = (nbit & 0x00ff00ff00ff00ff) + (( nbit >> 8 ) & 0x00ff00ff00ff00ff)
            nbit = (nbit & 0x0000ffff0000ffff) + (nbit >> 16 & 0x0000ffff0000ffff)
            return (nbit & 0x00000000ffffffff) + (nbit >> 32)
        elif bow == 2:
            nbit = (self.__wh_board & 0x5555555555555555) + (( self.__wh_board >> 1 ) & 0x5555555555555555)
            nbit = (nbit & 0x3333333333333333) + (( nbit >> 2 ) & 0x3333333333333333)
            nbit = (nbit & 0x0f0f0f0f0f0f0f0f) + (( nbit >> 4 ) & 0x0f0f0f0f0f0f0f0f)
            nbit = (nbit & 0x00ff00ff00ff00ff) + (( nbit >> 8 ) & 0x00ff00ff00ff00ff)
            nbit = (nbit & 0x0000ffff0000ffff) + (nbit >> 16 & 0x0000ffff0000ffff)
            return (nbit & 0x00000000ffffffff) + (nbit >> 32)


    def put_stone(self, x, y, bow):
        #着手した場合のボードを生成
        atk_board = self.get_board_half(bow)
        opp_board = self.get_board_half(self.get_opponent(bow))
        print(type(int(x)))
        print(x)

        rev = 0
        put = 0b1 << ( x + 8*y )
        for way in range(self.__board_size):
            tmp_rev = 0
            mask = self.transfer(put, way)

            while (mask != 0) and ((mask & opp_board) != 0):
                tmp_rev |= mask
                mask = self.transfer(mask, way)

            if (mask & atk_board) != 0 :
                rev |= tmp_rev

        #反転する
        atk_board ^= put | rev
        opp_board ^= rev
        self.set_board(atk_board, bow)
        self.set_board(opp_board, self.get_opponent(bow))


