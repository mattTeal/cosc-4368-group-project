import pygame
import time
from dummymoves import moves

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
WIDTH = 100
HEIGHT = 100
MARGIN = 5
window_size = [1400, 700]
scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("Cell Values")
cell_font = pygame.font.get_default_font()

valueGrid = []
for row in range(5):
    valueGrid.append([])
    for column in range(11):
        valueGrid[row].append(0)

agent = [0, 0]
print(agent[0])
valueGrid[agent[0]][agent[1]] = 1

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

def drawCellValue(img):
    for loc in dropoff_locations:
        value_img = pygame.font.SysFont(cell_font,
                                    40).render(
            str(1.0127), True, black
        )
        text_rect = value_img.get_rect(center=img.center)
        scr.blit(value_img, text_rect)
    
def drawLastMove(img):
    for loc in dropoff_locations:
        last_move_img = pygame.font.SysFont(cell_font,
                                    25).render(
            "N", True, black
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
        drawCellValue(cell_img)
        drawLastMove(cell_img)

        if valueGrid[row][column] == 1:
            color = red

clock.tick(50)
pygame.display.flip()

while not done:
    time.sleep(.25)
    for move in moves:
        counter += 1
        color = white
        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * agent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * agent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        checkLocation(cell_img, agent[0], agent[1])
        drawCellValue(cell_img)
        drawLastMove(cell_img)

        print(agent)
        agent[0] = agent[0] + move[0]
        agent[1] = agent[1] + move[1]

        color = red
        cell_img = pygame.draw.rect(scr,
                                    color,
                                    [(MARGIN + WIDTH) * agent[1] + MARGIN,
                                     (MARGIN + HEIGHT) * agent[0] + MARGIN,
                                     WIDTH,
                                     HEIGHT])
        checkLocation(cell_img, agent[0], agent[1])
        drawCellValue(cell_img)
        drawLastMove(cell_img)

        clock.tick(50)
        pygame.display.flip()

        time.sleep(.25)

    time.sleep(.6)
    done = True

pygame.quit()
