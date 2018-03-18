# 参考 : 『リバーシのアルゴリズム』 星 正明 著　工学社

import copy

# 辺に関するパラメータをまとめたクラス
class EdgeParam:
    def __init__(self):
        self.stable   = None      # 確定石の個数
        self.wing     = None      # wingの個数
        self.mountain = None      # 山の個数 
        self.Cmove    = None      # C打ちの個数 

    def set_value(self, stable, wing, mountain, Cmove):
        self.stable   = stable
        self.wing     = wing
        self.mountain = mountain
        self.Cmove    = Cmove

    # += 演算子をオーバーロード
    def __iadd__(self, src):
        self.stable += src.stable
        self.wing += src.wing
        self.mountain += src.mountain
        self.Cmove += src.Cmove
        return self


# 隅周辺に関するパラメータをまとめたクラス
class CornerParam:
    def __init__(self):
        self.corner   = None        # 隅にある石の数
        self.Xmove    = None        # 危険なX打ちの個数

# 重み係数を規定するクラス
class Weight:
    def __init__(self):
        self.mobility_w = None
        self.liberty_w  = None
        self.stable_w   = None
        self.wing_w     = None
        self.Xmove_w    = None
        self.Cmove_w    = None

# パラメータを空、攻め手、相手の三種類用意
class ColorStorage:
    def __init__(self, class_name):
        self.myside = class_name()
        self.opponent = class_name()

    def __iadd__(self, src):
        self.myside += src.myside
        self.opponent += src.opponent

        return self


# 評価関数の抽象クラス
class Evaluator:
    def evaluate(self, __board, attacker, myside):      # attacker : 石を置く側　 myside : AI自身
        pass

# 終盤の完全読み切り用評価関数
class PerfectEvaluator(Evaluator):
    def evaluate(self, __board, attacker , myside):
        self.discdiff = __board.count_stone(myside) - __board.count_stone(__board.get_opponent(myside))

        # 対戦相手視点の時は符号反転
        if(attacker != myside):
            return -self.discdiff

        return self.discdiff

# 終盤初期で必勝読みを行なう際に用いる評価関数
class WLDEvaluator(Evaluator):
    def __init__(self):
        self.WIN  =  1
        self.DRAW =  0
        self.LOSE = -1 

    def evaluate(self, __board, attacker ,myside):
        self.discdiff = __board.count_stone(myside) - __board.count_stone(__board.get_opponent(myside))

        # 対戦相手視点の時は符号反転
        if(attacker != myside):
            self.discdiff = -self.discdiff

        if(discdiff > 0): return self.WIN;
        elif (discdiff < 0): return self.LOSE;
        else: return self.DRAW

