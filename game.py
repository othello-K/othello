from board import Board
from user import User
import numpy as np

class Game():
    """
    in this class, game process is written
    """


    def __init__(self):
        #preceding user
        self.__user1 = User()
        #after atack user
        self.__user2 = User()
        #board
        self.__board = Board()
        #turn
        self.__turn = 0
        #input coor
        input_coor = np.zeros(2)
        #puttable list: points are contained
        puttable_list = []

    def start_game(self):
        while True:
            self.__board.print_board()
            input_coor()


    def input_coor(self):
        while True:

            print('input coordinate x')
            coorx = input('coor x:')
            if not( int(coorx) in [0,1,2] ):
                continue

            print('input coordinate x')
            coory = input('coor y:')
            if not( int(coory) in [0,1,2] ):
                continue

            self.input_coor = np.array([coorx, coory])
            if selfl.__board.is_puttable(coor):
                break
            else:
                print("unable to put stone there")
                continue
