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
        #puttable list: points are contained
        self.__puttable_list = []

    def read_board(self, file_path):
        with open(file_path) as f:
            for i, row in enumerate(f):
                col = row.split(self.parser)
                self.__board[i,] = col

    def is_puttable(self, coor, bow):

        if self.__board[coor[0], coor[1]] != 0:
            return False

        for i in range(8):
            tmp_coor = coor.copy()
            tmp_coor += self.__vec[i]
            if 
            while True:
                tmp_coor += self.__vec[i]

                if tmp_coor[0] > 7 or tmp_coor[0] < 0:
                    return False

                if tmp_coor[1] > 7 or tmp_coor[1] < 0:
                    return False

                if self.__board[tmp_coor[0], tmp_coor[1]] == 0:
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

    def put_stone(self, coor):
        pass

    def print_board(self):
        print(" ", end="")
        for i in range(self.__board_size):
            print(" {}".format(i), end="")
        print("")
        bar = "-"*18
        print(bar)
        for i in range(self.__board_size):
            print("{}|".format(i), end="")
            for j in range(self.__board_size):
                tstn = int(self.__board[i,j])
                stone = " "
                if tstn == 1:
                    stone = "B"
                elif tstn == 2:
                    stone = "W"

                print("{}|".format(stone), end="")
            print("")


    def put_stone(self, user, coor):
        pass
        #if(is_able(coor)):





if __name__ == '__main__':

    b = Board()
    b.read_board("init.csv")

