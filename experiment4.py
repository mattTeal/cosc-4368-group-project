from email import policy
from typing import final
import pygame
import time
from world import world
from qtable import Qtable
from agent import agent
from policies import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

init_blocks = 10
init_seed = 3325215321
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
purple = (255, 0, 255)
WIDTH = 205
HEIGHT = 205
MARGIN = 5
window_size = [1060, 1060]
scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("Cell Values")
cell_font = pygame.font.get_default_font()
FPS = 10

clock = pygame.time.Clock()


def drawPickup(img, blocks):
    D_img = pygame.font.SysFont(cell_font,
                                25).render(
        "P: " + str(blocks), True, black
    )
    text_rect = D_img.get_rect(center=img.topleft)
    text_rect.x += 22
    text_rect.y += 12
    scr.blit(D_img, text_rect)
    for i in range(blocks):
        P_img = pygame.font.SysFont(cell_font, 50).render("*", True, purple)
        text_rect = P_img.get_rect(center=img.topleft)
        text_rect.x += 10 + i * 8
        text_rect.y += 35
        scr.blit(P_img, text_rect)


def drawPD(pickups, dropoffs, init_blocks):
    for pickup in pickups:
        cell_image = pygame.draw.rect(scr,
                                      white,
                                      [(MARGIN + WIDTH) * pickup[0] + MARGIN + (WIDTH / 4),
                                       (MARGIN + HEIGHT) *
                                       pickup[1] + MARGIN + (HEIGHT / 4),
                                       WIDTH / 2,
                                       HEIGHT / 2])
        pygame.draw.rect(scr,
                         black,
                         [(MARGIN + WIDTH) * pickup[0] + MARGIN + (WIDTH / 4),
                          (MARGIN + HEIGHT) *
                          pickup[1] + MARGIN + (HEIGHT / 4),
                          WIDTH / 2,
                          HEIGHT / 2], width=2)
        drawPickup(cell_image, init_blocks)
    for dropoff in dropoffs:
        cell_image = pygame.draw.rect(scr,
                                      white,
                                      [(MARGIN + WIDTH) * dropoff[0] + MARGIN + (WIDTH / 4),
                                       (MARGIN + HEIGHT) *
                                       dropoff[1] + MARGIN + (HEIGHT / 4),
                                       WIDTH / 2,
                                       HEIGHT / 2])
        pygame.draw.rect(scr,
                         black,
                         [(MARGIN + WIDTH) * dropoff[0] + MARGIN + (WIDTH / 4),
                          (MARGIN + HEIGHT) *
                          dropoff[1] + MARGIN + (HEIGHT / 4),
                          WIDTH / 2,
                          HEIGHT / 2], width=2)
        drawDropoff(cell_image, 0)


def drawDropoff(img, blocks):
    D_img = pygame.font.SysFont(cell_font,
                                25).render(
        "D: " + str(blocks), True, black
    )
    text_rect = D_img.get_rect(center=img.topleft)
    text_rect.x += 22
    text_rect.y += 12
    scr.blit(D_img, text_rect)
    for i in range(blocks):
        item = pygame.font.SysFont(cell_font, 50).render("*", True, green)
        item_rect = item.get_rect(center=img.topleft)
        item_rect.x += 10 + i*8
        item_rect.y += 35
        scr.blit(item, item_rect)


def drawCellValue(img, value):
    value_img = pygame.font.SysFont(cell_font,
                                    20).render(
        str(round(value, 3)), True, black
    )
    text_rect = value_img.get_rect(center=img.center)
    scr.blit(value_img, text_rect)


def drawLastMove(img, move, color):
    last_move_img = pygame.font.SysFont(cell_font,
                                        25).render(
        move, True, color
    )
    text_rect = last_move_img.get_rect(center=img.center)
    text_rect.y += 30
    scr.blit(last_move_img, text_rect)


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


def drawPolygon(point1, point2, point3, point4, color):
    cell_img = pygame.draw.polygon(
        scr, color, [point1, point2, point3, point4])
    pygame.draw.polygon(scr, black, [point1, point2, point3, point4], width=2)
    return cell_img


def drawBlock(column, row, color, value, action="none"):
    topLeft = ((MARGIN + WIDTH) * column + MARGIN,
               (MARGIN + HEIGHT) * row + MARGIN)
    topRight = (topLeft[0]+WIDTH, topLeft[1])
    bottomLeft = (topLeft[0], topLeft[1]+HEIGHT)
    bottomRight = (topLeft[0]+WIDTH, topLeft[1]+HEIGHT)
    centerTL = (topLeft[0] + WIDTH / 4, topLeft[1] + HEIGHT / 4)
    centerTR = (topRight[0] - WIDTH / 4, topRight[1] + HEIGHT / 4)
    centerBL = (bottomLeft[0] + WIDTH / 4, bottomLeft[1] - HEIGHT / 4)
    centerBR = (bottomRight[0] - WIDTH / 4, bottomRight[1] - HEIGHT / 4)

    if(action == "N" or action == "none"):
        cell_img = drawPolygon(topLeft, topRight, centerTR, centerTL, color)
    if(action == "E" or action == "none"):
        cell_img = drawPolygon(topRight, bottomRight,
                               centerBR, centerTR, color)
    if(action == "S" or action == "none"):
        cell_img = drawPolygon(bottomRight, bottomLeft,
                               centerBL, centerBR, color)
    if(action == "W" or action == "none"):
        cell_img = drawPolygon(bottomLeft, topLeft, centerTL, centerBL, color)
    if(action == "P" or action == "D"):
        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * column + MARGIN + (WIDTH / 4),
                                     (MARGIN + HEIGHT) * row +
                                     MARGIN + (HEIGHT / 4),
                                     WIDTH / 2,
                                     HEIGHT / 2])
    drawCellValue(cell_img, value)
    return cell_img


