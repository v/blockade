from board import Board
from token import Token
from constants import * 
from PySFML import sf
import math, os, sys

window = sf.RenderWindow(sf.VideoMode(win_width, win_height), "Blackode")
InputHandler = window.GetInput()


bcircle = Token('circle', blue)
bcircle.set_center(150, win_height/2)
rcircle = Token('circle', red)
rcircle.set_center(win_width - 150, win_height/2)

b = Board(bcircle, rcircle)
running = True

tokens = []

lx = 250
rx = win_width - lx

for i in range(num_cols - 1):
	y = 100 + (i * box_height * 2)	

	token = Token('rect', blue)
	token.shape.SetPosition(lx , y)

	tokens.append(token)
	
	token = Token('rect', red)
	token.shape.SetPosition(rx, y)

	tokens.append(token)

tokens.append(bcircle)
tokens.append(rcircle)


valid_paths = None

while running:
	event = sf.Event()
	while window.GetEvent(event):
		if event.Type == sf.Event.Closed:
			running = False
		if event.Type == sf.Event.MouseButtonPressed:
			for token in tokens:				
				if token.mouse_over(InputHandler, window):
					token.dragged = True
					if token.i >= 0 and token.j >= 0:
						b.grid[token.i][token.j] = None

					if token.type == 'rect':
						b.invalid = b.find_critical_nodes(valid_paths)
						print b.invalid
		if event.Type == sf.Event.MouseButtonReleased:
			for token in tokens:
				if token.dragged:
					token.dragged = False
					b.snap(window, token)
					b.invalid = set()
					valid_paths =  b.get_valid_paths()
	window.Clear()
	b.draw(window)
	for t in tokens:
		t.update(InputHandler, window)
		t.draw(window)
	window.Display()
