from user.base_user import BaseUser

class User(BaseUser):

    def input_coord(self, **kwargs):
        """
        ユーザにインプットさせる．
        """
        atk = kwargs['bow']
#        gui_board = kwargs['board']
#        gui_board.display_board()
