import copy
import math

import cython
import numpy as np
cimport numpy as np

from ai import eval_test
from ai import book_manager
from board.bit_board import BitBoard

cdef class Search():

    cdef public int _turn, _own, _opponent, _depth
    cdef public object _board, _eval, _bmanager
    cdef int [:] _index

    def __init__(self, board, int own, int opponent, int turn):
        self._turn = turn
        self._own = own
        self._opponent = opponent
        self._index = None
        self._board = board
        self._depth = 6
        if(turn >= 0 and turn <= 50):
            self._eval = eval_test.MidEvaluator(board)
        else:
            self._eval = eval_test.WLDEvaluator()
        self._bmanager = book_manager.BookManager(own)

    def search(self):
        cdef int tmp
        tmp = self.alpha_beta(self._board, self._own, -999999999, 999999999, self._depth)
        return tmp, self._index[0], self._index[1]

    #alpha beta algorithm
    def alpha_beta(self, object board, int atk, int alpha, int beta, int depth):
        cdef int i, score
        cdef int [:] coord
        cdef object tmp_board
        cdef list legals
        if depth == 0:
            return  self._eval.evaluate(board, atk)

        if(atk == self._own):
            board.listing_puttable(atk)
            legals = board.get_puttable_list()
            if len(legals) != 0:
                #legals = self._bmanager.find(board)
                for i in range( len(legals) ):
                    coord = legals[i]
                    tmp_board = copy.deepcopy(board)
                    tmp_board.put_stone(int(coord[0]), int(coord[1]), atk)
                    score = self.alpha_beta(tmp_board, self._opponent, alpha, beta, depth-1)
                    if score > alpha:
                        alpha = score
                        if depth==self._depth:
                            self._index = coord
                    #beta cut
                    if alpha >= beta:
                        break
                return alpha
            else:
                tmp_board = copy.deepcopy(board)
                return max([alpha, self.alpha_beta(tmp_board, self._opponent, alpha, beta, depth-1)])
        else:
            board.listing_puttable(atk)
            legals = board.get_puttable_list()
            if len(legals) != 0:
                #legals = self._bmanager.find(board)
                for i in range( len(legals) ):
                    coord = legals[i]
                    tmp_board = copy.deepcopy(board)
                    tmp_board.put_stone(int(coord[0]), int(coord[1]), self._opponent)
                    score = self.alpha_beta(tmp_board, self._own, alpha, beta, depth-1)
                    if score < beta:
                        beta = score
                    if alpha >= beta:
                        break
                return beta
            else:
                tmp_board = copy.deepcopy(board)
                return min([beta, self.alpha_beta(tmp_board, self._own, alpha, beta, depth-1)])

