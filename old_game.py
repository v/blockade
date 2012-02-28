# Include the PySFML extension
from PySFML import sf
import math
import pymunk as pm

constants = {
		'box_width': 60,
		'box_height': 60,
		'circle_radius': 25,
		'x_boxes': 7,
		'y_boxes': 7,
		'win_width': 1024,
		'win_height': 768
}



# Create the main window
window = sf.RenderWindow(sf.VideoMode(constants['win_width'], constants['win_height']), "PySFML test")
InputHandler = window.GetInput()

# Create a graphical string to display
text = sf.String("Blockade")

white = sf.Color(255, 255, 255)
black = sf.Color(0, 0, 0)
red = sf.Color(255, 25, 25)
blue = sf.Color(25, 25, 255)

grid = []
for i in range(constants['x_boxes']):
	grid.append([])
	for j in range(constants['y_boxes']):
		grid[i].append(None)

def draw_box(window, x, y, color):
	width = constants['box_width']
	height = constants['box_height']
	window.Draw(sf.Shape.Rectangle(x, y, x+width, y+height, black, 1, color))

def draw_grid(window):
	center = (constants['win_width']/2, constants['win_height']/2)
	startx = center[0] - constants['x_boxes']*constants['box_width']/2
	starty = center[1] - constants['y_boxes']*constants['box_height']/2
	for i in range(constants['x_boxes']):
		color = white
		if i == 0:
			color = red
		if i == constants['x_boxes'] - 1:
			color = blue

		for j in range(constants['y_boxes']):

			draw_box(window, startx + i * constants['box_width'], starty + j * constants['box_height'], color=color)

""" Returns left/top by default, center if you specify center=True"""
def compute_pos(x, y, center=False):
	center = (constants['win_width']/2, constants['win_height']/2)
	startx = center[0] - constants['x_boxes']*constants['box_width']/2
	starty = center[1] - constants['y_boxes']*constants['box_height']/2

	if center:
		startx += constants['box_width']/2
		starty += constants['box_height']/2

	return (startx+x * constants['box_width'], starty + y*constants['box_height'])


class DraggableCircle:
	def __init__(self, color):
		self.shape =  sf.Shape.Circle(0, 0, constants['circle_radius'], color)
		self.dragged = False
		self.color = color
		self.type = "circle"

		self.grid_pos = [-1, -1]

	def update(self):
		if self.grid_pos[0] >= 0 and self.grid_pos[1] >= 0:
			pos = compute_pos(*self.grid_pos, center=True)
			self.shape.SetPosition(pos[0], pos[1])
		if self.dragged:
			self.shape.SetPosition(*window.ConvertCoords(InputHandler.GetMouseX(), InputHandler.GetMouseY()))

	def center(self):
		return self.shape.GetPosition()
	
	def set_center(self, x, y):
		self.shape.SetPosition(x, y)

	def mouse_over(self):
		x, y = self.center()

		mx = InputHandler.GetMouseX()
		my = InputHandler.GetMouseY()

		mx, my = window.ConvertCoords(mx, my)

		return math.sqrt((mx - x) ** 2 + (my - y) ** 2) < constants['circle_radius']

class DraggableRect:
	def __init__(self, color):
		self.color = color
		self.dragged = False
		self.shape = sf.Shape.Rectangle(0, 0, constants['box_width'], constants['box_height'], color)
		self.type = 'rect'
		self.grid_pos = [-1, -1]

	def update(self):
		if self.grid_pos[0] >= 0 and self.grid_pos[1] >= 0:
			pos = compute_pos(*self.grid_pos, center=True)
			self.set_center(pos[0], pos[1])
		if self.dragged:
			self.shape.SetPosition(*window.ConvertCoords(InputHandler.GetMouseX(), InputHandler.GetMouseY()))
			self.shape.Move(-constants['box_width']/2, -constants['box_height']/2)

	def center(self):
		x, y = self.shape.GetPosition()
		x += constants['box_width']/2
		y += constants['box_height']/2

		return (x, y)

	def set_center(self, x, y):
		self.shape.SetPosition(x, y)
		self.shape.Move(-constants['box_width']/2, -constants['box_height']/2)

	def mouse_over(self):
		x, y = self.shape.GetPosition()
		x, y = int(x), int(y)

		rect = sf.IntRect(x, y, x + constants['box_width'], y + constants['box_height'])

		mx = InputHandler.GetMouseX()
		my = InputHandler.GetMouseY()

		mx, my = window.ConvertCoords(mx, my)

		return rect.Contains(mx, my)

