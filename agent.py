class agent:
    def __init__(self, i, j, x, qTable, world, learningStrat):
        self.agentState = [i, j, x]
        self.qTable = qTable
        self.world = world
        self.worldState = world.getWorldState(x)
        self.pairedAgent = None
        self.lrnStrat = learningStrat

    def getPos(self):
        return self.agentState

    def getQVals(self):
        return self.qTable.getQVal(self)
    
    def getState(self):
        i, j, x = self.agentState
        s, t, u, v = self.worldState
        i2, j2, x2 = self.pairedAgent.agentState
        return [i, j, x, i2, j2, s, t, u, v]

    def pairAgent(self, agent):
        if self.pairedAgent: return
        self.pairedAgent = agent
        agent.pairAgent(self)

    def aplop(self):
        return self.world.aplop(self)

    def move(self, action):
        newAgentState, newWorldState = self.world.apply(self, action)
        oldState = self.getState()
        self.agentState = newAgentState
        self.worldState = newWorldState
        if self.lrnStrat == "QLearn":
            return self.qTable.QUpdate(oldState, self, action)
        if self.lrnStrat == "SARSA":
            return self.qTable.SARSA(oldState, self, action)
        return -1
    
    def reset(self, i, j):
        self.agentState = [i, j, 0]
        self.worldState = self.world.getWorldState(0)