def drawCenter(pos1, pos2, color):
    return pygame.draw.rect(scr, color, [(MARGIN + WIDTH) * pos1 + MARGIN + (WIDTH / 4),
                                         (MARGIN + HEIGHT) * pos2 +
                                         MARGIN + (HEIGHT / 4),
                                         WIDTH / 2,
                                         HEIGHT / 2])


def initialDraw(world):
    for row in range(5):
        for column in range(5):
            color = white
            cell_img = drawBlock(row, column, color, 0)
    drawPD(world.pickups, world.dropoffs, init_blocks)
    clock.tick(FPS)
    pygame.display.flip()


def PlayerMove(agent, policy):
    moves = agent.aplop()
    chosenMove = chooseMove(moves, agent.getQVals(), policy)
    oldPos, value, action = agent.move(chosenMove, policy)
    newPos = agent.getPos()

    return [oldPos, newPos, chosenMove, value]

# Call to run with policy and max moves or terminal states
# Returns moves ran if given terminal states stopping point or terminal states reached if given moves


def Run(currentPolicy, femaleAgent, maleAgent, moves=0, terminalStops=0):
    world = femaleAgent.world
    currentMoves = 0
    totalMoves = 0
    terminalStates = 0
    movesPerTerminal = []
    while(True):
        ##Female Agent##
        fPos, new_fPos, chosenMove, value = PlayerMove(
            femaleAgent, currentPolicy)
        cell_img = drawCenter(new_fPos[0], new_fPos[1], yellow)
        cell_img = drawCenter(fPos[0], fPos[1], black)
        drawLastMove(cell_img, chosenMove, yellow)
        cell_shade = shadeCell(value)
        cell_img = drawBlock(fPos[0], fPos[1], cell_shade, value, chosenMove)
        if(not fPos == new_fPos):
            if(tuple(fPos[0:2]) in world.pickups):
                cell_img = drawCenter(fPos[0], fPos[1], white)
                drawPickup(cell_img, world[fPos[0]][fPos[1]])
            if(tuple(fPos[0:2]) in world.dropoffs):
                cell_img = drawCenter(fPos[0], fPos[1], white)
                drawDropoff(cell_img, world[fPos[0]][fPos[1]])

        clock.tick(FPS)
        pygame.display.flip()
        ##Male Agent##
        mPos, new_mPos, chosenMove, value = PlayerMove(
            maleAgent, currentPolicy)
        cell_img = drawCenter(new_mPos[0], new_mPos[1], blue)
        cell_img = drawCenter(mPos[0], mPos[1], black)
        drawLastMove(cell_img, chosenMove, yellow)
        cell_shade = shadeCell(value)
        cell_img = drawBlock(mPos[0], mPos[1], cell_shade, value, chosenMove)
        if(not mPos == new_mPos):
            if(tuple(mPos[0:2]) in world.pickups):
                cell_img = drawCenter(mPos[0], mPos[1], white)
                drawPickup(cell_img, world[mPos[0]][mPos[1]])
            if(tuple(mPos[0:2]) in world.dropoffs):
                cell_img = drawCenter(mPos[0], mPos[1], white)
                drawDropoff(cell_img, world[mPos[0]][mPos[1]])
        clock.tick(FPS)
        pygame.display.flip()
        #Reset for terminal state##
        if(world.isTerminal()):
            pause = 1
            terminalStates += 1
            movesPerTerminal.append(currentMoves)
            currentMoves = 0
            world.reset(init_blocks)
            femaleAgent.reset(2, 0)
            maleAgent.reset(2, 4)
            if(terminalStates == terminalStops):
                break
            initialDraw(world)
        if (totalMoves == moves and moves != 0):
            break
        totalMoves += 1
        currentMoves += 1
        clock.tick(FPS)
        pygame.display.flip()

    movesPerTerminal.append(currentMoves)
    return movesPerTerminal, totalMoves

# Where to put your experiment. Call run with necessary params


