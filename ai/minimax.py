
import copy
import sys
sys.path.append("../")
from bit_board import BitBoard
from eval import evaluate
import math

def maxlevel(board, own, opponent, depth):
    if(depth <= 0):
        evaluation_max = evaluate(board, own)
        return evaluation_max
    board.listing_puttable(own)
    evaluation_max = -math.inf
    for coord in board.get_puttable_list():
        board1 = copy.deepcopy(board)
        board1.put_stone(int(coord[0]),int(coord[1]),own)
        score = minlevel(board1, own, opponent, depth-1)
        if(score > evaluation_max):
            evaluation_max = score
    return evaluation_max

def minlevel(board, own, opponent, depth):
    if(depth <= 0):
        evaluation_min = evaluate(board, opponent)
        return evaluation_min    
    board.listing_puttable(opponent)
    evaluation_min = math.inf
    for coord in board.get_puttable_list():
        board2 = copy.deepcopy(board)
        board2.put_stone(int(coord[0]),int(coord[1]),opponent)
        score = maxlevel(board2, own, opponent, depth-1)
        if(score < evaluation_min):
            evaluation_min = score
    return evaluation_min

if __name__ == "__main__":
    b = BitBoard()
    b.init_board("../init.csv")
    b.display_board()
    cb = copy.deepcopy(b)
    print("深さいくつ？")
    depth = int(input())
    print(maxlevel(cb, 1, cb.get_opponent(1), depth))
    evaluate(cb,1)

