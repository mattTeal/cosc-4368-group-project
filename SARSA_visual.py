from email import policy
import pygame
import time
from dummymoves import moves
from dataclasses import make_dataclass
from world import world
from qtable import Qtable
from agent import agent
from policies import *


# QLearn or SARSA
algo = "SARSA"
#PR, PE, PG
policies = "PR"

pickups = [(4, 2), (1, 3)]
dropoffs = [(0, 0), (4, 0), (2, 2), (4, 4)]
items = [[0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 10],
         [0, 10, 0, 0, 0],
         [0, 0, 0, 0, 0]]
init_blocks = 10
learningRate = 0.3
discountRate = 0.5
testWorld = world(pickups, dropoffs, init_blocks)

SfemaleAgent = agent(2, 0, 0, Qtable(
    learningRate, discountRate), testWorld, algo)
SmaleAgent = agent(2, 4, 0, Qtable(
    learningRate, discountRate), testWorld, algo)
SfemaleAgent.pairAgent(SmaleAgent)

terminalStates = 0

##Init Game##
pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
redtone = red
greentone = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 128, 0)
WIDTH = 100
HEIGHT = 100
MARGIN = 5
window_size = [530, 530]
scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("Cell Values")
cell_font = pygame.font.get_default_font()

valueGrid = []
for row in range(5):
    valueGrid.append([])
    for column in range(5):
        valueGrid[row].append(0)

mAgent = [4, 2]
fAgent = [0, 2]
valueGrid[mAgent[0]][mAgent[1]] = 1
valueGrid[fAgent[0]][fAgent[1]] = 1

pickup_locations = [[2, 4], [3, 1]]
dropoff_locations = [[0, 0], [0, 4], [2, 2], [4, 4]]

done = False
clock = pygame.time.Clock()


def drawPickup(img, blocks):
    D_img = pygame.font.SysFont(cell_font,
                                25).render(
        "P: " + str(blocks), True, black
    )
    text_rect = D_img.get_rect(center=img.topleft)
    text_rect.x += 20
    text_rect.y += 10
    scr.blit(D_img, text_rect)
    for i in range(blocks):
        P_img = pygame.font.SysFont(cell_font, 50).render("*", True, red)
        text_rect = P_img.get_rect(center=img.topleft)
        text_rect.x += 10 + i * 8
        text_rect.y += 35
        scr.blit(P_img, text_rect)


def drawDropoff(img, blocks):

    D_img = pygame.font.SysFont(cell_font,
                                25).render(
        "D: " + str(blocks), True, black
    )
    text_rect = D_img.get_rect(center=img.topleft)
    text_rect.x += 20
    text_rect.y += 10
    scr.blit(D_img, text_rect)
    for i in range(blocks):
        item = pygame.font.SysFont(cell_font, 50).render("*", True, green)
        item_rect = item.get_rect(center=img.topleft)
        item_rect.x += 10 + i*8
        item_rect.y += 35
        scr.blit(item, item_rect)


def drawCellValue(img, value):
    value_img = pygame.font.SysFont(cell_font,
                                    40).render(
        str(round(value, 3)), True, black
    )
    text_rect = value_img.get_rect(center=img.center)
    scr.blit(value_img, text_rect)


def drawLastMove(img, move):
    last_move_img = pygame.font.SysFont(cell_font,
                                        25).render(
        move, True, black
    )
    text_rect = last_move_img.get_rect(center=img.center)
    text_rect.y += 30
    scr.blit(last_move_img, text_rect)


def checkLocation(img, row, column, blocks):
    for loc in pickup_locations:
        if (row == loc[0] and column == loc[1]):
            drawPickup(img, blocks)
    for loc in dropoff_locations:
        if (row == loc[0] and column == loc[1]):
            drawDropoff(img, blocks)


def shadeCell(value):
    if (value < 0):
        if (value < -1):
            value = 0
        else:
            value = (1 - abs(value)) * 250
        return (255, value, value)
    else:
        if(value < 1):
            value = (abs(1 - value)) * 250
        else:
            value = 0
        return (value, 255, value)


for row in range(5):
    for column in range(5):
        color = white

        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * column + MARGIN,
                                     (MARGIN + HEIGHT) * row + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        blocks = items[row][column]
        checkLocation(cell_img, row, column, blocks)
        drawCellValue(cell_img, 0)
        if valueGrid[row][column] == 1:
            color = red

clock.tick(50)
pygame.display.flip()
terminalStates = 0
count = 0

fmoves = SfemaleAgent.aplop()
fchosenMove = chooseMove(fmoves, SfemaleAgent.getQVals(), policies)

mmoves = SmaleAgent.aplop()
mchosenMove = chooseMove(mmoves, SmaleAgent.getQVals(), policies)