def PlayGame(femaleAgent, maleAgent):
    done = False
    initialDraw(femaleAgent.world)
    movesPerTerminal = []
    totalMoves = 0
    while not done:
        mpt, currentMoves = Run("PR", femaleAgent, maleAgent, moves=500)
        movesPerTerminal.extend(mpt)
        totalMoves += currentMoves
        mpt, currentMoves = Run("PE", femaleAgent, maleAgent, terminalStops=3)
        mpt[0] += movesPerTerminal.pop()
        movesPerTerminal.extend(mpt[:-1])
        totalMoves += currentMoves
        femaleAgent.world.changePickups([(0, 1), (3, 4)])
        initialDraw(femaleAgent.world)
        mpt, currentMoves = Run("PE", femaleAgent, maleAgent, terminalStops=3)
        movesPerTerminal.extend(mpt[:-1])
        totalMoves += currentMoves
        done = True
    return movesPerTerminal, (femaleAgent.manhattan / totalMoves)


def finalQtable(qtable, world):
    initialDraw(world)
    drawCenter(2, 0, yellow)
    drawCenter(2, 4, blue)
    for index, row in qtable.iterrows():
        drawBlock(int(index / 5), index %
                  5, shadeCell(row["N"] / 4), row["N"], "N")
        drawBlock(int(index / 5), index %
                  5, shadeCell(row["E"] / 4), row["E"], "E")
        drawBlock(int(index / 5), index %
                  5, shadeCell(row["S"] / 4), row["S"], "S")
        drawBlock(int(index / 5), index %
                  5, shadeCell(row["W"] / 4), row["W"], "W")
    clock.tick(FPS)
    pygame.display.flip()


def initVariables(combined, learning, discount, algo):
    pickups = [(4, 2), (1, 3)]
    dropoffs = [(0, 0), (4, 0), (2, 2), (4, 4)]
    World = world(pickups, dropoffs, init_blocks)
    if (combined):
        combinedQTable = Qtable(learning, discount)
        femaleAgent = agent(2, 0, 0, combinedQTable, World, algo)
        maleAgent = agent(2, 4, 0, combinedQTable, World, algo)
    else:
        femaleAgent = agent(2, 0, 0, Qtable(learning, discount), World, algo)
        maleAgent = agent(2, 4, 0, Qtable(learning, discount), World, algo)
    femaleAgent.pairAgent(maleAgent)
    return femaleAgent, maleAgent, World


def plot(run1, run2):
    sns.regplot(y=run1, x=np.arange(0, len(run1), 1),
                color="g", label="First Run")
    ax2 = plt.twinx()
    sns.regplot(y=run2, x=np.arange(0, len(run2), 1),
                ax=ax2, label="Second Run")
    plt.title("Moves per Terminal State Vs. Time")
    plt.xlabel("Terminal State")
    plt.ylabel("Moves")
    plt.show()


print("Seperate Tables")
algo = "SARSA"
random.seed(init_seed)
femaleAgent, maleAgent, World = initVariables(False, 0.3, 0.5, algo)
sepMPTRun1, manhattan = PlayGame(femaleAgent, maleAgent)
print("Average Manhattan Distance:", manhattan)

random.seed(init_seed + 17438291)
femaleAgent, maleAgent, World = initVariables(False, 0.3, 0.5, algo)
sepMPTRun2, manhattan = PlayGame(femaleAgent, maleAgent)
print("Average Manhattan Distance:", manhattan)
print("Female Final Qtable Run 2 (sep=True, x = 0):")
finalQtable(femaleAgent.qTable.getQtable(0), World)
time.sleep(20)
print("Female Final Qtable Run 2 (sep=True, x = 1):")
finalQtable(femaleAgent.qTable.getQtable(1), World)
time.sleep(0)
print("Male Final Qtable Run 2 (sep=True, x = 0):")
finalQtable(maleAgent.qTable.getQtable(0), World)
time.sleep(20)
print("Male Final Qtable Run 2 (sep=True, x = 1):")
finalQtable(maleAgent.qTable.getQtable(1), World)
time.sleep(0)

print("Combined Tables")
# COMBINED QTABLES
random.seed(init_seed)
femaleAgent, maleAgent, World = initVariables(True, 0.3, 0.5, algo)
comMPTRun1, manhattan = PlayGame(femaleAgent, maleAgent)
print("Average Manhattan Distance:", manhattan)
print("Combined Final Qtable Run 1 (x=0): ")
finalQtable(femaleAgent.qTable.getQtable(0), World)
time.sleep(20)
print("Combined Final Qtable Run 1 (x=1): ")
finalQtable(femaleAgent.qTable.getQtable(1), World)
time.sleep(20)

random.seed(init_seed + 17438291)
femaleAgent, maleAgent, World = initVariables(True, 0.3, 0.5, algo)
comMPTRun2, manhattan = PlayGame(femaleAgent, maleAgent)
print("Average Manhattan Distance:", manhattan)
print("Combined Final Qtable Run 2 (x=0): ")
finalQtable(femaleAgent.qTable.getQtable(0), World)
time.sleep(20)
print("Combined Final Qtable Run 2 (x=1): ")
finalQtable(femaleAgent.qTable.getQtable(1), World)
time.sleep(20)

plot(sepMPTRun1, sepMPTRun2)
plot(comMPTRun1, comMPTRun2)

pygame.quit()
