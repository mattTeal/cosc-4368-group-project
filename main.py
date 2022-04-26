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

qtable = Qtable(learningRate, discountRate)
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

steps = []
for i in range(8000):
    if i == 500:
        policy = "PE"

    foldstate = SfemaleAgent.getState()
    SfemaleAgent.move(fchosenMove)

    moldstate = SmaleAgent.getState()
    SmaleAgent.move(mchosenMove)

    fmoves = SfemaleAgent.aplop()
    fchosenMove2 = chooseMove(fmoves, SfemaleAgent.getQVals(), policy)
    moveback = ''
    if fchosenMove2 == 'N':
        moveback = 'S'
    elif fchosenMove2 == 'S':
        moveback = 'N'
    elif fchosenMove2 == 'E':
        moveback = 'W'
    elif fchosenMove2 == 'W':
        moveback = 'E'
    elif fchosenMove2 == 'P':
        moveback = 'D'
    elif fchosenMove2 == 'D':
        moveback = 'P'
    qtable = SfemaleAgent.sarsa(foldstate, fchosenMove, fchosenMove2)
    fchosenMove = fchosenMove2
    SfemaleAgent.move(fchosenMove2)

    mmoves = SmaleAgent.aplop()
    qval = SmaleAgent.getQVals()
    mchosenMove2 = chooseMove(mmoves, SmaleAgent.getQVals(), policy)
    qtable = SmaleAgent.sarsa(moldstate, mchosenMove, mchosenMove2)
    mchosenMove = mchosenMove2

    SfemaleAgent.move(moveback)

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
        steps.append(turns)
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
print("Terminal States Reached: ", terminalStates)
total = 0
min = steps[0]
for i in steps:
    total += i
    if i < min:
        min = i
average = total/terminalStates
print(average)
print(min)
