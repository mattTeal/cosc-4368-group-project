import pygame
black = (0, 0, 0)
white = (255, 255, 255)

red = (255, 0, 0)
WIDTH = 100
HEIGHT = 100
MARGIN = 5
valueGrid = []
for row in range(5):
	valueGrid.append([])
	for column in range(5):
		valueGrid[row].append(0)
valueGrid[0][4] = 1
pygame.init()
window_size = [1400, 700]
scr = pygame.display.set_mode(window_size)
pygame.display.set_caption("Cell Values")
done = False
clock = pygame.time.Clock()
while not done:
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			done = True 
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			column = pos[0] // (WIDTH + MARGIN)
			row = pos[1] // (HEIGHT + MARGIN)
			valueGrid[row][column] = 1
			print("Click ", pos, "Grid coordinates: ", row, column)
	scr.fill(black)
	for row in range(5):
		for column in range(5):
			color = white
			if valueGrid[row][column] == 1:
				color = red
			pygame.draw.rect(scr,
												color,
												[(MARGIN + WIDTH) * column + MARGIN,
												(MARGIN + HEIGHT) * row + MARGIN,
												WIDTH,
												HEIGHT])
	clock.tick(50)
	pygame.display.flip()
pygame.quit()