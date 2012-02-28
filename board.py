from constants import *
from PySFML import sf
class Board:
	def __init__(self, blue, red):
		self.grid = []
		self.blue = blue
		self.red = red
		self.invalid = set()
		for i in range(num_rows):
			self.grid.append([])
			for j in range(num_cols):
				self.grid[i].append(None)

	def draw(self, window):
		startx = win_width/2
		starty = win_height/2
		startx, starty = window.ConvertCoords(startx, starty)
		startx -= num_cols * box_width/2
		starty -= num_rows * box_height/2

		startx, starty = (400, 200)
		for i, row in enumerate(self.grid):
			y = starty  + (i * box_height)
			for j, square in enumerate(row):
				x = startx + (j * box_width)
				color = sf.Color(255, 255, 255)
				if j == 0:
					color = red
				elif j == num_cols - 1:
					color = blue

				bg_color = sf.Color(0, 0, 0)
				if (i, j) in self.invalid:
					bg_color = sf.Color(150, 25, 25)
				
				box = sf.Shape.Rectangle(x, y, x + box_width, y + box_height, bg_color, 1, color)

				window.Draw(box)

				if self.grid[i][j]:
					self.grid[i][j].draw(window, x, y)

	def snap(self, window, token):
		startx = win_width/2
		starty = win_height/2
		startx, starty = window.ConvertCoords(startx, starty)
		startx -= num_cols * box_width/2
		starty -= num_rows * box_height/2

		cx, cy = token.get_center()
		cx, cy = int(cx), int(cy)


		startx, starty = (400, 200)
		for i, row in enumerate(self.grid):
			y = starty  + (i * box_height)
			for j, square in enumerate(row):
				x = startx + (j * box_width)

				rect = sf.IntRect(x, y, x + box_width, y + box_height)
				if not self.grid[i][j] and rect.Contains(cx, cy):
					self.grid[i][j] = token
					token.i = i
					token.j = j

					return


	def is_end_point(self, node, color):
		if color == 'blue' and node[1] == num_cols - 1:
			return True
		if color == 'red' and node[1] == 0:
			return True
		return False

	def neighbors(self, root):
		right = (root[0] + 1, root[1])	
		left = (root[0] - 1, root[1])	
		top = (root[0], root[1] + 1)	
		bottom = (root[0], root[1] - 1)	

		neighbors = []
		for node in  (right, left, top, bottom):
			if node[0] >= 0 and node[1] >= 0 and node[0] <= num_cols - 1 and node[1] <= num_cols - 1 and (not self.grid[node[0]][node[1]] or self.grid[node[0]][node[1]].type != 'rect'):
				neighbors.append(node)

		return neighbors

	def find_paths(self, path, color):
		paths = []
		if self.is_end_point(path[-1], color):
			return path

		for node in self.neighbors(path[-1]):
			if not node in path:
				path.append(node)
				paths += self.find_paths(path, color)

		return paths

	def get_valid_paths(self):
		paths = []	

		start = (self.red.i, self.red.j)

		return self.find_paths([start], 'red')

	def find_critical_nodes(self, paths):
		if not paths:
			return set()
		result = set(paths[0])
		for path in paths:
			set_path = set(path)
			result &= set_path

		return result
			
