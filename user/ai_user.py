import copy

from user.base_user import BaseUser
from ai.search import Search

class AiUser(BaseUser):

    def input_coord(self, **kwargs):
        """
        ユーザにインプットさせる．
        """
        board = kwargs['board']
        atk = kwargs['bow']
        opp = board.get_opponent(atk)
        game = kwargs['game']
        tmp_board = copy.deepcopy(board)
        search = Search(board, atk)
        evaluation, x, y = search.AlphaBeta(tmp_board, tmp_board.get_puttable_list(),\
                                    atk, opp, game.get_turn())
        game.game_process(None, int(x), int(y), atk)
