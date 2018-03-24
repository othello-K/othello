# 参考 : 『リバーシのアルゴリズム』 星 正明 著　工学社

import copy

# 辺に関するパラメータをまとめたクラス
class EdgeParam:
    def __init__(self):
        self.stable   = 0     # 確定石の個数
        self.wing     = 0     # wingの個数
        self.mountain = 0     # 山の個数 
        self.Cmove    = 0     # C打ちの個数 

    def set_value(self, stable, wing, mountain, Cmove):
        self.stable   = stable
        self.wing     = wing
        self.mountain = mountain
        self.Cmove    = Cmove

    # += 演算子をオーバーロード
    def __iadd__(self, src):
        #print("src.stable : " + str(src.stable))
        self.stable += src.stable
        self.wing += src.wing
        self.mountain += src.mountain
        self.Cmove += src.Cmove

        return self


# 隅周辺に関するパラメータをまとめたクラス
class CornerParam:
    def __init__(self):
        self.corner   = 0        # 隅にある石の数
        self.Xmove    = 0        # 危険なX打ちの個数

    def set_value(self, corner, Xmove):
        self.corner   = corner
        self.Xmove    = Xmove


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
        self.black = class_name()
        self.white = class_name()

    def __iadd__(self, src):
        self.black += src.black
        self.white += src.white

        return self


# 評価関数の抽象クラス
class Evaluator:
    def evaluate(self, __board, attacker):      # attacker : 石を置く側　 myside : AI自身
        pass

# 終盤の完全読み切り用評価関数
class PerfectEvaluator(Evaluator):     
    def evaluate(self, __board, attacker):
        # black - white
        self.discdiff = __board.count_stone(1) - __board.count_stone(__board.get_opponent(2))

        # 白視点の時は符号反転
        if(attacker != 1):
            return -self.discdiff

        return self.discdiff

# 終盤初期で必勝読みを行なう際に用いる評価関数
class WLDEvaluator(Evaluator):
    def __init__(self):
        self.WIN  =  1
        self.DRAW =  0
        self.LOSE = -1

    def evaluate(self, __board, attacker):
        # black - white
        self.discdiff = __board.count_stone(1) - __board.count_stone(__board.get_opponent(2))

        # 白視点の時は符号反転
        if(attacker != 1):
            self.discdiff = -self.discdiff

        if(discdiff > 0): return self.WIN;
        elif (discdiff < 0): return self.LOSE;
        else: return self.DRAW

