class state:
    rewards = {
        "N": -1,
        "E": -1,
        "S": -1,
        "W": -1,
        "P": 13,
        "D": 13
    }

    def __init__(self):
        self.actions = {
            "N": 0,
            "E": 0,
            "S": 0,
            "W": 0,
            "P": 0,
            "D": 0
        }

    def maxApplicable(self, aplop):
        values = []
        for keys, value in self.actions.items():
            if keys in aplop:
                values.append(value)
        return max(values)

    def QUpdate(self, action, new_state, learning, discount, aplop):
        self.actions[action] = (1 - learning) * self.actions[action] + learning * (
            self.rewards[action] + discount * new_state.maxApplicable(aplop))
        return self.actions[action]

    def SARSA(self, action, new_state, learning, discount):
        self.actions[action] = self.actions[action] + learning * \
            (self.rewards[action] + discount *
             new_state.actions[action] - self.actions[action])
        return self.actions[action]
