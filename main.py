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
algo = "SARSA"


SfemaleAgent = agent(2, 0, 0, Qtable(
    learningRate, discountRate), testWorld, algo)
SmaleAgent = agent(2, 4, 0, Qtable(
    learningRate, discountRate), testWorld, algo)
SfemaleAgent.pairAgent(SmaleAgent)


femaleAgent = agent(2, 0, 0, Qtable(
    learningRate, discountRate), testWorld, algo)
maleAgent = agent(2, 4, 0, Qtable(
    learningRate, discountRate), testWorld, algo)
femaleAgent.pairAgent(maleAgent)

terminalStates = 0
turns = 0
policy = "PR"

fmoves = SfemaleAgent.aplop()
fchosenMove = chooseMove(fmoves, SfemaleAgent.getQVals(), policy)

mmoves = SmaleAgent.aplop()
mchosenMove = chooseMove(mmoves, SmaleAgent.getQVals(), policy)

drops = 0
done = 0
for i in range(8000):
    if i == 500:
        policy = "PE"
    if testWorld.world[2][2] > 5:
        print(fchosenMove2)
        print(mchosenMove2)
        break

    foldstate = SfemaleAgent.getState()
    SfemaleAgent.move(fchosenMove)

    moldstate = SmaleAgent.getState()
    SmaleAgent.move(mchosenMove)

    fmoves = SfemaleAgent.aplop()
    fchosenMove2 = chooseMove(fmoves, SfemaleAgent.getQVals(), policy)
    qtable = SfemaleAgent.sarsa(foldstate, fchosenMove, fchosenMove2)
    fchosenMove = fchosenMove2

    mmoves = SmaleAgent.aplop()
    qval = SmaleAgent.getQVals()
    mchosenMove2 = chooseMove(mmoves, SmaleAgent.getQVals(), policy)
    qtable = SmaleAgent.sarsa(moldstate, mchosenMove, mchosenMove2)
    mchosenMove = mchosenMove2

    # moves = SfemaleAgent.aplop()
    # chosenMove = chooseMove(moves, SfemaleAgent.getQVals(), policy)
    # qtable = SfemaleAgent.move(chosenMove)
    # moves = SmaleAgent.aplop()
    # chosenMove = chooseMove(moves, SmaleAgent.getQVals(), policy)
    # qtable = SmaleAgent.move(chosenMove)

    turns += 1
    if(testWorld.isTerminal()):
        terminalStates += 1
        testWorld.reset(init_blocks)
        SfemaleAgent.reset(2, 0)
        SmaleAgent.reset(2, 4)
        print(turns)
        turns = 0
        fmoves = SfemaleAgent.aplop()
        fchosenMove = chooseMove(fmoves, SfemaleAgent.getQVals(), policy)
        mmoves = SmaleAgent.aplop()
        mchosenMove = chooseMove(mmoves, SmaleAgent.getQVals(), policy)

    # if i == 500:
    #     policy = "PG"
    # moves = femaleAgent.aplop()
    # chosenMove = chooseMove(moves, femaleAgent.getQVals(), policy)
    # qtable = femaleAgent.move(chosenMove)
    # moves = maleAgent.aplop()
    # chosenMove = chooseMove(moves, maleAgent.getQVals(), policy)
    # qtable = maleAgent.move(chosenMove)
    # if(testWorld.isTerminal()):
    #     terminalStates += 1
    #     testWorld.reset(init_blocks)
    #     femaleAgent.reset(2, 0)
    #     maleAgent.reset(2, 4)
print(turns)
print("Terminal States Reached: ", terminalStates)
