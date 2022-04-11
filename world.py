import numpy as np
class world:
  def __init__(self, pickups, dropoffs, init_blocks):
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

  # Reworked aplop to be simpler and work without needing to specify agent
  def aplop(self, state):
    i, j, x, i2, j2, s, t, u, v = state
    validMoves = set()
    validDP = [s, t, u, v]
    # Agent actions
    if ((i, j) in self.dropoffs and x):  # on dropoff and isHoldingBlock
      if (validDP[self.dropoffs.index((i, j))]):
        validMoves.add('D')

    if ((i, j) in self.pickups and not x):  # on pickup and !isHoldingBlock
      if (validDP[self.pickups.index((i, j))]):
        validMoves.add('P')

    if (i > 0 and i - 1 != i2):
      validMoves.add('W')
    if (i < 4 and i + 1 != i2):
      validMoves.add('E')
    if (j > 0 and j - 1 != j2):
      validMoves.add('N')
    if (j < 4 and j + 1 != j2):
      validMoves.add('S')
    
    return validMoves