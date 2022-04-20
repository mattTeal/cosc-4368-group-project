from state import state
import numpy as np


class Qtable_v2:
    stateSpace = np.empty((5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 2, 2), dtype=object)

    def __init__(self, learning, discount):
        self.learning = learning
        self.discount = discount
        # Positions of agents
        for i1 in range(5):
            for j1 in range(5):
                for i2 in range(5):
                    for j2 in range(5):
                        # Carrying block
                        for x1 in range(2):
                            for x2 in range(2):
                                # Pickup contains blocks
                                for p1 in range(2):
                                    for p2 in range(2):
                                        # Dropoff has empty space
                                        for d1 in range(2):
                                            for d2 in range(2):
                                                for d3 in range(2):
                                                    for d4 in range(2):
                                                        self.stateSpace[i1][j1][i2][j2][x1][x2][p1][p2][d1][d2][d3][d4] = state(
                                                        )

    def __getitem__(self, key):
        return self.stateSpace[key]

    def getQVal(self, agent_one, agent_two, world_state):
        i1, j1, x1 = agent_one.getState()
        i2, j2, x2 = agent_two.getState()
        p1, p2, d1, d2, d3, d4 = world_state
