from board import Board
from user import User
import numpy as np

class Game():
    """
    in this class, game process is written
    """


    def __init__(self):
        #preceding user
        self.__user1 = None
        #after atack user
        self.__user2 = None
        #board
        self.__board = None
        #turn
        self.__turn = 0
        #input coor
        self.input_list = []
        #now attacker
        self.attacker = 1

    def set_user(self, user, user_id):
        if user_id == 1:
            self.__user1 = user
        elif user_id == 2:
            self.__user2 = user
        else:
            print("only user1 or user2 can be assigned")

    def set_board(self, board):
        self.__board = board
        print(self.__board)

    def input_coor(self):
        while True:

            ptlist = self.__board.get_puttable_list()
            print(ptlist)

            print('input coordinate x')
            coorx = input('coor x:')

            print('input coordinate x')
            coory = input('coor y:')

            coor = np.array([coorx, coory])

            # refactoring required: not to get puttable list
            if coor in ptlist :
                self.input_coor.append( np.array([coorx, coory]) )
                break
            else:
                print("unable to put stone there")
                continue

    def put_stone(self):
        print(self.__board)
        self.__board.put_stone()

    def start_game(self):
        while True:
            self.__board.print_board()
            self.__board.listing_puttable()
            self.input_coor()
            self.put_stone()
