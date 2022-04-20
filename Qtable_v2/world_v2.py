import numpy as np


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

    def getWorldState(self):
        pickup1 = self.pickups[0]
        pickup2 = self.pickups[1]
        x, y = pickup1
        if world[x][y] > 0:
            p1 = 1
        x, y = pickup2
        if world[x][y] > 0:
            p2 = 1

        dropoff1 = self.dropoffs[0]
        x, y = dropoff1
        if world[x][y] > 0:
            d1 = 1
        dropoff2 = self.dropoffs[1]
        x, y = dropoff2
        if world[x][y] > 0:
            d2 = 1
        dropoff3 = self.dropoffs[2]
        x, y = dropoff3
        if world[x][y] > 0:
            d3 = 1
        dropoff4 = self.dropoffs[3]
        x, y = dropoff4
        if world[x][y] > 0:
            d4 = 1

        return [p1, p2, d1, d2, d3, d4]

    def aplop(self):
        # Find operators for each agent, return as ([], [])
        pass

    def apply(self, action_one, action_two):
        # Apply actions on agents, respectively
        pass
