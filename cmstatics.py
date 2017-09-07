#Casey's Trial for Statics Program and OOP

import pygame

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

pygame.display.set_caption("STACTICS")

#clock initialization
clock = pygame.time.Clock()

#Booleans, Variables, Lists, Etc.

programRun = True

beam_list = []

#main loop code
class Main_Program: #main program class 
	def __init__(self): #initializes variables in main program class

		self.DISPLAY = pygame.display.set_mode(SCREENSIZE) #sets window size and stores it in self.DISPLAY 
		self.DISPLAY.fill(WHITE) #fills display with white
		self.myfont = pygame.font.SysFont("arial", 25) # initializes font
		self.click = pygame.mouse.get_pressed()

		self.flag = True #variable that is used as a flag in tandem with mouse clicks

	def Run(self): #the run method within the main program class

		while programRun: #while loop runs while programRun varibable is True

			self.DISPLAY.fill(WHITE) #fills display white at top of while loop
			self.leftClick = pygame.mouse.get_pressed() # checks for a mouse click and stores a tuple of (0,0,0) = (left, mid, right) in self.leftClick

			for event in pygame.event.get(): #event handling for loop checks for events that occur
				if event.type == pygame.QUIT: #check if close button has been pressed
					pygame.quit() #quits pygame
					quit() #quits
				if event.type == pygame.KEYDOWN: #checks if a keydown event has occured
					if event.key == pygame.K_b: #checks if a "b" keydown event has occured
						print("beam")
						drawBeam(self.DISPLAY) #calls the drawBeam function, passes through self.DISPLAY
					if event.key == pygame.K_d: #checks if a "d" keydown event has occured
						print("dimension")

			for beam in beam_list:
				beam.create(self.DISPLAY)

			for beam in beam_list:
				var = beam.check(self.DISPLAY)


			pygame.display.update() #updates the graphics on the display

class Beams():

	def __init__(self,p1,p2):

		self.p1 = p1
		self.p2 = p2
		self.mouse = (0,0)

	def create(self,screen):

		pygame.draw.line(screen, BLACK, (self.p1), (self.p2), 5)

	def check(self, screen):

		self.mouse = pygame.mouse.get_pos()

		if self.p1[0] + 10 >= self.mouse[0] >= self.p1[0] - 10:
			pygame.draw.line(screen, RED, (self.p1), (self.p2), 5)

def drawBeam(screen): #draw beam function, takes the self.DISPLAY and passes it through screen into the function

	draw = True 
	flag = False
	pos1 = (0,0)
	pos2 = (0,0)

	while draw: #runs while loop while draw is True

		screen.fill(WHITE) #fills the display white

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
			
			pos1 = pygame.mouse.get_pos()

			flag = True

		elif Click[0] == True and flag == True:

			pos2 = pygame.mouse.get_pos()

			pygame.draw.line(screen, BLUE, (pos1), (pos2), 5)

		elif Click[0] == False and flag == True:

			flag = False

			beam_list.append(Beams(pos1, pos2))

		for beam in beam_list:
			beam.create(screen)

		clock.tick(60) #sets the frame rate to 60 FPS

		pygame.display.update() #updates graphics to screen
			
#initializes main program class
if __name__ == '__main__': 
    
    try:
        # sim = Main_Program() 
        # sim.Run() #calls the Run method in Main_Program class
        Main_Program().Run()

    except KeyboardInterrupt: #allows for a control c event to occur in the terminal
        print (" SHUTTING DOWN APP...")
        pygame.quit() 