class MidEvaluator(Evaluator):
    def __init__(self, __board):
        self.TABLE_SIZE = 6561     #3^8 
        self.EdgeTable  = [ColorStorage(EdgeParam) for i in range(self.TABLE_SIZE)]    # 評価テーブルを宣言
        self._BLACK = 1
        self._WHITE = 2

        # 初回起動時にテーブルを生成
        self.generateEdge(0, __board, [0]*8 , [0]*8)

        """
        for i in range(self.TABLE_SIZE):
            print(str(i) + " : " + str(self.EdgeTable[i].black.stable) )
        """

        # 重み係数を設定
        self.EvalWeight = Weight()

        self.EvalWeight.movility_w =   67
        self.EvalWeight.liberty_w  =  -13
        self.EvalWeight.stable_w   =  101
        self.EvalWeight.wing_w     = -308
        self.EvalWeight.Xmove_w    = -449
        self.EvalWeight.Cmove_w    = -552


    # テーブルのindexを算出
    def idxLine(self, __board, b_line, w_line):
        l = []

        for i in range(len(b_line)):
            l.append(b_line[i] * 1 + w_line[i] * 2)

        return 3*(3*(3*(3*(3*(3*(3*l[0]+l[1])+l[2])+l[3])+l[4])+l[5])+l[6])+l[7]

    # 評価
    def evaluate(self, __board, attacker):
        edgestat = ColorStorage(EdgeParam)
        cornerstat = ColorStorage(CornerParam)

        # 辺の評価

        stat = self.EdgeTable[self.idxTop(__board)]
        #edgestat  = self.EdgeTable[self.idxTop(__board)]
        edgestat.black.set_value(stat.black.stable, stat.black.wing, stat.black.mountain, stat.black.Cmove)
        edgestat.white.set_value(stat.white.stable, stat.white.wing, stat.white.mountain, stat.white.Cmove) 

        """        
        print("black-stable-bottom : " + str(self.EdgeTable[self.idxBottom(__board)].black.stable))
        print("white-stable-bottom : " + str(self.EdgeTable[self.idxBottom(__board)].white.stable))
        print("black-stable-right : " + str(self.EdgeTable[self.idxRight(__board)].black.stable))
        print("white-stable-right : " + str(self.EdgeTable[self.idxRight(__board)].white.stable))
        print("black-stable-left : " + str(self.EdgeTable[self.idxLeft(__board)].black.stable))
        print("white-stable-left : " + str(self.EdgeTable[self.idxLeft(__board)].white.stable))
        """
        

        edgestat += self.EdgeTable[self.idxBottom(__board)]
        edgestat += self.EdgeTable[self.idxRight(__board)]
        edgestat += self.EdgeTable[self.idxLeft(__board)]

        print("black : " + str(format(__board._bl_board, '016x')))
        print("white : " + str(format(__board._wh_board, '016x')))


        # 隅の評価
        stat = self.evalCorner(__board)
        cornerstat.black.set_value(stat.black.corner, stat.black.Xmove)
        cornerstat.white.set_value(stat.white.corner, stat.white.Xmove)


        # 確定石に関して、隅の石を2回数えてしまっているので補正
        edgestat.black.stable -= cornerstat.black.corner
        edgestat.white.stable -= cornerstat.white.corner


        # パラメータの線型結合 black - white
        result = \
             edgestat.black.stable * self.EvalWeight.stable_w\
           - edgestat.white.stable * self.EvalWeight.stable_w\
           + edgestat.black.wing * self.EvalWeight.wing_w\
           - edgestat.white.wing * self.EvalWeight.wing_w\
           + cornerstat.black.Xmove * self.EvalWeight.Xmove_w\
           - cornerstat.white.Xmove * self.EvalWeight.Xmove_w\
           + edgestat.black.Cmove * self.EvalWeight.Cmove_w\
           - edgestat.white.Cmove * self.EvalWeight.Cmove_w\

        print("--------------------------")
        print("stable : " + str(edgestat.black.stable) + " , " + str(edgestat.white.stable))
        print("corner : " + str(cornerstat.black.corner) + " , " + str(cornerstat.white.corner))
        print("wing : " + str(edgestat.black.wing) + " , " + str(edgestat.white.wing))
        print("Xmove : " + str(cornerstat.black.Xmove) + " , " + str(cornerstat.white.Xmove))
        print("Cmove : " + str(edgestat.black.Cmove) + " , " + str(edgestat.white.Cmove))


        # 開放度・着手可能手数の評価
        if(self.EvalWeight.liberty_w != 0):
            liberty = self.countLiberty(__board)
            print("liberty : " + str(liberty.black) + " , " + str(liberty.white))
            result += liberty.black * self.EvalWeight.liberty_w
            result -= liberty.white * self.EvalWeight.liberty_w

        # 現在の手番の色についてのみ、着手可能手数を数える
        __board.listing_puttable(attacker)

        movility = len(__board.get_puttable_list()) * self.EvalWeight.movility_w
        print("movility : " + str(movility))
        
        """
        自分視点の場合 正の値なので+ 敵視点の場合 負の値なので-  
        対戦相手視点の時は符号反転して返す
        """
        if(attacker == 1):  # 黒が攻めの時 
            result += movility
            print("result : " + str(result))
            print("--------------------------")
            return result
        else:               # 白が攻めの時 
            result -= movility
            print("result : " + str(-result))
            print("--------------------------")
            return -result


    def generateEdge(self, count, __board, b_edge, w_edge):

        if(count == __board.get_board_size()):
            # このパターンは完成したので、局面のカウント
            stat = ColorStorage(EdgeParam) 

            stat.black = self.evalEdge(b_edge)
            stat.white = self.evalEdge(w_edge)
            self.EdgeTable[self.idxLine(__board, b_edge, w_edge)] = stat;

            return

        # 再帰的に全てのパターンを網羅
        b_edge[count] = 0
        w_edge[count] = 0
        self.generateEdge(count+1, __board, b_edge, w_edge)

        b_edge[count] = 1
        w_edge[count] = 0
        self.generateEdge(count+1, __board, b_edge, w_edge)

        b_edge[count] = 0
        w_edge[count] = 1
        self.generateEdge(count+1, __board, b_edge, w_edge)

        return

    # 辺のパラメータを数える  
    def evalEdge(self, line):
        edgeparam = EdgeParam()
        edgeparam.set_value(0, 0, 0, 0)

        # ウィング等のカウント
        if(line[0]== 0 and line[7] == 0):
            x = 2
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

        # 確定石のカウント
        # 左から右方向へ走査
        for i in range(8):
            if(line[i] != 1): break
            edgeparam.stable += 1

        if(edgeparam.stable < 8):
            # 右側からも走査
            for i in reversed(range(8)):
                if(line[i] != 1): break
                edgeparam.stable += 1

        return edgeparam



    # 隅のパラメータを調べる。この関数は各評価時に行う
    def evalCorner(self, __board):
        cornerstat = ColorStorage(CornerParam)

        cornerstat.black.corner=0
        cornerstat.black.Xmove=0
        cornerstat.white.corner=0
        cornerstat.white.Xmove=0



        # 左上
        if(__board.get_stone(0, 0, self._BLACK) == 1):
            print("left-top1")
            cornerstat.black.corner += 1
        elif(__board.get_stone(0, 0, self._WHITE) == 1):
            print("left-top2")
            cornerstat.white.corner += 1
        else:
            if(__board.get_stone(1, 1, self._BLACK) == 1):
                print("left-top-X1")
                cornerstat.black.Xmove += 1
            elif(__board.get_stone(1, 1, self._WHITE) == 1):
                print("left-top-X2")
                cornerstat.white.Xmove += 1


        # 左下
        if(__board.get_stone(0, 7, self._BLACK) == 1):
            print("left-bottom1")
            cornerstat.black.corner += 1
        elif(__board.get_stone(0, 7, self._WHITE) == 1):
            print("left-bottom2")
            cornerstat.white.corner += 1
        else:
            if(__board.get_stone(1, 6, self._BLACK) == 1):
                print("left-bottom-X1")
                cornerstat.black.Xmove += 1
            elif(__board.get_stone(1, 6, self._WHITE) == 1):
                print("left-bottom-X2")
                cornerstat.white.Xmove += 1

        # 右下
        if(__board.get_stone(7, 7, self._BLACK) == 1):
            print("right-bottom1")
            cornerstat.black.corner += 1
        elif(__board.get_stone(7, 7, self._WHITE) == 1):
            print("right-bottom2")
            cornerstat.white.corner += 1
        else:
            if(__board.get_stone(6, 6, self._BLACK) == 1):
                print("right-bottom-X1")
                cornerstat.black.Xmove += 1
            elif(__board.get_stone(6, 6, self._WHITE) == 1):
                print("right-bottom-X2")
                cornerstat.white.Xmove += 1

        # 右上
        if(__board.get_stone(7, 0, self._BLACK) == 1):
            print("right-top1")
            cornerstat.black.corner += 1
        elif(__board.get_stone(7, 0, self._WHITE) == 1):
            print("right-top2")
            cornerstat.white.corner += 1
        else:
            if(__board.get_stone(6, 1, self._BLACK) == 1):
                print("right-top-X1")
                cornerstat.black.Xmove += 1
            elif(__board.get_stone(6, 1, self._WHITE) == 1):
                print("right-top-X2")
                cornerstat.white.Xmove += 1

        return cornerstat

    def countLiberty(self, __board):
        liberty = ColorStorage(int)

        liberty.black = 0
        liberty.white = 0

        for x in range(0, __board.get_board_size()):
            for y in range(0, __board.get_board_size()):
                value = __board.get_liberty(x, y)
                if(__board.get_stone(x, y, self._BLACK) == 1):
                    liberty.black += value
                elif(__board.get_stone(x, y, self._WHITE) == 1):
                    liberty.white += value

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
              +  3 * (__board.get_player(6,0) )\
              +  1 * (__board.get_player(7,0) )

        return index

    def idxBottom(self, __board):

        index = \
              2187 * (__board.get_player(0,7) )\
              +729 * (__board.get_player(1,7) )\
              +243 * (__board.get_player(2,7) )\
              + 81 * (__board.get_player(3,7) )\
              + 27 * (__board.get_player(4,7) )\
              +  9 * (__board.get_player(5,7) )\
              +  3 * (__board.get_player(6,7) )\
              +  1 * (__board.get_player(7,7) )

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
