from state import state
import numpy as np


class Qtable:
    stateSpace = np.empty((5, 5, 2, 5, 5, 2, 2, 2, 2), dtype=object)

    def __init__(self, learning, discount):
        self.learning = learning
        self.discount = discount
        for i in range(5):
            for j in range(5):
                for x in range(2):
                    for k in range(5):
                        for l in range(5):
                            for s in range(2):
                                for t in range(2):
                                    for u in range(2):
                                        for v in range(2):
                                            self.stateSpace[i][j][x][k][l][s][t][u][v] = state(
                                            )

    def __getitem__(self, key):
        return self.stateSpace[key]

    def getQVal(self, state):
        i, j, x, k, l, s, t, u, v = state
        return self.stateSpace[i][j][x][k][l][s][t][u][v].actions

    def QUpdate(self, currentState, newState, action, aplop):
        i, j, x, k, l, s, t, u, v = currentState
        i1, j1, x1, k1, l1, s1, t1, u1, v1 = newState
        self.stateSpace[i][j][x][k][l][s][t][u][v].QUpdate(
            action, self.stateSpace[i1][j1][x1][k1][l1][s1][t1][u1][v1], self.learning, self.discount, aplop)

    def SARSA(self, currentState, newState, action):
        i, j, x, k, l, s, t, u, v = currentState
        i1, j1, x1, k1, l1, s1, t1, u1, v1 = newState
        self.stateSpace[i][j][x][k][l][s][t][u][v].SARSA(
            action, self.stateSpace[i1][j1][x1][k1][l1][s1][t1][u1][v1], self.learning, self.discount)
