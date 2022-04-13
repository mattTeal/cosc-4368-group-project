import random


def PRandom(validMoves):
    pick_up = 'P' in validMoves
    drop_off = 'D' in validMoves

    if pick_up == True:
        return 'P'
    elif drop_off == True:
        return 'D'
    else:
        return random.choice(tuple(validMoves))


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
        ran = random.random()
        if ran < chance:
            if len(minMoves) != 0:
                return random.choice(tuple(minMoves))
            return random.choice(tuple(maxMoves))
        else:
            return random.choice(tuple(maxMoves))


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
