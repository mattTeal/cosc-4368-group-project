import itertools
from qtable import Qtable
import numpy as np
import random
import itertools


def PRandom(validMoves):
    pick_up = 'P' in validMoves
    drop_off = 'D' in validMoves

    if pick_up == True:
        return 'P'
    elif drop_off == True:
        return 'D'
    else:
        return random.choice(tuple(validMoves))


def PGreedy(validMoves, qVal):
    pick_up = 'P' in validMoves
    drop_off = 'D' in validMoves

    if pick_up == True:
        return 'P'
    elif drop_off == True:
        return 'D'
    else:
        d = {k: qVal[k] for k in validMoves}
        maxVal = max(d.values())
        listOfDir = list()
        for key, value in d.items():
            if value == maxVal:
                listOfDir.append(key)
        return random.choice(tuple(listOfDir))
