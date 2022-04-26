from state import state
from policies import *
import numpy as np
import pandas as pd

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

    def getQtable(self, x):
        flattened_qtable = []
        for i in range(5):
            for j in range(5):
                N = 0
                E = 0
                S = 0
                W = 0
                P = 0
                D = 0
                for m in range(5):
                    for s in range(2):
                        for t in range(2):
                            for u in range(2):
                                for v in range(2):
                                    N += self.stateSpace[i][j][x][m][s][t][u][v].actions["N"]
                                    E += self.stateSpace[i][j][x][m][s][t][u][v].actions["E"]
                                    S += self.stateSpace[i][j][x][m][s][t][u][v].actions["S"]
                                    W += self.stateSpace[i][j][x][m][s][t][u][v].actions["W"]
                                    P += self.stateSpace[i][j][x][m][s][t][u][v].actions["P"]
                                    D += self.stateSpace[i][j][x][m][s][t][u][v].actions["D"]
                new_item = {
                    "N": N,
                    "E": E,
                    "S": S,
                    "W": W,
                    "P": P,
                    "D": D
                }
                flattened_qtable.append(new_item)
        return pd.DataFrame(flattened_qtable)

    def QUpdate(self, oldState, agent, action):
        i, j, x, m, s, t, u, v = oldState
        i1, j1, x1, m1, s1, t1, u1, v1 = agent.getState()
        aplop = agent.aplop()
        oldSS = self.stateSpace[i][j][x][m][s][t][u][v]
        newSS = self.stateSpace[i1][j1][x1][m1][s1][t1][u1][v1]
        qValue = oldSS.QUpdate(action, newSS, self.learning, self.discount, aplop)
        return [[i, j, x], qValue, action]

    def SARSA(self, oldState, agent, action, policy):
        i, j, x, m, s, t, u, v = oldState
        i1, j1, x1, m1, s1, t1, u1, v1 = agent.getState()
        aplop = agent.pairedAgent.phantomMove(action)
        chosenNewMove = chooseMove(aplop, self.getQVal(agent), policy)
        oldSS = self.stateSpace[i][j][x][m][s][t][u][v]
        newSS = self.stateSpace[i1][j1][x1][m1][s1][t1][u1][v1]
        qValue = oldSS.SARSA(action, newSS, self.learning, self.discount, chosenNewMove)
        return [[i, j, x], qValue, action]
