import copy
from ai import eval_test
from board.bit_board import BitBoard
import math

class Search():
    def __init__(self, board, own, opponent, turn):
        self._turn = turn
        self._alpha = math.inf
        self._beta = -math.inf
        self._own = own
        self._opponent = opponent
        self._index = None
        self._board = board
        self._depth = 7
        if(turn >= 0 and turn <= 54):
            self._eval = eval_test.MidEvaluator(board)
        else:
            self._eval = eval_test.WLDEvaluator()

    def search(self):
        tmp = self.beta_cut(self._board, self._depth)
        print('current status')
        self._board.display_board()
        self._eval.evaluate(self._board, self._own)
        return tmp, self._index[0], self._index[1]

    def beta_cut(self, board, depth):
        if(depth == 0):
            evaluation = self._eval.evaluate(board, self._opponent)
            return evaluation
        score_max = -math.inf
        board.listing_puttable(self._own)
        #beta cut
        legals = board.get_puttable_list()
        print('depth:{}'.format(depth), legals)
        if len(legals) != 0:
            i = 0
            max_score = -math.inf
            for coord in legals:
                i += 1
                board1 = copy.deepcopy(board)
                board1.put_stone(int(coord[0]), int(coord[1]), self._own)
                score1 = self.alpha_cut(board1, depth-1)
                if(score1 >= max_score):
                    #より良い手が見つかった
                    if(depth == self._depth):
                        self._index = coord
                    #beta_値を更新
                    max_score = score1
                    self._beta = score1
                if(score1 < max_score):
                    #betacut
                    return max_score
        else:
            score1 = self.alpha_cut(board, depth-1)
        return score1

    def alpha_cut(self, board, depth):
        if(depth == 0):
            evaluation = self._eval.evaluate(board, self._own)
            return evaluation
        board.listing_puttable(self._opponent)
        #alpha cut
        legals = board.get_puttable_list()
        if len(legals) != 0:
            min_score = math.inf
            for coord in board.get_puttable_list():
                board2 = copy.deepcopy(board)
                board2.put_stone(int(coord[0]), int(coord[1]), self._opponent)
                score2 = self.beta_cut(board2, depth-1)
                if(score2 <= min_score):
                    #より悪い手が見つかった
                    if(depth == self._depth):
                        self._index = coord
                    #Alpha値を更新
                    min_score = score2
                    self._alpha = score2
                if(score2 > min_score):
                    #alphacut
                    return min_score
        else:
            score2 = self.beta_cut(board, depth-1)
        return score2
