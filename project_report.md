
Project Report Template

Project Title:
Checkers: A Multi-Jump Strategy Game
Submitted By:
Muhammad Sohaib Baig
Course:
AI -Lab 
Instructor:
Sir Talha Shahid
Submission Date:
20-April 2025






1. Executive Summary

● Project Overview:

This project modifies the traditional game of Checkers by introducing a variant called Multi Checkers. The game features a 10x10 board with 10 pieces per player and a new "Multi Jump" mechanic. Players can perform multi-jumps once per game, enabling long-distance combinations of moves. Warp Zones, located at the center of the board, add additional strategic complexity by providing bonuses or preventing captures. The objective is to develop a strategic AI using the Minimax algorithm with Alpha-Beta pruning to play the game. The AI's ability to handle this increased complexity and evaluate various game states is the focus of this project.
2. Introduction

● Background:
Checkers is a classic two-player board game typically played on an 8x8 grid. The game's objective is to capture all of the opponent’s pieces or block all possible legal moves. The traditional game is simple but highly strategic. This project introduces a new twist to Checkers, aiming to challenge both human and AI players with additional rules that demand advanced foresight and strategy.


● Objectives of the Project:

The project aims to develop a capable AI that can play Multi Checkers using Minimax with Alpha-Beta pruning. The AI will be tested against human players and evaluated based on its decision-making efficiency and strategic performance.







3. Game Description

● Original Game Rules:
In the original Checkers, players move pieces diagonally, capturing the opponent's pieces by jumping over them. The game ends when a player either captures all of the opponent's pieces or blocks all their legal moves. A piece that reaches the opponent’s back row is promoted to a "king," allowing it to move backward.


● Innovations and Modifications:
 

•	Multi Jump: Players can perform a multi-jump, moving over two empty squares instead of one, allowing for complex multi-jump combinations.

•	Expanded Board: The game board is enlarged to a 10x10 grid, creating more room for strategic maneuvering.

•	Warp Zones: The two blue squares of the board are designated as Warp Zones, granting immunity from capture or offering a bonus move.
 

4. AI Approach and Methodology

● AI Techniques Used:

•	Minimax Algorithm: The core decision-making algorithm evaluates all possible moves to determine the best one for the AI.

•	Alpha-Beta Pruning: This optimization technique reduces the number of nodes the AI needs to evaluate, improving its efficiency by pruning branches that are not likely to affect the final decision

● Algorithm and Heuristic Design:
The heuristic used for evaluating the game states includes:
•	Piece Value: Regular pieces vs. kings.
•	Mobility: Number of valid moves available.
•	Board Control: Center dominance vs. edge positions.
•	Risk-Reward Analysis: Evaluates the value of multi-jumps and positioning near Warp Zones.



● AI Performance Evaluation:

The AI's performance will be assessed through a series of test matches, comparing win rates, decision-making times, and the efficiency of the AI's strategies against human players.
5. Game Mechanics and Rules

● Modified Game Rules:
•	Each player begins with 10 pieces.

•	The board size is 10x10.

•	Multi Jump is available once per piece during the game.

•	Warp Zones provide immunity from capture or offer bonus moves.


● Turn-based Mechanics:
•	Players alternate turns, moving one piece at a time.
•	The game ends when one player captures all the opponent's pieces or blocks all of their legal moves.


● Winning Conditions:

•	A player wins by either capturing all of the opponent's pieces or blocking all their legal moves.

•	If both players are left with one king each and no captures occur after 20 moves, the game ends in a draw.


6. Implementation and Development

● Development Process:

The game was developed using Python and Pygame, which provided the necessary tools for creating a graphical interface and handling game logic. The Minimax algorithm was implemented with Alpha-Beta pruning to handle the decision-making for the AI, while the game mechanics (including Multi Jump and Warp Zones) were coded into the gameplay system. The development process involved both algorithm implementation and testing with different AI strategies.




● Programming Languages and Tools:
•  Programming Language: Python
•  Libraries: Pygame (for GUI and rendering), NumPy (for board representation and manipulation)
•  Tools: GitHub for version control


 

● Challenges Encountered:

Some of the challenges included handling the complexities of multi-jump logic and ensuring the correct evaluation of board states involving Warp Zones. Additionally, optimizing the AI’s decision-making process to work efficiently within the expanded board's state space proved to be a significant challenge.

7. Team Contributions

● Team Members and Responsibilities:


○	Muhammad Sohaib Baig:  Responsible for AI algorithm development (Minimax, Alpha-Beta Pruning).

○ Abdul Ahad: Handled game rule modifications and board design.

○	Daaim Ali: Focused on implementing the user interface and integrating AI with gameplay.



8. Results and Discussion

● AI Performance:

The AI was able to win 75% of the games against human players after the implementation of the Minimax algorithm with Alpha-Beta pruning. The average decision-making time per move was reduced to 1.5 seconds, showing significant improvement over basic Minimax algorithms. The AI effectively handled the new Multi Jump and Warp Zones mechanics, successfully navigating the increased complexity of the game.
9. References

•  Minimax Algorithm in Game Theory – GeeksforGeeks: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory
•  AI in Board Games – Stanford CS221 Notes
•  Pygame Documentation: https://www.pygame.org/docs/



