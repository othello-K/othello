from board import Board
from user import User
import numpy as np

class Game():
    """
    in this class, game process is written
    """

    def __init__(self):
        #preceding attack user
        self.__user1 = None
        #after attack user
        self.__user2 = None
        #board
        self.__board = None
        #turn
        self.__turn = 0
        #input coor
        self.__input_list = []
        #now attacker
        self.__attacker = 1
        #game keeper flag
        self.__flag = False

    def set_user(self, user, user_id):
        if user_id == 1:
            self.__user1 = user
        elif user_id == 2:
            self.__user2 = user
        else:
            print("only user1 or user2 can be assigned")

    def append_input(self, coor, bow):
        if bow == 1:
            self.__user1.append_input(coor)
        if bow == 2:
            self.__user2.append_input(coor)

    def set_board(self, board):
        self.__board = board
        print(self.__board)

    def set_nstone(self, nstone, bow):
        if bow == 1:
            self.__user1.set_nstone(nstone)
        elif bow == 2:
            self.__user2.set_nstone(nstone)

    def print_nstone(self):
        nstone1 = self.__user1.get_nstone()
        nstone2 = self.__user1.get_nstone()
        print("Black: {}\nWhite: {}".format(nstone1, nstone2))

    def input_coor(self):
        while True:

            print('input coordinate x')
            coorx = input('coor x:')

            print('input coordinate x')
            coory = input('coor y:')

            coor = np.array([int(coorx), int(coory)])
            print(coor)

            # refactoring required: not to get puttable list
            if self.__board.is_in_puttable_list(coor) :
                self.__input_list.append( coor )
                break
            else:
                print("unable to put stone there")
                continue

    def put_stone(self, coor, bow):
        self.__board.put_stone(self.__input_list[-1], bow)

    def start_game(self):
        while True:
            self.__board.listing_puttable(self.__attacker)
            self.__board.display_board()
            print("player {}'s attack".format(self.__attacker))

            if len(self.__board.get_puttable_list()) == 0:
                if flag:
                    print("game finished!")
                    break;
                else:
                    flag = True
                    print("nowhere to put stone")
                    self.__turn += 1
                    self.__attacker = self.__turn % 2 + 1
                    continue
            else:
                flag = False

            self.input_coor()

            self.put_stone(self.__input_list[-1], self.__attacker)

            #self.append_input(coor, bow)
            self.set_nstone(self.__board.count_stone(self.__attacker), self.__attacker)

            self.__turn += 1
            self.__attacker = self.__turn % 2 + 1

    def end_game(self):

        if nstone1 > nstone2:
            print("Black Win!")
        elif nstone1 < nstone2:
            print("White Win!")
        else:
            print("DRAW!")
