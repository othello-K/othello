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


	def rotatePoint(self, old_point, rotate):
		new_p = []
		rotate %= 4

		if(rotate < 0): rotate += 4

		if(rotate == 1):
			new_p.append(old_point[1])
			new_p.append(self.BOARD_SIZE - old_point[0] - 1)
		elif(ratate == 2):
			new_p.append(self.BOARD_SIZE - old_point[0] - 1)
			new_p.append(self.BOARD_SIZE - old_point[1] - 1)
		elif(rotate == 3):
			new_p.append(self.BOARD_SIZE - old_point[1] - 1)
			new_p.append(old_point[0])
		else:
			new_p.append(old_point[0])
			new_p.append(old_point[1])

		return new_p


	def mirrorPoint(self, old_point):
		new_p = []

		new_p.append(self.BOARD_SIZE - old_point[0] - 1)
		new_p.append(old_point[1])

		return new_p


    def normalize(self, point):
    	new_p = rotatePoint(point, self.Rotate)
    	if(Mirror): 
    		new_p= mirrorPoint(new_p)

    	new_p = rotatePoint(new_p, -self.Rotate)

    	return new_p


    def denormalize(self, point):
    	if(Mirror):
    		new_p = mirrorPoint(point)

    		new_p = rotatePoint(new_p, -self.Rotate)