speed = 0.0001
sleep = 0
while not done:
    time.sleep(.5)
    for i in range(8000):
        if i == 500:
            policies = "PE"

        foldstate = SfemaleAgent.getState()
        SfemaleAgent.move(fchosenMove)

        moldstate = SmaleAgent.getState()
        SmaleAgent.move(mchosenMove)

        ##Female Agent##
        fmoves = SfemaleAgent.aplop()
        fchosenMove2 = chooseMove(fmoves, SfemaleAgent.getQVals(), policies)
        qtable = SfemaleAgent.sarsa(foldstate, fchosenMove, fchosenMove2)

        value = qtable[1]
        cell_shade = shadeCell(value)
        move = qtable[2]
        cell_img = pygame.draw.rect(scr,
                                    cell_shade,
                                    [(MARGIN + WIDTH) * fAgent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * fAgent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        if(fchosenMove == 'P'):
            items[fAgent[0]][fAgent[1]] -= 1
            blocks = items[fAgent[0]][fAgent[1]]
            checkLocation(
                cell_img, fAgent[0], fAgent[1], blocks)
        elif(fchosenMove == 'D'):
            items[fAgent[0]][fAgent[1]] += 1
            blocks = items[fAgent[0]][fAgent[1]]
            checkLocation(
                cell_img, fAgent[0], fAgent[1], blocks)
        else:
            blocks = items[fAgent[0]][fAgent[1]]
            checkLocation(
                cell_img, fAgent[0], fAgent[1], blocks)
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, move)
        fMoves = SfemaleAgent.getPos()
        fAgent[0] = fMoves[1]
        fAgent[1] = fMoves[0]

        color = red
        cell_img = pygame.draw.rect(scr,
                                    yellow,
                                    [(MARGIN + WIDTH) * fAgent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * fAgent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        blocks = items[fAgent[0]][fAgent[1]]
        checkLocation(
            cell_img, fAgent[0], fAgent[1], blocks)
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, move)

        fchosenMove = fchosenMove2
        ##Male Agent##
        mmoves = SmaleAgent.aplop()
        qval = SmaleAgent.getQVals()
        mchosenMove2 = chooseMove(mmoves, SmaleAgent.getQVals(), policies)
        qtable = SmaleAgent.sarsa(moldstate, mchosenMove, mchosenMove2)
        value = qtable[1]
        cell_shade = shadeCell(value)
        move = qtable[2]

        cell_img = pygame.draw.rect(scr, cell_shade,
                                    [(MARGIN + WIDTH) * mAgent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * mAgent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        if(mchosenMove == 'P'):
            items[mAgent[0]][mAgent[1]] -= 1
            blocks = items[mAgent[0]][mAgent[1]]
            checkLocation(
                cell_img, mAgent[0], mAgent[1], blocks)
        elif(mchosenMove == 'D'):
            items[mAgent[0]][mAgent[1]] += 1
            blocks = items[mAgent[0]][mAgent[1]]
            checkLocation(
                cell_img, mAgent[0], mAgent[1], blocks)
        else:
            blocks = items[mAgent[0]][mAgent[1]]
            checkLocation(
                cell_img, mAgent[0], mAgent[1], blocks)
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, move)

        mMoves = SmaleAgent.getPos()
        mAgent[0] = mMoves[1]
        mAgent[1] = mMoves[0]

        color = blue
        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * mAgent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * mAgent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        blocks = items[mAgent[0]][mAgent[1]]
        checkLocation(
            cell_img, mAgent[0], mAgent[1], blocks)
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, move)
        mchosenMove = mchosenMove2

        count += 1

        #Reset for terminal state##
        if(testWorld.isTerminal()):
            print(count)
            count = 0
            terminalStates += 1
            if terminalStates == 19:
                sleep = 10
                speed = 0.5
            testWorld.reset(init_blocks)
            SfemaleAgent.reset(2, 0)
            SmaleAgent.reset(2, 4)
            mAgent = [4, 2]
            fAgent = [0, 2]
            items = [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 10],
                     [0, 10, 0, 0, 0],
                     [0, 0, 0, 0, 0]]
            fmoves = SfemaleAgent.aplop()
            fchosenMove = chooseMove(fmoves, SfemaleAgent.getQVals(), policies)
            mmoves = SmaleAgent.aplop()
            mchosenMove = chooseMove(mmoves, SmaleAgent.getQVals(), policies)

            for row in range(5):
                for column in range(5):
                    color = white

                    cell_img = pygame.draw.rect(scr,
                                                color,
                                                [(MARGIN + WIDTH) * column + MARGIN,
                                                 (MARGIN + HEIGHT) *
                                                 row + MARGIN,
                                                 WIDTH,
                                                 HEIGHT])
                    blocks = items[row][column]
                    checkLocation(cell_img, row, column, blocks)
                    if valueGrid[row][column] == 1:
                        color = red
            time.sleep(sleep)
        clock.tick(50)
        pygame.display.flip()

        # speed of agent movement
        time.sleep(speed)

    print("Terminal states reached: ", terminalStates)
    time.sleep(10)
    done = True
print(items)
pygame.quit()
