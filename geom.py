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

gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))

clock = pygame.time.Clock()

draw = True 
flag = False

theta = 0


while draw: #runs while loop while draw is True

	gameDisplay.fill(white) #fills the display white

	Click = pygame.mouse.get_pressed() # checks for a mouse click and stores a tuple of (0,0,0) = (left, mid, right) in self.leftClick
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				print("dimension")
				draw = False #exits the drawBeam function

	if Click[0] == True and flag == False:
			
		X1,Y1 = pygame.mouse.get_pos()

		X1 = float (X1)
		Y1 = float (Y1)

		flag = True

	elif Click[0] == True and flag == True:

		X2,Y2 = pygame.mouse.get_pos()

		X2 = float (X2)
		Y2 = float(Y2)

		if X1 == X2 or Y1 == Y2:
			X2 = X1 + 1.0
			Y2 = Y1 + 2.0


		theta = math.degrees(math.atan((Y1 - Y2)/(X2 - X1)))

		modTheta = theta

		if (X2 - X1) < 0:
			modTheta = theta + 180


		pygame.draw.line(gameDisplay, blue, (int(X1),int(Y1)), (int(X2),int(Y2)), 5)
		pygame.draw.circle(gameDisplay, blue, (int(X1),int(Y1)), 5, 5)
		pygame.draw.circle(gameDisplay, blue, (int(X2),int(Y2)), 5, 5)

		cosTheta = math.cos(math.radians(round(modTheta)))

		sinTheta = math.sin(math.radians(round(modTheta)))


		X3 = X1 + 30
		Y3 = Y1 + 12

		newX3 = X3 - X1
		newY3 = Y3 - Y1


		X3prime = (newX3)*(cosTheta) + (newY3)*(sinTheta)

		Y3prime = (newY3)*(cosTheta) - (newX3)*(sinTheta)

		X3prime = X3prime + X1
		Y3prime = Y3prime + Y1



		X4 = X1 - 30
		Y4 = Y1 + 12

		newX4 = X4 - X1
		newY4 = Y4 - Y1


		X4prime = (newX4)*(-cosTheta) + (newY4)*(-sinTheta)

		Y4prime = (newY4)*(-cosTheta) - (newX4)*(-sinTheta)

		X4prime = X4prime + X1
		Y4prime = Y4prime + Y1


		pygame.draw.polygon(gameDisplay, blue, ((int(X1),int(Y1)), (int(X3prime), int(Y3prime)), (int(X4prime), int(Y4prime))))
		
		
		angle = myfont.render(str("%.0f" % round(theta)), 1, black)

		gameDisplay.blit(angle, (X1+20,Y1-20))

	elif Click[0] == False and flag == True:

		flag = False


	pygame.display.update() #updates graphics to screen