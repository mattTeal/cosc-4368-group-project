import main

def aplop(i, j, i2, j2, x, x2, a, b, c, d, e, f):
  fValidMoves = set()
  mValidMoves = set()
  # Female agent actions
  if (main.world[i][j] == 1):  # and !female.isHoldingBlock
    fValidMoves.add('D')
  elif (main.world[i][j] == 2):  # and female.isHoldingBlock
    fValidMoves.add('P')
  else: 
    if (i == 0):
      fValidMoves.add('S')
      if (j == 0):
        fValidMoves.add('E')
      elif (j == 4):
        fValidMoves.add('W')
    elif (i == 4):
      fValidMoves.add('N')
      if (j == 0):
        fValidMoves.add('E')
      elif (j == 4):
        fValidMoves.add('W')
      else:
        fValidMoves.add('W')
        fValidMoves.add('E')
    else:
      fValidMoves.add('N')
      fValidMoves.add('S')
      if (j == 0):
        fValidMoves.add('E')
      elif (j == 4):
        fValidMoves.add('W')
      else:
        fValidMoves.add('W')
        fValidMoves.add('E')

  # Male agent actions
  if (main.world[i2][j2] == 1):  # and !Male.isHoldingBlock
    mValidMoves.add('D')
  elif (main.world[i2][j2] == 2):  # and Male.isHoldingBlock
    mValidMoves.add('P')
  else: 
    if (i2 == 0):
      mValidMoves.add('S')
      if (j2 == 0):
        mValidMoves.add('E')
      elif (j2 == 4):
        mValidMoves.add('W')
    elif (i2 == 4):
      mValidMoves.add('N')
      if (j2 == 0):
        mValidMoves.add('E')
      elif (j2 == 4):
        mValidMoves.add('W')
      else:
        mValidMoves.add('W')
        mValidMoves.add('E')
    else:
      mValidMoves.add('N')
      mValidMoves.add('S')
      if (j2 == 0):
        mValidMoves.add('E')
      elif (j2 == 4):
        mValidMoves.add('W')
      else:
        mValidMoves.add('W')
        mValidMoves.add('E')


  return fValidMoves, mValidMoves 