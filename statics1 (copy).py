#Statics App Mark 1

import pygame

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

displayHeight = 600
displayWidth = 1000

gameDisplay = pygame.display.set_mode((displayWidth,displayHeight)) # (Width,height)

clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("none", 25)
medfont = pygame.font.SysFont("none", 50)
largefont = pygame.font.SysFont("none", 80)

def text_objects(text, color, size): #FUNCTION HANDLES FONT SIZE OF TEXT OBJECTS AND RETURNS A TEXT SURFACE 
	if size == "small":
		textSurface = smallfont.render(text, True, color)
	elif size == "medium":
		textSurface = medfont.render(text, True, color)
	elif size == "large":
		textSurface = largefont.render(text, True, color)
	
	return textSurface, textSurface.get_rect()

def message_to_screen(msg,color, y_displace=0, size = "small"): #FUNCTION BLITS A MESSAGE TO THE SCREEN
	textSurf, textRect = text_objects(msg, color, size)
	textRect.center = (displayWidth/2), (displayHeight/2) + y_displace
	gameDisplay.blit(textSurf, textRect)

def control_info(): #CONTROL INFORMATION FUNCTION BRING UP CONTROL INFORMATION SCREEN
	info = True

	message_to_screen("CONTROLS INFORMATION", black, -100, size = "large")
	message_to_screen("Press C to continue or Q to quit.", green, 25)
	message_to_screen("L: Line   D: Dimension   S: Supports   F: Force", black, 100)

	pygame.display.update()

	while info:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					info = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

def draw_line():

	#new change here

	draw = True

	z = False
	flag = False

	pos1 = (0,0)
	pos2 = (0,0)

	poslist = []

	while draw:
		clock.tick(10)

		gameDisplay.fill(white)

		curpos = pygame.mouse.get_pos() #Returns tuple of mouse position (xlocation, y location)
		click = pygame.mouse.get_pressed() #Returns tuple of (0,0,0) = (left click, center click, right click)
	
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				z = True
			if event.type == pygame.MOUSEBUTTONUP:
				z = False

		if z == True and flag == False:
			pos1 = pygame.mouse.get_pos()
			flag = True

		elif z == True and flag == True:
			pos2 = pygame.mouse.get_pos()
			pygame.draw.line(gameDisplay, blue, (pos1), (pos2), 5)

		elif z == False and flag == True:
			pos1 = (0,0)
			flag = False



		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					print("EXIT")
					mainLoop()

		pygame.display.update()

def mainLoop(): #BEGIN MAIN LOOP CODE HERE

	z = False

	while True:
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_i:
					control_info()
				elif event.key == pygame.K_l:
					draw_line(startX, startY)
					#print(startX, startY)
				elif event.key == pygame.K_d:
					draw_line()
					#pygame.draw.line(gameDisplay, blue, (200,300), (500,500), 5) #draw line (screenlocation, color, start, end, width)
				elif event.key == pygame.K_s:
					pass
				elif event.key == pygame.K_f:
					pass


		gameDisplay.fill(white)
		pygame.display.update()



mainLoop() #PROGRAM COMES HERE FIRST AND CALLS MAIN LOOP FUNCTION

