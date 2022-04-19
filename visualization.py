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

agent = [0,0]
copy_agent = [0,6]
print(agent[0])
valueGrid[agent[0]][agent[1]] = 1
valueGrid[copy_agent[0]][copy_agent[1]] = 1

pickup_locations = [[2,4], [3,1]]
dropoff_locations = [[0,0], [0,4], [2,2], [4,4]]

done = False
clock = pygame.time.Clock()
counter = 0

def drawPickup(img):
	for loc in pickup_locations:
		P_img = pygame.font.SysFont(cell_font, 
						50).render(
							"P", True, black
						)
		text_rect = P_img.get_rect(center=img.center)
		scr.blit(P_img, text_rect)

def drawDropoff(img):
	for loc in dropoff_locations:
		D_img = pygame.font.SysFont(cell_font, 
						50).render(
							"D", True, black
						)
		text_rect = D_img.get_rect(center=img.center)
		scr.blit(D_img, text_rect)

def checkLocation(img, row, column):
	for loc in pickup_locations:
		if (row == loc[0] and column == loc[1]):
			drawPickup(img)
	for loc in dropoff_locations:
		if (row == loc[0] and column == loc[1]):
			drawDropoff(img)

def checkCopyLocation(img, row, column):
	for loc in pickup_locations:
		if (row == loc[0] and column - 6 == loc[1]):
			drawPickup(img)
	for loc in dropoff_locations:
		if (row == loc[0] and column - 6 == loc[1]):
			drawDropoff(img)

for row in range(5):
		for column in range(11):
			color = white
			if(column == 5):
				color = black

			cell_img = pygame.draw.rect(scr,
								color,
								[(MARGIN + WIDTH) * column + MARGIN,
								(MARGIN + HEIGHT) * row + MARGIN,
								WIDTH,
								HEIGHT])
			checkLocation(cell_img, row, column)
			checkCopyLocation(cell_img, row, column)

			if valueGrid[row][column] == 1:
				color = red
clock.tick(50)
pygame.display.flip()

while not done:
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
		
		copy_cell_img = pygame.draw.rect(scr,
						color,
						[(MARGIN + WIDTH) * copy_agent[1] + MARGIN,
						(MARGIN + HEIGHT) * copy_agent[0] + MARGIN,
						WIDTH,
						HEIGHT])
		checkCopyLocation(copy_cell_img, copy_agent[0], copy_agent[1])
		
		print(agent)
		agent[0] = agent[0] + move[0]
		agent[1] = agent[1] + move[1]
		copy_agent[0] = agent[0]
		copy_agent[1] = agent[1] + 6

		color = red
		cell_img = pygame.draw.rect(scr,
						color,
						[(MARGIN + WIDTH) * agent[1] + MARGIN,
						(MARGIN + HEIGHT) * agent[0] + MARGIN,
						WIDTH,
						HEIGHT])
		checkLocation(cell_img, agent[0], agent[1])

		copy_cell_img = pygame.draw.rect(scr,
						color,
						[(MARGIN + WIDTH) * copy_agent[1] + MARGIN,
						(MARGIN + HEIGHT) * copy_agent[0] + MARGIN,
						WIDTH,
						HEIGHT])
		checkCopyLocation(copy_cell_img, copy_agent[0], copy_agent[1])

		clock.tick(50)
		pygame.display.flip()

		time.sleep(.25)

	time.sleep(60)
	done = True

pygame.quit()