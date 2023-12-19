# cribbage_solver
A solver for cribbage using monte-carlo tree search and complete state representation

# How to Run:
1. Download the zip file
2. Extract the zip to preferred location
3. From command line run: python main.py {player1} {player}
4. There are three types of players to choose from: human, ai, and random
   1. Human requires input from the user.
   2. AI runs the created MCTS program
   3. Random runs a random player
5. Example command line: python main.py ai random


# Acknowledgements:
The main code for this program was retrieved from https://github.com/dacarlin/cribbage
The code contained in card.py, game.py, players.py, and score.py are from this module. 
My contribution is parts of main.py and all of MonteCarloPlayer.py.
players.py also contains some more complex ai models, details of which can be found in the main repo.
Big thanks to dacarlin for the python cribbage game template.
