import copy
import sys
from ai.eval.
sys.path.append('../')
from bit_board import BitBoard

def AlphaBeta(board, list, own, opponent):  # AlphaBeta法で探索する
    evaluations = AlphaBeta_evaluate1(board, list, own, opponent)
    maximum_evaluation_index = evaluations.index(max(evaluations))
    x, y = list[maximum_evaluation_index]
    return evaluations, x, y

def AlphaBeta_evaluate1(board, list, own, opponent):
    def pruning2(max_evaluations3):
        return len(evaluations1) > 0 and max(evaluations1) >= max_evaluations3
    evaluations1 = []
    board.listing_puttable(own)
    for coord in board.get_puttable_list():
        board1 = copy.deepcopy(board)
        board1.put_stone(int(coord[0]),int(coord[1]), own)
        evaluations2 = AlphaBeta_evaluate2(board1, own, opponent, pruning2)
        if len(evaluations2) > 0:
            evaluations1 += [min(evaluations2)]
    return evaluations1

def AlphaBeta_evaluate2(board, own, opponent, pruning):
    def pruning3(min_evaluations4):
        return len(evaluations2) > 0 and min(evaluations2) <= min_evaluations4
    evaluations2 = []
    board.listing_puttable(opponent)
    for coord in board.get_puttable_list():
        board2 = copy.deepcopy(board)
        board2.put_stone(int(coord[0]),int(coord[1]), opponent)
        evaluations3 = AlphaBeta_evaluate3(board2, own, opponent, pruning3)
        if len(evaluations3) > 0:
            max_evaluations3 = max(evaluations3)
            evaluations2 += [max_evaluations3]
            if pruning(max_evaluations3):
                break
    return evaluations2

def AlphaBeta_evaluate3(board, own, opponent, pruning):
    def pruning4(max_evaluations5):
        return len(evaluations3) > 0 and max(evaluations3) >= max_evaluations5
    evaluations3 = []
    board.listing_puttable(own)
    for coord in board.get_puttable_list():
        board3 = copy.deepcopy(board)
        board3.put_stone(int(coord[0]),int(coord[1]), own)
        evaluations4 = AlphaBeta_evaluate4(board3, own, opponent, pruning4)
        if len(evaluations4) > 0:
            min_evaluations4 = min(evaluations4)
            evaluations3 += [min_evaluations4]
            if pruning(min_evaluations4):
                break
    return evaluations3

def AlphaBeta_evaluate4(board, own, opponent, pruning):
    def pruning5(min_evaluations6):
        return len(evaluations4) > 0 and min(evaluations4) <= min_evaluations6
    evaluations4 = []
    board.listing_puttable(opponent)
    for coord in board.get_puttable_list():
        board4 = copy.deepcopy(board)
        board4.put_stone(int(coord[0]),int(coord[1]), opponent)
        evaluations5 = AlphaBeta_evaluate5(board4, own, opponent, pruning5)
        if len(evaluations5) > 0:
            max_evaluations5 = max(evaluations5)
            evaluations4 += [max_evaluations5]
            if pruning(max_evaluations5):
                break
    return evaluations4

def AlphaBeta_evaluate5(board, own, opponent, pruning):
    def pruning6(evaluation6):
        return len(evaluations5) > 0 and max(evaluations5) >= evaluation6
    evaluations5 = []
    board.listing_puttable(own)
    for coord in board.get_puttable_list():
        board5 = copy.deepcopy(board)
        board5.put_stone(int(coord[0]),int(coord[1]), own)
        evaluations6 = AlphaBeta_evaluate6(board5, own, opponent, pruning6)
        if len(evaluations6) > 0:
            min_evaluation6 = min(evaluations6)
            evaluations5 += [min_evaluation6]
            if pruning(min_evaluation6):
                break
    return evaluations5

def AlphaBeta_evaluate6(board, own, opponent, pruning):
    evaluations6 = []
    board.listing_puttable(opponent)
    for coord in board.get_puttable_list():
        board6 = copy.deepcopy(board)
        board6.put_stone(int(coord[0]),int(coord[1]), opponent)
        ev_opponent = evaluation(board6, opponent)
        ev_own = evaluation(board6, own)
        evaluation = ev_own - ev_opponent
        evaluations6 += [evaluation]
        if pruning(evaluation):
            break
    return evaluations6

if __name__ == "__main__":
    b = BitBoard()
    b.init_board("init.csv")
    cb = copy.deepcopy(b)
    cb.listing_puttable(1)
    list = cb.get_puttable_list()
    AlphaBeta(cb,list, 1,  cb.get_opponent(1))
    print("正常")
    
