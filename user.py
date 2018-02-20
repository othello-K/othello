
class User():

    def __init__(self, bow):
        #if bow == 1, preceding, if 2 after
        self.__bow = bow
        #num of stone
        self.__nstone = 0
        #history
        self.__history = []
        #type: HUMAN=1, CPU > 1
        self.type = 1

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

    def human_input(self):
        print('input coordinate x')
        coorx = input('coor x:')

        print('input coordinate x')
        coory = input('coor y:')

        return np.array([int(coorx), int(coory)])

    def input_coor(self):
        if self.__type == 1:
            self.human_input()

