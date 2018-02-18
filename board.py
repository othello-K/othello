import numpy as np
from user import User

class Board():

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
        self.__nstone = 0
        self.__board_size = 8
        self.__board = np.zeros((self.__board_size, self.__board_size))
        self.__board_history = []
        #puttable list: points are contained
        self.__puttable_list = []

    def get_opponent(self, bow):
        return bow % 2 + 1

    def set_stone(self, coor, bow):
        if coor[0] < 8 and coor[0] >= 0 and coor[1] < 8 and coor[1] >= 0:
            self.__board[coor[0], coor[1]] = bow
        else:
            print("out of board size")

    def get_stone(self, coor):
        if coor[0] < 8 and coor[0] >=0 and coor[1] < 8 and coor[1] >= 0:
            return self.__board[coor[0], coor[1]]
        else:
            return -1

    def read_board(self, file_path):
        with open(file_path) as f:
            for i, row in enumerate(f):
                col = row.split(self.parser)
                self.__board[i,] = col

    def is_puttable(self, coor, bow):

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
        self.__puttable_list = []
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                coor = np.array([i, j])
                if self.is_puttable(coor, bow):
                    self.__puttable_list.append(coor)

    def get_puttable_list(self):
        return self.__puttable_list

    def is_in_puttable_list(self, coor):
        for puttable in self.__puttable_list:
            if (coor==puttable).all():
                return True

        return False

    def put_stone(self, coor, bow):
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


    def print_board(self):
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
    b.read_board("init.csv")

