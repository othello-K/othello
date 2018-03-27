import numpy as np

class InvalidArgument (Exception):
  """
  想定外の引数が渡された時に発生させる例外
  """
  def __init__ (self):         
    print ('ArgumentError : The argument must be Reversi style coordinates!')


class Point:
    def __init__(self, coord = None):

        # numpy array なら
        if(type(coord).__module__ == np.__name__):
            self.x = coord[0]
            self.y = coord[1]
            return

        # None or list なら
        if(coord == None):
            self.x = None
            self.y = None
            return
        elif(len(coord) < 2):
            raise InvalidArgument()
        elif(isinstance(coord[0], str) or isinstance(coord[1], str)):
            self.x = ord(coord[0]) - ord('a')
            self.y = ord(coord[1]) - ord('1')
            return
        elif(not isinstance(coord[0], int) or not isinstance(coord[1], int)):
            self.x = int(coord[0])
            self.y = int(coord[1])
            return
        else:
            self.x = coord[0]
            self.y = coord[1]
            return


class Node:
    def __init__(self):
        self.child = None
        self.sibling = None
        self.point = Point()
    

class StandardMoves:
    def __init__(self, __board, first):
        self.BOARD_SIZE = __board.get_board_size()
        self.Rotate = 0
        self.Mirror = False

        # first.x : 一手目のx座標, first.y : 一手目のy座標
        if(first.x == 3 and first.y == 2):   # d3に置いた時
            self.Rorate = 1
            Mirror = True
        elif(first.x == 2 and first.y == 3): # c4
            self.Rotate = 2
        elif(first.x == 4 and first.y == 5): # e6
            self.Rotate = -1
            Mirror = True


    def rotatePoint(self, old_point, rotate):
        new_p = Point()
        rotate %= 4

        if(rotate < 0): rotate += 4

        if(rotate == 1):
            new_p.x = old_point.y
            new_p.y = self.BOARD_SIZE - old_point.x - 1
        elif(rotate == 2):
            new_p.x = self.BOARD_SIZE - old_point.x - 1
            new_p.y = self.BOARD_SIZE - old_point.y - 1
        elif(rotate == 3):
            new_p.x = self.BOARD_SIZE - old_point.y - 1
            new_p.y = old_point.x
        else:
            new_p.x = old_point.x
            new_p.y = old_point.y

        return new_p


    def mirrorPoint(self, old_point):
        new_p = Point()

        new_p.x = self.BOARD_SIZE - old_point.x - 1
        new_p.y = old_point.y

        return new_p


    def normalize(self, point):
        new_p = self.rotatePoint(point, self.Rotate)
        if(self.Mirror): 
            new_p = self.mirrorPoint(new_p)

        return new_p


    def denormalize(self, point):
        new_p = point
        if(self.Mirror):
            new_p = self.mirrorPoint(new_p)

        new_p = self.rotatePoint(new_p, -self.Rotate)

        return new_p




