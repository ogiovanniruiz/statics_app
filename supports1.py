#Draw Supports


import pygame, random

pygame.init()

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


#screen 
WIDTH = 1000
HEIGHT = 600

SCREENSIZE = (WIDTH, HEIGHT) #(width, height)

display = pygame.display.set_mode(SCREENSIZE)

pygame.display.set_caption("Supports")

#clock initialization
clock = pygame.time.Clock()

#Booleans, Variables, Lists, Etc.
programRun = True

fixed_supports = []
pinned_supports = []
roller_supports = []

support_type = "none"

z = 0

class Support():
	def __init__(self, y, x, color, support, width=0, height=0):
		
		self.y = y
		self.x = x
		self.width = width
		self.height = height
		self.color = color
		self.support = support

	def draw(self):

		if self.support == "fixed":
			pygame.draw.rect(display, self.color, [self.x, self.y, self.width, self.height])
		if self.support == "pinned":
			pygame.draw.polygon(display, self.color, 
								((self.x,self.y),(self.x-15,self.y+20), 
								(self.x+15,self.y+20)))
		if self.support == "roller":
			pygame.draw.polygon(display, self.color, 
								((self.x,self.y),(self.x-15,self.y+20), 
								(self.x+15,self.y+20)))
			#pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)
			pygame.draw.circle(display, self.color, (self.x, self.y+25), 5)
			pygame.draw.circle(display, self.color, (self.x+10, self.y+25), 5)
			pygame.draw.circle(display, self.color, (self.x-10, self.y+25), 5)

while programRun:

	display.fill(WHITE)

	x,y = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT: #check if close button has been pressed
			pygame.quit() #quits pygame
			quit() #quits
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_f:
				print("fixed selected")
				support_type = "fixed"
			if event.key == pygame.K_p:
				print("pinned selected")
				support_type = "pinned"
			if event.key == pygame.K_r:
				print("roller selected")
				support_type = "roller"

		elif event.type == pygame.MOUSEBUTTONDOWN:
			z = 1
		elif event.type == pygame.MOUSEBUTTONUP:
			z = 0

	if support_type == "fixed":
		pygame.draw.rect(display, RED, [x, y, 30, 15])
	if z == 1 and support_type == "fixed":
		fixed_supports.append(Support(y, x, RED, support_type, 30, 15))
		z = 4

	if support_type == "pinned":
		pygame.draw.polygon(display, BLUE, ((x,y),(x-15,y+20), (x+15,y+20)))
	if z == 1 and support_type == "pinned":
		pinned_supports.append(Support(y, x, BLUE, support_type))
		z = 4

	if support_type == "roller":
		pygame.draw.polygon(display, BLACK, ((x,y),(x-15,y+20), (x+15,y+20)))
		pygame.draw.circle(display, BLACK, (x, y+25), 5)
		pygame.draw.circle(display, BLACK, (x+10, y+25), 5)
		pygame.draw.circle(display, BLACK, (x-10, y+25), 5)
	if z == 1 and support_type == "roller":
		roller_supports.append(Support(y, x, BLACK, support_type))
		z = 4

	elif z > 1:
		z -= 1

	for i in fixed_supports:
		i.draw()

	for i in pinned_supports:
		i.draw()

	for i in roller_supports:
		i.draw()

	#clock.tick(60)

	pygame.display.update()