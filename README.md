# Checkers AI

A Checkers game with an AI opponent, built using Python and Pygame. Features an AI with minimax and alpha-beta pruning, warp zones that grant bonus moves and prevent captures, a 5-second turn timer, and a random one-time multi-jump ability for both player and AI.

## Features
- AI opponent using minimax with alpha-beta pruning.
- Warp zones (center squares) that grant bonus moves and prevent captures.
- 5-second turn timer with a yellow timer display on a pink background.
- Random one-time multi-jump ability for both player and AI.
- Visual feedback with Pygame, including messages for game events.

## Installation
1. Clone the repository: `git clone <repository-url>`
2. Install Python 3.x and Pygame: `pip install pygame`
3. Run the game: `python main.py`

## How to Play
- White pieces (player) move first.
- Move pieces by clicking to select and then clicking a valid destination.
- Warp zones are the center squares (4,4), (4,5), (5,4), (5,5).
- You have 5 seconds per turn, or the turn switches.
- Multi-jumps are randomly enabled once per game for each side.

