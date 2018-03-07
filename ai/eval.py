
EVALUATION_BOARD = (  # どのマスに石があったら何点かを表す評価ボード
    ( 45, -11,  4, -1, -1,  4, -11,  45),
    (-11, -16, -1, -3, -3, -1, -16, -11),
    (  4,  -1,  2, -1, -1,  2,  -1,   4),
    ( -1,  -3, -1,  0,  0, -1,  -3,  -1),
    ( -1,  -3, -1,  0,  0, -1,  -3,  -1),
    (  4,  -1,  2, -1, -1,  2,  -1,   4),
    (-11, -16, -1, -3, -3, -1, -16, -11),
    ( 45, -11,  4, -1, -1,  4, -11,  45))

def evaluate(bb, bow):  # 任意の盤面のどちらかの石の評価値を計算する
    # bb = bit_board
    bp = 0
    opp = bb.get_opponent(bow)
    for x in range(bb.get_board_size()):
        for y in range(bb.get_board_size()):
            if bb.get_stone(x,y,bow) == 0 and bb.get_stone(x,y,opp):   #  (x,y)に石が置いてあるか
                pass
            elif bb.get_stone(x,y,bow) == 1:
                bp += EVALUATION_BOARD[x][y] * random.random() * 3
            else:
                bp -= EVALUATION_BOARD[x][y] * random.random() * 3

    p = confirm_stone(bb, bow)
    q = confirm_stone(bb, opp)
    fs = ((p - q) + random.random() * 3) * 11

    b = bb.listing_puttable(bow)
    cn = (len(b) + random.random() * 2) * 10

    evaluation = bp * 2 + fs * 5 + cn * 1
    return evaluation

def confirm_stone(bb, bow):  # 確定石の数を数える
    # bb = bit_board
    forward = range(0, bb.get_board_size())
    backward = range(bb.get_board_size() - 1, -1, -1)
    corners = ((+0, +0, forward, forward),
               (+0, -1, forward, backward),
               (-1, +0, backward, forward),
               (-1, -1, backward, backward))
    confirm = 0
    for x, y, rangex, rangey in corners:
        for ix in rangex:
            if bb.get_stone(ix,y,bow) != 1:
                break
            confirm += 1
        for iy in rangey:
            if bb.get_stone(x,iy,bow) != 1:
                break
            confirm += 1
    return confirm