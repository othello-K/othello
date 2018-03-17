


def negamax(board, attacker, own, depth):
    if(depth <= 0 and attacker == own):
        evaluation = evaluate(board, own, own)
    elif(depth <= 0 and attacker == opponent):
        evaluation = evaluate(board, opponent, own)
        return evaluation
    board.listing_puttable()
    evaluation_max = -math.inf
    for coord in board.get_puttable_list():
        board1 = copy.deepcopy(board)
        board1.put_stone(int(coord[0]),int(coord[1]),own)
        score = negamax(board1, opponent, own, depth-1)
