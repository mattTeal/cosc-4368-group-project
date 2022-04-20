from dataclasses import make_dataclass
from world import world
from qtable import Qtable
from agent import agent
from policies import *

pickups = [(4, 2), (1, 3)]
dropoffs = [(0, 0), (4, 0), (2, 2), (4, 4)]
init_blocks = 10
learningRate = 0.3
discountRate = 0.5
testWorld = world(pickups, dropoffs, init_blocks)

femaleAgent = agent(2, 0, 0, Qtable(
    learningRate, discountRate), testWorld, "QLearn")
maleAgent = agent(2, 4, 0, Qtable(
    learningRate, discountRate), testWorld, "QLearn")

femaleAgent.pairAgent(maleAgent)

terminalStates = 0

for i in range(8000):
    moves = femaleAgent.aplop()
    chosenMove = chooseMove(moves, femaleAgent.getQVals(), "PR")
    qtable = femaleAgent.move(chosenMove)
    moves = maleAgent.aplop()
    chosenMove = chooseMove(moves, maleAgent.getQVals(), "PR")
    qtable = maleAgent.move(chosenMove)
    if(testWorld.isTerminal()):
        terminalStates += 1
        testWorld.reset(init_blocks)
        femaleAgent.reset(2, 0)
        maleAgent.reset(2, 4)

print("Terminal States Reached: ", terminalStates)
