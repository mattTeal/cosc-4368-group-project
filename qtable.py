from state import state
import numpy as np


class Qtable:

    def __init__(self, learning, discount):
        self.stateSpace = np.empty((5, 5, 2, 5, 2, 2, 2, 2), dtype=object)
        self.learning = learning
        self.discount = discount
        for i in range(5):
            for j in range(5):
                for x in range(2):
                    for m in range(5):
                        for s in range(2):
                            for t in range(2):
                                for u in range(2):
                                    for v in range(2):
                                        self.stateSpace[i][j][x][m][s][t][u][v] = state()

    def __getitem__(self, key):
        return self.stateSpace[key]

    def getQVal(self, agent):
        i, j, x, m, s, t, u, v = agent.getState()
        return self.stateSpace[i][j][x][m][s][t][u][v].actions

    def QUpdate(self, oldState, agent, action):
        i, j, x, m, s, t, u, v = oldState
        i1, j1, x1, m1, s1, t1, u1, v1 = agent.getState()
        aplop = agent.aplop()
        oldSS = self.stateSpace[i][j][x][m][s][t][u][v]
        newSS = self.stateSpace[i1][j1][x1][m1][s1][t1][u1][v1]
        qValue = oldSS.QUpdate(action, newSS, self.learning, self.discount, aplop)
        return [[i, j, x], qValue, action]

    def SARSA(self, oldState, agent, action, newAction):
        i, j, x, k, l, s, t, u, v = oldState
        i1, j1, x1 = agent.agentState
        s1, t1, u1, v1 = agent.worldState
        qValue = self.stateSpace[i][j][x][k][l][s][t][u][v].SARSA(
            action, self.stateSpace[i1][j1][x1][k][l][s1][t1][u1][v1], self.learning, self.discount, newAction)
        return [[i, j, x], qValue, action]
