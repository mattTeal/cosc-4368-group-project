from email import policy
import pygame
import time
from dummymoves import moves
from dataclasses import make_dataclass
from world import world
from qtable import Qtable
from agent import agent
from policies import *

init_blocks = 10

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
WIDTH = 100
HEIGHT = 100
MARGIN = 5
window_size = [530, 530]
scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("Cell Values")
cell_font = pygame.font.get_default_font()

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
        P_img = pygame.font.SysFont(cell_font, 50).render("*", True, purple)
        text_rect = P_img.get_rect(center=img.topleft)
        text_rect.x += 10 + i * 8
        text_rect.y += 35
        scr.blit(P_img, text_rect)

def drawPD(pickups, dropoffs, init_blocks):
    for pickup in pickups:
        cell_image = pygame.draw.rect(scr,
                                            white,
                                            [(MARGIN + WIDTH) * pickup[0] + MARGIN,
                                            (MARGIN + HEIGHT) * pickup[1] + MARGIN,
                                            WIDTH,
                                            HEIGHT])
        drawPickup(cell_image, init_blocks)
    for dropoff in dropoffs:
        cell_image = pygame.draw.rect(scr,
                                            white,
                                            [(MARGIN + WIDTH) * dropoff[0] + MARGIN,
                                            (MARGIN + HEIGHT) * dropoff[1] + MARGIN,
                                            WIDTH,
                                            HEIGHT])
        drawDropoff(cell_image, init_blocks)

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
        
def initialDraw(world):
    for row in range(5):
        for column in range(5):
            color = white

            cell_img = pygame.draw.rect(scr,
                                        color,
                                        [(MARGIN + WIDTH) * column + MARGIN,
                                        (MARGIN + HEIGHT) * row + MARGIN,
                                        WIDTH,
                                        HEIGHT])
            drawCellValue(cell_img, 0)
    drawPD(world.dropoffs, world.pickups, init_blocks)

def PlayerMove(agent, policy):
    moves = agent.aplop()
    chosenMove = chooseMove(moves, agent.getQVals(), policy)
    oldPos, value, action = agent.move(chosenMove)
    newPos = agent.getPos()


    return [oldPos, newPos, chosenMove, value]

## Call to run with policy and max moves or terminal states
## Returns moves ran if given terminal states stopping point or terminal states reached if given moves
def Run(currentPolicy, femaleAgent, maleAgent, moves=0, terminalStops=0):
    world = femaleAgent.world
    currentMoves = 0
    terminalStates = 0
    while(True):
        ##Female Agent##
        fPos, new_fPos, chosenMove, value = PlayerMove(femaleAgent, currentPolicy)
        cell_img = pygame.draw.rect(scr,
                                yellow,
                                [(MARGIN + WIDTH) * new_fPos[0] + MARGIN,
                                    (MARGIN + HEIGHT) * new_fPos[1] + MARGIN,
                                    WIDTH,
                                    HEIGHT])
        cell_shade = shadeCell(value)
        cell_img = pygame.draw.rect(scr,
                                    cell_shade,
                                    [(MARGIN + WIDTH) * fPos[0] + MARGIN,
                                    (MARGIN + HEIGHT) * fPos[1] + MARGIN,
                                    WIDTH,
                                    HEIGHT])

        if(tuple(fPos[0:2]) in world.pickups):
            drawPickup(cell_img, world[fPos[0]][fPos[1]])
        if(tuple(fPos[0:2]) in world.dropoffs):
            drawDropoff(cell_img, world[fPos[0]][fPos[1]])
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, chosenMove)

        ##Male Agent##
        mPos, new_mPos, chosenMove, value = PlayerMove(maleAgent, currentPolicy)
        cell_img = pygame.draw.rect(scr,
                                blue,
                                [(MARGIN + WIDTH) * new_mPos[0] + MARGIN,
                                    (MARGIN + HEIGHT) * new_mPos[1] + MARGIN,
                                    WIDTH,
                                    HEIGHT])
        cell_shade = shadeCell(value)
        cell_img = pygame.draw.rect(scr,
                                    cell_shade,
                                    [(MARGIN + WIDTH) * mPos[0] + MARGIN,
                                    (MARGIN + HEIGHT) * mPos[1] + MARGIN,
                                    WIDTH,
                                    HEIGHT])

        if(tuple(mPos[0:2]) in pickups):
            drawPickup(cell_img, world[mPos[0]][mPos[1]])
        if(tuple(mPos[0:2]) in dropoffs):
            drawDropoff(cell_img, world[mPos[0]][mPos[1]])
        drawCellValue(cell_img, value)
        drawLastMove(cell_img, chosenMove)

        #Reset for terminal state##
        if(world.isTerminal()):
            pause = 1
            terminalStates += 1
            if(terminalStates == terminalStops):
                break
            world.reset(init_blocks)
            femaleAgent.reset(2, 0)
            maleAgent.reset(2, 4)

            initialDraw(world)
            time.sleep(5)
        if (currentMoves == moves and moves != 0):
            break
        currentMoves += 1
        clock.tick(50)
        pygame.display.flip()

        # speed of agent movement
        time.sleep(0.03)

    if(terminalStops > 0):
        return currentMoves
    else:
        return terminalStates

