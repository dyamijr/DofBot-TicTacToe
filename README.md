# DofBot-TicTacToe

### Members:

Arslan Lau\
Dyami Watson Jr\
Hengrui Pei\
Sidy Thiam 

### Summary

Tic-Tac-Toe is a game on a 3x3 board in which each player is assigned to either an X or an O block. The
player that goes first must place their block on the board and each player takes turns placing blocks in
open spaces. The game's goal is for a player to get three of their blocks placed in a row (horizontal,
vertical, or diagonal). If all blocks are placed on the board and no player has one the game is called a tie.
This project will implement a system that enables the Dofbot arm to play a game of Tic-Tac-Toe against a
human opponent on a physical board using blocks labeled with either an X or an O.

### Background/Motivation

We chose this particular task because it combines skills from a variety of disciplines: Artificial
intelligence (for determining optimal moves), computer vision (for interpreting game state), and inverse
kinematics (for moving the arm towards a desired location). We believe that implementing Tic-Tac-Toe
on a Dofbot arm involves key robotics concepts:
1. Inverse Kinematics and Motion Planning: The robot calculates joint angles to reach each grid position, using recent advancements in inverse kinematics and motion planning to improve precision and efficiency.
2. Object Manipulation and Gripping: The Dofbot needs to pick up and place markers (X or O), which adds to the challenge of precision handling and actuation.
3. Human-Robot Interaction: This task provides insights into developing intuitive interactions, enabling the robot to respond accurately to human moves and engage in a turn-based game environment.

Programming a robot arm to play Tic-Tac-Toe offers a practical way to explore robotic control, inverse
kinematics, and human-robot interaction. This project demonstrates the arm’s ability to perform precise
movements in response to game logic, while also creating an engaging, hands-on application for learning
essential robotics skills.

### Goals

#### Baseline:

1. The robot arm can pick and place blocks in valid locations on the board
2. The robot will only pick up blocks corresponding to its “team” (If the robot is X’s it will only
    pick up X blocks)
3. The robot will be able to accurately read and reproduce the board state to the user^1. This includes
    the number of blocks placed, their location, which block should be placed next, and if the game
    has a winner.
4. The robot will complete a full game of Tic Tac Toe, resulting in a win, loss, or draw.

#### Target:

1. The robot will minimize losing and recognize winning moves
2. The robot will make its move after being triggered to do so by the user.
3. The system will output the result of the game to the user (Win, Loss, Draw)
4. Track statistics from a game session such as the number of user's wins, losses, and draws.

#### Reach:

1. After completion of the game, the robot will clear the board resetting to the beginning position
2. The robot will automatically begin its move after completion of the human player's turn
3. Implement reinforcement learning algorithm to learn from user's behavior and improve
    performance
4. Allow a user slider to adjust the difficulty of the game to add variety to the user experience.

### Approach

1. Board detection: we will use OpenCV^1 to read the game state from the physical board and
    transform it into an abstract representation for ease of manipulation.
2. Core algorithm: we will use the minimax algorithm^2 to choose the most optimal moves for the
    arm to make against its opponent.
3. Placing blocks: we will transform an abstract description of a move into task space, and
    determine the appropriate joint angles to pick up the needed blocks and place them on the board^3.

<sup>1</sup>Garrido, Sergio, and Alexander Panov. “Board Detection.” OpenCV,
docs.opencv.org/4.x/db/da9/tutorial_aruco_board_detection.html. Accessed 30 Oct. 2024.\
<sup>2</sup>Shahd H. Alkaraz, Essam El-Seidy, Neveen S. Morcos, Tic-Tac-Toe: Understanding the Minimax
Algorithm, Journal of Game Theory, Vol. 9 No. 1, 2020, pp. 1-7. doi: 10.5923/j.jgt.20200901.01.\
<sup>3</sup>Kim, Y., Kim, J., & Park, J. (2020). _Real-Time Inverse Kinematics for Redundant Robots Using Improved
Optimization Methods_. IEEE Robotics and Automation Letters, 5(4), 5889-5896.
