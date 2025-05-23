# Chinese Checkers 

This project is an implementation of Chinese Checkers, a strategy board game, developed using Python and Pygame. The game allows you to play either solo against the Computer or with friends in a multi-player setup. It includes a user-friendly graphical interface and advanced features like game saving and loading.

## Features:

* Graphical User Interface (GUI) using Pygame for intuitive and interactive gameplay.
* Suitable for 2-6 players, with two game modes: Human vs Human and Human vs Computer.
* Save and load functionality:
  Save your current game state at any time.
  Load a previously saved game and resume exactly where you left off.
* Move highlighting:
  Shows available moves for selected pieces.
  Supports multiple jumps, following standard Chinese Checkers rules.
* Turn-based system: Automatic switching between players (human or computer).
* Victory detection: The game recognizes when a player has moved all their pieces to the opposite corner.

## Code Quality Enhancements:
* Type annotations across the codebase
* Modular design with separation of game logic and rendering

## Setup:
### Install dependencies:
Before running the game, make sure to install the required dependencies:
<pre>pip install -r requirements.txt</pre>
### Running the Game:
To start the game, simply run:
<pre>python main.py</pre>
You can also pass the --help flag to see the game rules and usage:
<pre>python main.py --help</pre>

## Usage:
When the game starts, you’ll be able to:
* Start a new game: Play a fresh game.
* Load a saved game: Continue from a previously saved game.
* Provide the number of players and their names via the input prompts.
* The Pygame window will launch automatically and gameplay will begin.
* Use the mouse to select a marble and then a valid cell to move it.
* After the game ends, choose whether to restart or exit.

## Rules:
The game is played on a star-shaped board with 121 spaces.
You can play with 2, 3, 4, or 6 players. Each player starts with 10 pieces placed in one of the corners of the star.
Objective: The goal is to move all your pieces to the opposite corner of the board. The first player to do so wins the game.
Movement: On each turn, a player can:
Move a piece to an adjacent space.
Jump over another piece if there is an empty space directly after it.
The game ends when one player has successfully moved all their pieces to the opposite corner of the board.