## Where to put your experiment. Call run with necessary params
def PlayGame(femaleAgent, maleAgent):
    done = False
    initialDraw(femaleAgent.world)
    while not done:
        time.sleep(.5)
        Run("PR", femaleAgent, maleAgent, moves=500)
        firstRun = Run("PE", femaleAgent, maleAgent,terminalStops=3)
        print("Changing Pickups")
        femaleAgent.world.changePickups([(0,1), (3, 4)])
        secondRun = Run("PE", femaleAgent, maleAgent,terminalStops=3)
        print("First Run moves:", firstRun)
        print("Second Run moves:", secondRun)
        time.sleep(10)
        done = True

pickups = [(4, 2), (1, 3)]
dropoffs = [(0, 0), (4, 0), (2, 2), (4, 4)]


print("Seperate Tables")
algo="QLearn"
random.seed(121)
testWorld = world(pickups, dropoffs, init_blocks)
maleQTable = Qtable(0.3, 0.5)
femaleQTable = Qtable(0.3, 0.5)
femaleAgent = agent(2, 0, 0, femaleQTable, testWorld, algo)
maleAgent = agent(2, 4, 0, maleQTable, testWorld, algo)
femaleAgent.pairAgent(maleAgent)
PlayGame(femaleAgent, maleAgent)

random.seed(242)
testWorld = world(pickups, dropoffs, init_blocks)
maleQTable = Qtable(0.3, 0.5)
femaleQTable = Qtable(0.3, 0.5)
femaleAgent = agent(2, 0, 0, femaleQTable, testWorld, algo)
maleAgent = agent(2, 4, 0, maleQTable, testWorld, algo)
femaleAgent.pairAgent(maleAgent)
PlayGame(femaleAgent, maleAgent)

print("Combined Tables")
# COMBINED QTABLES
algo="QLearn"
random.seed(121)
testWorld = world(pickups, dropoffs, init_blocks)
combinedQTable = Qtable(0.3, 0.5)
femaleAgent = agent(2, 0, 0, combinedQTable, testWorld, algo)
maleAgent = agent(2, 4, 0, combinedQTable, testWorld, algo)
femaleAgent.pairAgent(maleAgent)
PlayGame(femaleAgent, maleAgent)


random.seed(242)
testWorld = world(pickups, dropoffs, init_blocks)
combinedQTable = Qtable(0.3, 0.5)
femaleAgent = agent(2, 0, 0, combinedQTable, testWorld, algo)
maleAgent = agent(2, 4, 0, combinedQTable, testWorld, algo)
femaleAgent.pairAgent(maleAgent)
PlayGame(femaleAgent, maleAgent)

pygame.quit()
