
class User():

    def __init__(self, bow):
        #if bow == 1, preceding, if 2 after
        self.__bow = bow
        #num of stone
        self.__nstone = 0
        #history
        self.__history = []

    def set_nstone(self, nstone):
        self.__nstone = nstone

    def append_history(self, coor):
        self.__history.append(self, coor)

    def out_bow(self):
        if self.__bow == 1:
            print("black: preceding attack")
        elif self.__bow == 2:
            print("white: after attack")
        else:
            print("i don't know")

    def get_nstone(self):
        return (self.__nstone)
