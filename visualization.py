import pygame
import time
from dummymoves import moves

from dataclasses import make_dataclass
from world import world
from qtable import Qtable
from agent import agent
from policies import *

##Init World##
random.seed(10)

pickups = [(4, 2), (1, 3)]
dropoffs = [(0, 0), (4, 0), (2, 2), (4, 4)]
init_blocks = 10
learningRate = 0.3
discountRate = 0.5
testWorld = world(pickups, dropoffs, init_blocks)

femaleAgent = agent(2, 0, 0, Qtable(
    learningRate, discountRate), testWorld, "QLearn")
maleAgent = agent(2, 4, 0, Qtable(
    learningRate, discountRate), testWorld, "QLearn")

femaleAgent.pairAgent(maleAgent)

terminalStates = 0

##Init Game##
pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
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
counter = 0


def drawPickup(img):
    for loc in pickup_locations:
        P_img = pygame.font.SysFont(cell_font,
                                    50).render(
            "*", True, black
        )
        text_rect = P_img.get_rect(center=img.topleft)
        text_rect.x += 10
        text_rect.y += 18
        scr.blit(P_img, text_rect)


def drawDropoff(img):
    for loc in dropoff_locations:
        D_img = pygame.font.SysFont(cell_font,
                                    25).render(
            "D", True, black
        )
        text_rect = D_img.get_rect(center=img.topleft)
        text_rect.x += 10
        text_rect.y += 10
        scr.blit(D_img, text_rect)


def drawCellValue(img, value):
    for loc in dropoff_locations:
        value_img = pygame.font.SysFont(cell_font,
                                        40).render(
            str(round(value, 3)), True, black
        )
        text_rect = value_img.get_rect(center=img.center)
        scr.blit(value_img, text_rect)


def drawLastMove(img, move):
    for loc in dropoff_locations:
        last_move_img = pygame.font.SysFont(cell_font,
                                            25).render(
            move, True, black
        )
        text_rect = last_move_img.get_rect(center=img.center)
        text_rect.y += 30
        scr.blit(last_move_img, text_rect)


def checkLocation(img, row, column):
    for loc in pickup_locations:
        if (row == loc[0] and column == loc[1]):
            drawPickup(img)
    for loc in dropoff_locations:
        if (row == loc[0] and column == loc[1]):
            drawDropoff(img)


for row in range(5):
    for column in range(5):
        color = white

        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * column + MARGIN,
                                     (MARGIN + HEIGHT) * row + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        checkLocation(cell_img, row, column)
        # drawCellValue(cell_img)
        # drawLastMove(cell_img)

        if valueGrid[row][column] == 1:
            color = red

clock.tick(50)
pygame.display.flip()

while not done:
    time.sleep(.5)
    for i in range(8000):

        ##Calculate moves##
        moves = femaleAgent.aplop()
        chosenMove = chooseMove(moves, femaleAgent.getQVals(), "PG")
        qtable = femaleAgent.move(chosenMove)
        value = qtable[1]
        move = qtable[2]

        ##Female Agent##
        color = white
        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * fAgent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * fAgent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        checkLocation(cell_img, fAgent[0], fAgent[1])
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, move)

        # print(fAgent)
        fMoves = femaleAgent.getPos()
        fAgent[0] = fMoves[1]
        fAgent[1] = fMoves[0]

        color = red
        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * fAgent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * fAgent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        checkLocation(cell_img, fAgent[0], fAgent[1])
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, move)

        ##Male Agent##
        moves = maleAgent.aplop()
        chosenMove = chooseMove(moves, maleAgent.getQVals(), "PG")
        qtable = maleAgent.move(chosenMove)
        value = qtable[1]
        move = qtable[2]

        color = white
        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * mAgent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * mAgent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        checkLocation(cell_img, mAgent[0], mAgent[1])
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, move)

        print(mAgent)
        mMoves = maleAgent.getPos()
        mAgent[0] = mMoves[1]
        mAgent[1] = mMoves[0]

        color = blue
        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * mAgent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * mAgent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        checkLocation(cell_img, mAgent[0], mAgent[1])
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, move)

        clock.tick(50)
        pygame.display.flip()

        time.sleep(.01)

    time.sleep(.6)
    done = True

pygame.quit()
