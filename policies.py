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
        return random.choice(validMoves)


def PExploit(validMoves, qVal):
    pick_up = 'P' in validMoves
    drop_off = 'D' in validMoves
    chance = .2
    if pick_up == True:
        return 'P'
    elif drop_off == True:
        return 'D'
    else:
        d = {k: qVal[k] for k in validMoves}
        maxVal = max(d.values())
        maxMoves = list()
        for key, value in d.items():
            if value == maxVal:
                maxMoves.append(key)
        minMoves = list(set(validMoves) - set(maxMoves))
        if random.random() < chance:
            return random.choice(minMoves)
        else:
            return random.choice(maxMoves)


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
        maxMoves = list()
        for key, value in d.items():
            if value == maxVal:
                maxMoves.append(key)
        return random.choice(maxMoves)
