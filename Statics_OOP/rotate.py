import pygame

import math

import time

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

displayWidth = 800
displayHeight = 600

myfont = pygame.font.SysFont("arial", 25) # initializes font

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))

draw = True

theta = 0

X1 = 400
Y1 = 300

key = "none"

while draw: #runs while loop while draw is True

	gameDisplay.fill(white) #fills the display white
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP: #arrow up
				key = "up"
			elif event.key == pygame.K_DOWN: #arrow down
				key = "down"
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP: #arrow up
					key = "none"
			elif event.key == pygame.K_DOWN: #arrow down
				key = "none"

		X2 = X1 + 250
		Y2 = Y1

	pygame.draw.line(gameDisplay, black, (X1,Y1), (X2,Y2), 5)
	pygame.draw.circle(gameDisplay, black, (int(X1),int(Y1)), 5, 5)
	pygame.draw.circle(gameDisplay, black, (int(X2),int(Y2)), 5, 5)

	if key == "up":
		theta += 1

	elif key == "down":
		theta -= 1

	if theta < 0:
		theta = 0
	if theta > 360:
		theta = 360

	cosTheta = math.cos(math.radians(theta))

	sinTheta = math.sin(math.radians(theta))

	# print cosTheta
	# print sinTheta

	newX2 = X2 - X1
	newY2 = Y2 - Y1

		
	X2prime = (newX2)*(cosTheta) + (newY2)*(sinTheta)

	Y2prime = (newY2)*(cosTheta) - (newX2)*(sinTheta)

	X2prime = X2prime + X1
	Y2prime = Y2prime + Y1

	# print (X2prime, Y2prime)

	pygame.draw.line(gameDisplay, blue, (X1,Y1), (X2prime,Y2prime), 5)
	pygame.draw.circle(gameDisplay, blue, (int(X1),int(Y1)), 5, 5)
	pygame.draw.circle(gameDisplay, blue, (int(X2prime),int(Y2prime)), 5, 5)

	angle = myfont.render(str("%.0f" % theta), 1, black)

	gameDisplay.blit(angle, (50,50))

	clock.tick(40)

	pygame.display.update() #updates graphics to screen