class MidEvaluator(Evaluator):
    def __init__(self, __board, myside):
        self.TABLE_SIZE = 6561     #3^8 
        self.EdgeTable  = [ColorStorage(EdgeParam)] * self.TABLE_SIZE     # 評価テーブルを宣言

        # 初回起動時にテーブルを生成
        self.generateEdge(0, __board, [0]*8 , [0]*8, myside)

        # 重み係数を設定
        self.EvalWeight = Weight()

        self.EvalWeight.movility_w =   67
        self.EvalWeight.liberty_w  =  -13
        self.EvalWeight.stable_w   =  101
        self.EvalWeight.wing_w     = -308
        self.EvalWeight.Xmove_w    = -449
        self.EvalWeight.Cmove_w    = -552


    # テーブルのindexを算出
    def idxLine(self, __board, m_line, o_line , myside):  
        opponent = __board.get_opponent(myside)
        l = []

        for i in range(len(m_line)):
            l.append(m_line[i] * myside + o_line[i] * opponent)

        return 3*(3*(3*(3*(3*(3*(3*l[0]+l[1])+l[2])+l[3])+l[4])+l[5])+l[6])+l[7]

    # 評価
    def evaluate(self, __board, attacker, myside):
        edgestat = ColorStorage(EdgeParam)
        cornerstat = ColorStorage(CornerParam)

        # 辺の評価
        edgestat  = self.EdgeTable[self.idxTop(__board)]
        edgestat += self.EdgeTable[self.idxBottom(__board)]
        edgestat += self.EdgeTable[self.idxRight(__board)]
        edgestat += self.EdgeTable[self.idxLeft(__board)]

        # 隅の評価
        cornerstat = self.evalCorner(__board, myside)

        # 確定石に関して、隅の石を2回数えてしまっているので補正
        edgestat.myside.stable -= cornerstat.myside.corner
        edgestat.opponent.stable -= cornerstat.opponent.corner

        # パラメータの線型結合
        result = \
             edgestat.myside.stable * self.EvalWeight.stable_w\
           - edgestat.opponent.stable * self.EvalWeight.stable_w\
           + edgestat.myside.wing * self.EvalWeight.wing_w\
           - edgestat.opponent.wing * self.EvalWeight.wing_w\
           + cornerstat.myside.Xmove * self.EvalWeight.Xmove_w\
           - cornerstat.opponent.Xmove * self.EvalWeight.Xmove_w\
           + edgestat.myside.Cmove * self.EvalWeight.Cmove_w\
           - edgestat.myside.Cmove * self.EvalWeight.Cmove_w\


        # 開放度・着手可能手数の評価
        if(self.EvalWeight.liberty_w != 0):
            liberty = self.countLiberty(__board, myside)
            result += liberty.myside * self.EvalWeight.liberty_w
            result -= liberty.opponent * self.EvalWeight.liberty_w

        # 現在の手番の色についてのみ、着手可能手数を数える
        __board.listing_puttable(attacker)

        value = len(__board.get_puttable_list()) * self.EvalWeight.movility_w
        
        """
        自分視点の場合 正の値なので+ 敵視点の場合 負の値なので-  
        対戦相手視点の時は符号反転して返す
        """
        if(myside == attacker):
            result += value
            return result
        else:
            result -= value
            return -result


    def generateEdge(self, count, __board, m_edge, o_edge, myside):

        if(count == __board.get_board_size()):
            # このパターンは完成したので、局面のカウント
            stat = ColorStorage(EdgeParam) 

            stat.myside = self.evalEdge(m_edge)
            stat.opponent = self.evalEdge(o_edge)
            self.EdgeTable[self.idxLine(__board, m_edge, o_edge, myside)] = stat;

            return

        # 再帰的に全てのパターンを網羅
        m_edge[count] = 0
        o_edge[count] = 0
        self.generateEdge(count+1, __board, m_edge, o_edge, myside)

        m_edge[count] = 1
        o_edge[count] = 0
        self.generateEdge(count+1, __board, m_edge, o_edge, myside)

        m_edge[count] = 0
        o_edge[count] = 1
        self.generateEdge(count+1, __board, m_edge, o_edge, myside)

        return

    # 辺のパラメータを数える  
    def evalEdge(self, line):
        edgeparam = EdgeParam()
        edgeparam.set_value(0, 0, 0, 0)

        # ウィング等のカウント
        if(line[0]== 0 and line[7] == 0):
            x = 2;
            while(x <= 5):
                if(line[x] != 1):
                    break
                    
                x += 1
            if(x == 6):     # 少なくともブロックができている
                if(line[1] == 1 and line[6] == 0):
                    edgeparam.wing = 1
                elif(line[1] == 0 and line[6] == 1):
                    edgeparam.wing = 1
                elif(line[1] == 1 and line[6] == 1):
                    edgeparam.mountain = 1
            else:           # それ以外の場合に、隅に隣接する位置に置いていたら  
                if(line[1] == 1):
                    edgeparam.Cmove += 1;
                if(line[6] == 1):
                    edgeparam.Cmove += 1;

        # 左から右方向へ走査
        for i in range(8):
            if(line[i] != 1):
                break
            edgeparam.stable += 1

        if(edgeparam.stable < 8):
            # 右側からも走査
            for i in reversed(range(8)):
                if(line[i] != 1):
                    break
                edgeparam.stable += 1

        return edgeparam



    # 隅のパラメータを調べる。この関数は各評価時に行う
    def evalCorner(self, __board, myside):
        cornerstat = ColorStorage(CornerParam)

        cornerstat.myside.corner=0
        cornerstat.myside.Xmove=0
        cornerstat.opponent.corner=0
        cornerstat.opponent.Xmove=0

        opponent = __board.get_opponent(myside)


        # 左上
        if(__board.get_stone(0, 0, myside) == 1):
            cornerstat.myside.corner += 1
        elif(__board.get_stone(0, 0, opponent) == 1):
            cornerstat.opponent.corner += 1
        else:
            if(__board.get_stone(1, 1, myside) == 1):
                cornerstat.myside.Xmove += 1
            elif(__board.get_stone(1, 1, opponent) == 1):
                cornerstat.opponent.Xmove += 1


        # 左下
        if(__board.get_stone(0, 7, myside) == 1):
            cornerstat.myside.corner += 1
        elif(__board.get_stone(0, 7, opponent) == 1):
            cornerstat.opponent.corner += 1
        else:
            if(__board.get_stone(1, 6, myside) == 1):
                cornerstat.myside.Xmove += 1
            elif(__board.get_stone(1, 6, opponent) == 1):
                cornerstat.opponent.Xmove += 1

        # 右下
        if(__board.get_stone(7, 6, myside) == 1):
            cornerstat.myside.corner += 1
        elif(__board.get_stone(7, 6, opponent) == 1):
            cornerstat.opponent.corner += 1

        if(__board.get_stone(7, 7, myside) == 0 and __board.get_stone(7, 7, opponent) == 0):
            if(__board.get_stone(6, 6, myside) == 1):
                cornerstat.myside.Xmove += 1
            elif(__board.get_stone(6, 6, opponent) == 1):
                cornerstat.opponent.Xmove += 1

        # 右上
        if(__board.get_stone(7, 0, myside) == 1):
            cornerstat.myside.corner += 1
        elif(__board.get_stone(7, 0, opponent) == 1):
            cornerstat.opponent.corner += 1

        if(__board.get_stone(7, 0, myside) == 0 and __board.get_stone(7, 0, opponent) == 0):
            if(__board.get_stone(6, 1, myside) == 1):
                cornerstat.myside.Xmove += 1
            elif(__board.get_stone(6, 1, opponent) == 1):
                cornerstat.opponent.Xmove += 1

        return cornerstat

    def countLiberty(self, __board ,myside):
        liberty = ColorStorage(int)

        liberty.myside = 0
        liberty.opponent = 0

        opponent = __board.get_opponent(myside)


        for x in range(0, __board.get_board_size()):
            for y in range(0, __board.get_board_size()):
                value = __board.get_liberty(x, y)
                if(__board.get_stone(x, y, myside) == 1):
                    liberty.myside += value
                elif(__board.get_stone(x, y, opponent) == 1):
                    liberty.opponent += value

            return liberty

    # 各箇所についてのインデックスの計算  
    def idxTop(self, __board):
        # 各箇所についてのインデックスの計算  
        index = \
              2187 * (__board.get_player(0,0) )\
              +729 * (__board.get_player(1,0) )\
              +243 * (__board.get_player(2,0) )\
              + 81 * (__board.get_player(3,0) )\
              + 27 * (__board.get_player(4,0) )\
              +  9 * (__board.get_player(5,0) )\
              +  3 * (__board.get_player(2,0) )\
              +  1 * (__board.get_player(2,0) )

        return index

    def idxBottom(self, __board):

        index = \
              2187 * (__board.get_player(0,7) )\
              +729 * (__board.get_player(1,7) )\
              +243 * (__board.get_player(2,7) )\
              + 81 * (__board.get_player(3,7) )\
              + 27 * (__board.get_player(4,7) )\
              +  9 * (__board.get_player(5,7) )\
              +  3 * (__board.get_player(2,7) )\
              +  1 * (__board.get_player(2,7) )

        return index

    def idxRight(self, __board):

        index = \
              2187 * (__board.get_player(7,0) )\
              +729 * (__board.get_player(7,1) )\
              +243 * (__board.get_player(7,2) )\
              + 81 * (__board.get_player(7,3) )\
              + 27 * (__board.get_player(7,4) )\
              +  9 * (__board.get_player(7,5) )\
              +  3 * (__board.get_player(7,6) )\
              +  1 * (__board.get_player(7,7) )

        return index


    def idxLeft(self, __board):

        index = \
              2187 * (__board.get_player(0,0) )\
              +729 * (__board.get_player(0,1) )\
              +243 * (__board.get_player(0,2) )\
              + 81 * (__board.get_player(0,3) )\
              + 27 * (__board.get_player(0,4) )\
              +  9 * (__board.get_player(0,5) )\
              +  3 * (__board.get_player(0,6) )\
              +  1 * (__board.get_player(0,7) )

        return index
