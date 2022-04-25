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
testQTable = Qtable(learningRate, discountRate)
femaleAgent = agent(2, 0, 0, testQTable, testWorld, "QLearn")
maleAgent = agent(2, 4, 0, testQTable, testWorld, "QLearn")

femaleAgent.pairAgent(maleAgent)

terminalStates = 0

#called before moving
i, j, x, i2, j2, s, t, u, v = femaleAgent.getState()

moves = femaleAgent.aplop()
chosenMove = chooseMove(moves, femaleAgent.getQVals(), "PE")
femaleQTable = femaleAgent.move(chosenMove)
moves = maleAgent.aplop()
chosenMove = chooseMove(moves, maleAgent.getQVals(), "PE")
maleQTable = maleAgent.move(chosenMove)
# compare states after moving
print(femaleAgent.qTable[i][j][x][i2][j2][s][t][u][v].actions)
print(maleAgent.qTable[i][j][x][i2][j2][s][t][u][v].actions)
