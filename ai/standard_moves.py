class StandardMoves:
	def __init__(self, __board, first_x, first_y):
		self.BOARD_SIZE = __board.get_board_size()
		self.Rotate = 0
		self.Mirror = False

        # first_x : 一手目のx座標, first_y : 一手目のy座標
		if(first_x == 3 and first_y == 2):   # d3に置いた時
		    self.Rorate = 1
		    Mirror = True
		elif(first_x == 2 and first_y == 3): # c4
		    self.Rotate = 2
		elif(first_x == 4 and firstY == 5): # e6
			self.Rotate = -1
			Mirror = True


	def rotatePoint(self, old_point_x, old_point_y, rotate):
		rotate %= 4

		if(rotate < 0): rotate += 4

		if(rotate == 1):
			new_point_x = old_point_y
			new_point_y = self.BOARD_SIZE - old_point_x - 1
		elif(ratate == 2):
			new_point_x = self.BOARD_SIZE - old_point_x - 1
			new_point_y = self.BOARD_SIZE - old_point_y - 1
		elif(rotate == 3):
			new_point_x = self.BOARD_SIZE - old_point_y - 1
			new_point_y = old_point_x
		else:
			new_point_x = old_point_x
			new_point_y = old_point_y

		return new_point_x, new_point_y


	def mirrorPoinnt(self, old_point_x, old_point_y):
		new_point_x = self.BOARD_SIZE - new_point_x - 1
		new_point_y = new_point_y

		return new_point_x, new_point_y


    def normalize(point_x, point_y):
    	new_x , new_y = rotatePoint(point_x, point_y, self.Rotate)

