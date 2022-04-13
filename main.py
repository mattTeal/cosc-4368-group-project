from world import world
from qtable import Qtable
from policies import *

# This is the current state and mock new state for a single agent for testing
# Using reduced [i, j, x, i1, j1, s, t, u, v] state space for each agent
currentState = [0, 0, 1, 0, 1, 1, 1, 1, 1]
newState = [0, 0, 0, 0, 0, 1, 1, 1, 1]

# testing a state that doesnt have drop/pickup
testState = [1, 1, 0, 3, 3, 1, 1, 1, 1]

# Define pickup and drop off locations. Converted from given to zero indexed
# This is so experiment 4 is easier
pickups = [(2, 4), (3, 1)]
dropoffs = [(0, 0), (0, 4), (2, 2), (4, 4)]
# In the event that we need to change number of blocks each pickup starts with
init_blocks = 10

# create an instance of the world with cdropoffs and pickups
testWorld = world(pickups, dropoffs, init_blocks)
# create an instance of qTable
testTable = Qtable(0.3, 0.5)

# Changed aplop to work universally for both agents
moves = testWorld.aplop(currentState)
newMoves = testWorld.aplop(newState)

testMoves = testWorld.aplop(testState)
print("Available moves for one agent:", moves)
# Pick a random move from applicable to test
qVal = testTable.getQVal(testState)
chosenMove = PExploit(testMoves, qVal)

# Perform Qlearning update
# testTable.QUpdate(currentState, newState, chosenMove, newMoves)
# print("Updated qtable for action ", chosenMove,
#       ":", testTable.getQVal(currentState))

# Perform SARSA update
testTable.SARSA(currentState, newState, chosenMove)
print("Updated qtable for action ", chosenMove,
      ":", testTable.getQVal(currentState))

# Starting locations
male_agent_location = [4, 2]
female_agent_location = [0, 2]
""" 
print(valid_actions.aplop(4, 0, 0, 0, 0, 0, 1, 1, 1, 1, pickups, dropoffs))
 """
