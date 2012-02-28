from constants import *
import math

class Token:
	def __init__(self, type, color):
		self.type = type
		self.color = color
		self.dragged = False
		self.i, self.j = -1, -1
		if self.type == 'circle':
			self.shape = sf.Shape.Circle(0, 0, token_radius, color)
		elif self.type =='rect':
			self.shape = sf.Shape.Rectangle(0, 0, box_width, box_height, color)

	def draw(self, window, x=None, y=None):
		if x and y:
			self.set_center(x+box_width/2, y+box_height/2)

		window.Draw(self.shape)

	def get_center(self):
		if self.type == 'circle':
			return self.shape.GetPosition()
		elif self.type == 'rect':
			position = list(self.shape.GetPosition())
			position[0] += box_width/2
			position[1] += box_height/2

			return position
	
	def set_center(self, x, y):
		if self.type == 'circle':
			return self.shape.SetPosition(x, y)
		elif self.type == 'rect':
			x -= box_width/2
			y -= box_height/2

			return self.shape.SetPosition(x, y)


	def update(self, InputHandler, window):
		if self.dragged:
			mx, my = window.ConvertCoords(InputHandler.GetMouseX(), InputHandler.GetMouseY())
			self.set_center(mx, my)

	def mouse_over(self, InputHandler, window):
		x, y = window.ConvertCoords(InputHandler.GetMouseX(), InputHandler.GetMouseY())
		cx, cy = self.shape.GetPosition()
		if self.type == 'circle':
			return math.sqrt((cx - x)**2 + (cy - y)**2) < token_radius

		elif self.type == 'rect':
			cx, cy = self.shape.GetPosition()
			cx, cy = int(cx), int(cy)
			x, y = int(x), int(y)
			rect = sf.IntRect(cx, cy, cx + box_width, cy + box_height)

			return rect.Contains(x, y)
