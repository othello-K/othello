import numpy as np

class Board():

    #置けるか判定をするときに使うベクトル
    __vec = np.array([\
            [1,0],
            [1,-1],
            [1,1],
            [-1,0],
            [-1,1],
            [-1,-1],
            [0,1],
            [0,-1]
        ])

    parser = ","

    def __init__(self):
        #石の数
        self.__nstone = 0
        #ボードのサイズ 変更できるようにする予定
        self.__board_size = 8
        #石をおくボードを表す二次元numpy array
        self.__board = np.zeros((self.__board_size, self.__board_size))
        #各ターンでのボードの形を保存する
        self.__board_history = []
        #puttable list: points are contained
        #石を置ける場所が入っている
        self.__puttable_list = []

    def get_opponent(self, bow):
        """
        敵ユーザの番号を返す
        """
        return bow % 2 + 1

    def set_stone(self, coor, bow):
        """
        指定されたcoordinateにbowの石を置く
        """
        if coor[0] < 8 and coor[0] >= 0 and coor[1] < 8 and coor[1] >= 0:
            self.__board[coor[0], coor[1]] = bow
        else:
            print("out of board size")

    def get_stone(self, coor):
        """
        指定されたcoordinateの石をみる
        """
        if coor[0] < 8 and coor[0] >=0 and coor[1] < 8 and coor[1] >= 0:
            return self.__board[coor[0], coor[1]]
        else:
            return -1

    def get_board_size(self):
        """
        ボードのサイズをゲット
        """
        return self.__board_size

    def init_board(self, file_path):
        """
        csvファイルを元に，ボードを初期化
        """
        with open(file_path) as f:
            for i, row in enumerate(f):
                col = row.split(self.parser)
                self.__board[i,] = col

    def is_puttable(self, coor, bow):
        """
        coordinateにbowの石を置けるか判定
        """

        if self.get_stone(coor) != 0:
            return False

        opp = self.get_opponent(bow)

        for i in range(8):
            tmp_coor = coor.copy()
            tmp_coor += self.__vec[i]

            if self.get_stone(tmp_coor) in [0,-1,bow]:
                continue

            while True:
                tmp_coor += self.__vec[i]

                if tmp_coor[0] > 7 or tmp_coor[0] < 0:
                    break

                if tmp_coor[1] > 7 or tmp_coor[1] < 0:
                    break

                if self.get_stone(tmp_coor) == 0:
                    break

                if self.get_stone(tmp_coor) == bow:
                    return True

        return False


    def listing_puttable(self, bow):
        """
        石を置ける場所を全てリストに入れる
        """
        self.__puttable_list = []
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                coor = np.array([i, j])
                if self.is_puttable(coor, bow):
                    self.__puttable_list.append(coor)

    def get_puttable_list(self):
        """
        石を置ける場所のリストをゲット
        """
        return self.__puttable_list

    def is_in_puttable_list(self, coor):
        """
        石を置けるか判定．こっちの方が速い．
        """
        for puttable in self.__puttable_list:
            if (coor==puttable).all():
                return True

        return False

    def put_stone(self, coor, bow):
        """
        石を置く．
        """
        opp = self.get_opponent(bow)
        self.__board_history.append(self.__board.copy())
        self.set_stone(coor, bow)

        for i in range(8):
            tmp_coor = coor.copy()
            tmp_coor += self.__vec[i]

            if self.get_stone(tmp_coor) in [0,-1,bow]:
                continue

            while True:
                tmp_coor += self.__vec[i]

                if tmp_coor[0] > 7 or tmp_coor[0] < 0:
                    break

                if tmp_coor[1] > 7 or tmp_coor[1] < 0:
                    break

                if self.get_stone(tmp_coor) == bow:
                    while True:
                        tmp_coor -= self.__vec[i]
                        if self.get_stone(tmp_coor) == bow:
                            break
                        self.set_stone(tmp_coor, bow)
                    break

    def count_stone(self, bow):
        """
        bowの石の数を数える
        """
        return np.count_nonzero(bow - self.__board)



    def display__board(self):
        """
        boardを表示
        """
        tmp_board = self.__board.copy()
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
                tstn = int(tmp_board[i,j])
                stone = " "
                if tstn == 1:
                    stone = "B"
                elif tstn == 2:
                    stone = "W"
                elif tstn == -1:
                    stone = "*"

                print("{}|".format(stone), end="")
            print("")




if __name__ == '__main__':
    b = Board()
    b.init_board("init.csv")

