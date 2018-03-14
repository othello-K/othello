
class BaseUser():

    def __init__(self, bow):
        #if bow == 1, preceding, if 2 after
        self.__bow = bow
        #num of stone
        self.__nstone = 0
        #history
        self.__history = []

    def set_nstone(self, nstone):
        """
        石の数をセット
        """
        self.__nstone = nstone

    def append_history(self, coord):
        """
        ユーザが石を置いた座標の履歴
        """
        self.__history.append(self, coord)

    def display_bow(self):
        """
        ユーザが先攻か後攻か表示
        """
        if self.__bow == 1:
            print("black: preceding attack")
        elif self.__bow == 2:
            print("white: after attack")
        else:
            print("i don't know")

    def get_nstone(self):
        """
        ユーザのとった石の数を表示
        """
        return (self.__nstone)

    def input_coord(self, **kwargs):
        """
        ユーザにインプットさせる．
        ここをオーバーライドしてください
        """
        pass

