from board.board import Board
from user.user import User
from game.base_game import BaseGame
import numpy as np

class CuiGame(BaseGame):
    """
    GameのCUI実装
    """

    def __init__(self):
        super(CuiGame, self).__init__()

    def start_game(self):
        """
        ゲームの流れが書いてあるメソッド
        """
        while True:
            #置ける場所を探す
            self.__board.listing_puttable(self.__attacker)
            #ボードを表示
            self.__board.display_board()
            #GUIボードを表示
            self.__gui_board.set_board(self.__board)
            self.__gui_board.display_board(self.__attacker)

            print("player {}'s attack".format(self.__attacker))

            #ゲームの終了判定
            #置ける場所がないとフラグがたつ
            if self.__board.is_no_puttable():
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

            #ユーザに入力させる
            self.input_coord(self.__attacker)

            #入力座標の履歴の最後尾を取り出し，そこに石をおく．
            self.put_stone(int(self.__input_list[-1][0]), int(self.__input_list[-1][1]), self.__attacker)

            #石の数を数えてユーザにセット
            self.set_nstone(self.__board.count_stone(self.__attacker), self.__attacker)

            #ターンを増やし，攻撃を変更
            self.__turn += 1
            self.__attacker = self.__turn % 2 + 1

    def end_game(self):
        """
        ゲーム終了時の処理．勝敗と石の数を表示．
        """

        if nstone1 > nstone2:
            print("Black Win!")
        elif nstone1 < nstone2:
            print("White Win!")
        else:
            print("DRAW!")