def get_closest_grid_point(draggable):
	for i in range(constants['x_boxes']):
		for j in range(constants['y_boxes']):
			pos = compute_pos(i, j, False)

			# This represents the grid.
			rectangle = sf.IntRect(pos[0], pos[1], pos[0] + constants['box_width'], pos[1] + constants['box_height'])

			if rectangle.Contains(*draggable.center()):
				return (i, j)
	return None


# Start the game loop

blue_circle = DraggableCircle(blue)
blue_circle.set_center(150, constants['win_height']/2 - 50)
blue_circle.init_position = blue_circle.center()

red_circle = DraggableCircle(red)
red_circle.set_center(constants['win_width'] - 150, constants['win_height']/2 - 50)
red_circle.init_position = red_circle.center()

wall = DraggableRect(white)
wall.set_center(constants['win_width'] - 150, constants['win_height'] / 2 + 50)
wall.init_position = wall.center()

other_wall = DraggableRect(white)
other_wall.set_center(150, constants['win_height'] / 2 + 50)
other_wall.init_position = other_wall.center()

controls = [red_circle, blue_circle, wall, other_wall]
running = True

dudes = []

red_blockades = 0
blue_blockades = 0

while running:
	event = sf.Event()
	while window.GetEvent(event):
		if event.Type == sf.Event.Closed:
			running = False
		if event.Type == sf.Event.MouseButtonPressed:
			if event.MouseButton.Button == 0:
				for c in controls:
					if c.mouse_over():
						c.dragged = True

				for d in dudes:
					if d.mouse_over():
						d.dragged = True
			else:
				for d in dudes:
					if d.mouse_over():
						dudes.remove(d)
						grid[d.grid_pos[0]][d.grid_pos[1]] = None

		if event.Type == sf.Event.MouseButtonReleased:
			for c in controls:
				if c.dragged:
					closest_point = get_closest_grid_point(c)
					if closest_point and not grid[closest_point[0]][closest_point[1]]:
						clone = None
						if c.type == 'rect':
							if c.init_position[0] < constants['win_width']/2:
								blue_blockades += 1
							else:
								red_blockades += 1
							clone = DraggableRect(white)
						elif c.type == 'circle':
							clone = DraggableCircle(c.color)
						clone.grid_pos = closest_point
						grid[closest_point[0]][closest_point[1]] = clone
						clone.update()
						clone.init_position = clone.center()
						dudes.append(clone)

					c.set_center(*c.init_position)

					c.dragged = False

			for d in dudes:
				if d.dragged:
					d.dragged = False
					closest_point = get_closest_grid_point(d)
					if closest_point and not grid[closest_point[0]][closest_point[1]]:
						grid[d.grid_pos[0]][d.grid_pos[1]] = None
						d.grid_pos = closest_point
						grid[closest_point[0]][closest_point[1]] = d
						d.update()
						d.init_position = d.center()

					else:
						d.set_center(*d.init_position)


	# Clear screen, draw the text, and update the window
	window.Clear()
	draw_grid(window)
	red_blockade_text = sf.String("Blue Blockades %s " % (blue_blockades))
	red_blockade_text.Move(0, 700)
	blue_blockade_text = sf.String("Red Blockades %s " % (red_blockades))
	blue_blockade_text.Move(750, 700)
	window.Draw(red_blockade_text)
	window.Draw(blue_blockade_text)
	window.Draw(text)

	for c in controls:
		c.update()
		window.Draw(c.shape)

	for d in dudes:
		d.update()
		window.Draw(d.shape)

	window.Display()
