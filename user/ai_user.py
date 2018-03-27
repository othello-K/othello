import copy

from user.base_user import BaseUser
from ai.search_better import Search

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
        search = Search(board, atk, opp, game.get_turn(), game)
        evaluation, x, y = search.search()
        game.game_process(None, int(x), int(y), atk)
