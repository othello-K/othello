from numpy.random import *
import os.path
from ai import standard_moves as sm
import numpy as np


class BookManager:
	def __init__(self, own):
		self.own = own
		self.BOOK_FILE_NAME = "ai/reversi.book"

		self.Root = sm.Node()
		self.Root.point = sm.Point([5, 4]) # f5

		ifs = open(self.BOOK_FILE_NAME, "r")
		book = []
		for line in ifs:
			book = []
			for i in range(0, len(line)-1, 2):
				try:
					p = sm.Point(line[i:])
				except sm.InvalidArgument:
					break

				book.append(p)
			self.add(book)

		ifs.close


	def compare(self, lhs, rhs):  # lhs : left hand size, rhs : right hand size
		if(lhs.x != rhs.x): return False
		if(lhs.y != rhs.y): return False

		return True


	def find(self, __board, __game , puttable):
		node = self.Root
		history = __board.get_input_history()
		print( "history : " , history)

		print("puttable list : ", puttable)
		if(not history): return puttable

		first = sm.Point(history[0])
		transformer = sm.StandardMoves(__board, first)

		normalized = []
        
        # 座標を変換してf5(5,4)から始まるようにする
		for i in range(len(history)):
			point = sm.Point(history[i])
			point = transformer.normalize(point)

			normalized.append(point)

		# 現在までの棋譜リストと定石の対応をとる
		for i in range(len(normalized)):
			point = normalized[i]

			node = node.child
			while(node != None):
				if(self.compare(node.point, point)): break

				node = node.sibling

			if(node == None):
				# 定石を外れている
				print("node == None")
				return puttable


		# 履歴と定石の終わりが一致していた場合
		if(node.child == None): 
			return puttable

		next_move = self.get_next_move(node)

		# 座標を元の形に変換する
		next_move = transformer.denormalize(next_move)

		moves = []
		value = [next_move.x ,next_move.y]
		moves.append(value)

		return moves


	def get_next_move(self, node):
		p = node.child
		candidates = []

		while(p != None):
			candidates.append(p.point)
			p = p.sibling

		index = int(rand() % len(candidates))
		return candidates[index]


	def add(self, book):
		node = self.Root

		for i in range(len(book)):
			p = book[i]

			if(node.child == None):
				# 新しい定石手
				node.child = sm.Node()
				node = node.child
				node.point.x = p.x
				node.point.y = p.y
			else:
				# 兄弟ノードの探索に移る
				node = node.child

				while(True):
					# 既にこの手はデータベース中にあり、その枝を見つけた
					if(node.point == p): break

					# 定石木の新しい枝
					if(node.sibling == None):
						node.sibling = sm.Node()

						node = node.sibling
						node.point.x = p.x
						node.point.y = p.y
						break

					node = node.sibling



















