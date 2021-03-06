import numpy as np

PICKUP_LOCATION_CAPACITY = 10
DROPOFF_LOCATION_CAPACITY = 5


class world:
    def __init__(self, pickups, dropoffs, init_blocks):
        # pickups and dropoffs are lists of tuple coordinates
        self.pickups = pickups
        self.dropoffs = dropoffs
        world = np.zeros((5, 5), dtype=np.int8)
        for i in pickups:
            world[i[0]][i[1]] = init_blocks
        self.world = world

    def __getitem__(self, key):
        return self.world[key]

    def __setitem__(self, key, newvalue):
        self.world[key] = newvalue

    def getWorldState(self, x):
        s, t, u, v = 0, 0, 0, 0
        if not x:
            # Pickup/dropoffs are (x, y) coordinates
            pickup_1, pickup_2 = self.pickups
            x1, y1 = pickup_1
            x2, y2 = pickup_2
            # Check if pickup locations still have blocks
            if self.world[x1][y1] > 0:
                s = 1
            if self.world[x2][y2] > 0:
                t = 1
        else:  # If agent carrying block
            dropoff_1, dropoff_2, dropoff_3, dropoff_4 = self.dropoffs
            x1, y1 = dropoff_1
            x2, y2 = dropoff_2
            x3, y3 = dropoff_3
            x4, y4 = dropoff_4
            # Check if dropoffs still have room
            if self.world[x1][y1] < DROPOFF_LOCATION_CAPACITY:
                s = 1
            if self.world[x2][y2] < DROPOFF_LOCATION_CAPACITY:
                t = 1
            if self.world[x3][y3] < DROPOFF_LOCATION_CAPACITY:
                u = 1
            if self.world[x4][y4] < DROPOFF_LOCATION_CAPACITY:
                v = 1
        return [s, t, u, v]

    # Reworked aplop to be simpler and work without needing to specify agent
    def aplop(self, agent):
        i, j, x, m, s, t, u, v = agent.getState()
        i2, j2, x2 = agent.pairedAgent.getPos()
        validMoves = []
        validDP = [s, t, u, v]
        # Agent actions
        if ((i, j) in self.dropoffs and x):  # on dropoff and isHoldingBlock
            if (validDP[self.dropoffs.index((i, j))]):
                validMoves.append('D')

        if ((i, j) in self.pickups and not x):  # on pickup and !isHoldingBlock
            if (validDP[self.pickups.index((i, j))]):
                validMoves.append('P')

        pairedAgent = (i2, j2)
        N = (i, j-1)
        E = (i+1, j)
        S = (i, j+1)
        W = (i-1, j)
        if (i > 0 and W != pairedAgent):
            validMoves.append('W')
        if (i < 4 and E != pairedAgent):
            validMoves.append('E')
        if (j > 0 and N != pairedAgent):
            validMoves.append('N')
        if (j < 4 and S != pairedAgent):
            validMoves.append('S')

        return tuple(validMoves)

    def apply(self, agent, action):
        # (i, j) - position of agent
        # x - isHoldingBlock
        # action can be N/S/E/W/P/D
        i, j, x = agent.agentState
        i_prime, j_prime, x_prime = i, j, x

        if (action == 'N'):
            j_prime -= 1
        elif action == 'S':
            j_prime += 1
        elif action == 'E':
            i_prime += 1
        elif action == 'W':
            i_prime -= 1
        elif action == 'P':
            # Pickup
            x_prime = 1
            # Block count
            self[i][j] -= 1
        elif action == 'D':
            # Dropoff
            x_prime = 0
            # Block count
            self[i][j] += 1

        s, t, u, v = self.getWorldState(x_prime)
        return [[i_prime, j_prime, x_prime], [s, t, u, v]]

    def isTerminal(self):
        for position in self.dropoffs:
            if self[position[0]][position[1]] != 5:
                return False
        return True

    def reset(self, init_blocks):
        for i in self.pickups:
            self[i[0]][i[1]] = init_blocks
        for i in self.dropoffs:
            self[i[0]][i[1]] = 0

    def changePickups(self, new_pickups):
        self.world[self.pickups[0][0]][self.pickups[0][1]] = self.world[new_pickups[0][0]][new_pickups[0][1]]
        self.world[self.pickups[1][0]][self.pickups[1][1]] = self.world[new_pickups[1][0]][new_pickups[1][1]]
        self.pickups = new_pickups
        self.reset(10)