class Node:
    child = Node()
    sibling = Node()
    point = [None, None]


class BookManager:
	def __init__(self, own):
		self.Root = None
		self.own


	def find(self, __board, __game):
		node = self.Root
		history = __game.get_input_history

		__board.listing_puttable(self.own)
		if(!history): return __board.get_puttable_list()

		first = history[0]
		transformer = StandardMoves(__board, first[0], first[1])

		normalized = []
        
        # 座標を変換してf5(5,4)から始まるようにする
		for i in range(len(history)):
			point = history[i]
			point = transformer.normalize(point[0], point[1])

			normalized += point

		# 現在までの棋譜リストと定石の対応をとる
		for i in range(len(normalized)):
			point = normalized[i]

			node = node.child
			while(node != None):
				if(node.point == point): break

				node = node.sibling

			if(Node == None):
				# 定石を外れている
				__board.listing_puttable(self.own)
				return __board.get_puttable_list()

		# 履歴と定石の終わりが一致していた場合
		if(node.child == None): 
			__board.listing_puttable(self.own)
			return __board.get_puttable_list()

		next_move = self.getNextMove(node)

		# 座標を元の形に変換する
		next_move = transformer.denormalize(next_move[0], next_move[1])














