Blockade
==========
This is another game made for the Game Design class I took.

This game is a turn based strategy game, that's essentially a board game. The game logic is not implemented in the game, but if you are playing with another player, you can still play by the rules.

Installation
------------

1. Clone this repo.
2. Run python game.py. This program is compiled with Python2.7 and PySFML, so you'll need to get those as dependencies.

Rules
--------
1. This is a two player game. The player on the left is trying to move the blue circle into the blue spaces, and the player on the right is trying to move the red circle into the red spaces.
2. On each turn, a player must either move their circle by one space (up, down, left, right) or place a blockade on the grid.
3. Neither player may pass through a blockade, whether it was placed by them or their opponent.
4. You may not move blockades that have already been placed.
5. You may not build a wall with blockades. This means that both players must always have a path to their goal, that is not fully closed off by blockades.
6. When a player can make no more moves, he loses.

Configuration
-------------

You can edit constants.py to change around the dimensions of the board. The rendering code isn't the cleanest so you might need to tweak some of it to correctly show the game.
