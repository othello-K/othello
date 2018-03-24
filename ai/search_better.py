import copy
from ai import eval_test
from board.bit_board import BitBoard
import math

class Search():
    def __init__(self, board, own, opponent, turn):
        self._turn = turn
        self._alpha = -math.inf
        self._beta = math.inf
        self._own = own
        self._opponent = opponent
        self._index = None
        self._board = board
        if(turn >= 1 and turn <= 54):
            self._eval = eval_test.MidEvaluator(board)
        else:
            self._eval = eval_test.PerfectEvaluator()

    def search(self):
        return self.beta_cut(self._board, 6), self._index[0], self._index[1]

    def beta_cut(self, board, depth):
        if(depth == 0):
            evaluation = self._eval.evaluate(board, self._opponent)
            print(evaluation)
            return evaluation
        score_max = -math.inf
        board.display_board()
        board.listing_puttable(self._own)
        for coord in board.get_puttable_list():
            print(coord)
            board1 = copy.deepcopy(board)
            board1.put_stone(int(coord[0]),int(coord[1]), self._own)
            score1 = self.alpha_cut(board1, depth-1)
            if(score1 > score_max):
                #より良い手が見つかった
                score_max = score1
                if(depth == 6):
                    self._index = coord
                    print("hhh")
                #beta_値を更新
                self._beta = min([self._beta,score_max])
            if(score1 >= self._beta):
                #betacut
                return score1
        return score_max

    def alpha_cut(self, board, depth):
        if(depth == 0):
            evaluation = self._eval.evaluate(board, self._own)
            return evaluation
        score_min = math.inf
        board.listing_puttable(self._opponent)
        for coord in board.get_puttable_list():
            board2 = copy.deepcopy(board)
            board2.put_stone(int(coord[0]),int(coord[1]), self._opponent)
            score2 = self.beta_cut(board2, depth-1)
            if(score2 <= self._alpha):
                #alphacut
                return score2
            if(score2 < score_min):
                #より悪い手が見つかった
                score_min = score2
                #Alpha値を更新
                self._alpha = max([self._alpha,score_min])
        return score_min
