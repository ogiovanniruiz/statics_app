import pygame

import matplotlib.lines as mlines

from pygame.locals import *

import numpy as np


red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
white = [255, 255, 255]
black = [0, 0, 0]

SCREENSIZE = [1000, 600]  # Size of our output display [width, height]

clock = pygame.time.Clock()

lines = [] # A list containing lines

lengths = [] # List containing length of lines and label locations

running = True

class Draw_Lines:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.screen.fill(white)
        pygame.display.set_caption("Draw Lines and Shit")

        self.myfont = pygame.font.SysFont("arial", 25)

        self.P1 = [0,0] # Place to store starting point of a line

        self.P2 = [0,0] # Place to store ending point of a line

        self.flag = False #Flag used to check mouse condition while dragging lines


    def Run(self):

        while(running):
             
            self.screen.fill(white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_l:
                        print("EXIT")

            if (pygame.mouse.get_pressed()[0]) and (self.flag == False):

                self.P1[:] = pygame.mouse.get_pos()

                self.flag = True

            elif (pygame.mouse.get_pressed()[0]) and (self.flag == True):

                self.P2[:] = pygame.mouse.get_pos()

                if (-10 < (self.P2[0] - self.P1[0]) < 10) :

                    self.P2[0] = self.P1[0]

                if (-10 < (self.P2[1] - self.P1[1]) < 10) :

                    self.P2[1] = self.P1[1]

                line_create(self.screen, blue, self.P1[:],  self.P2[:])
                
                leng = np.linalg.norm(np.array(self.P1[:]) - np.array(self.P2[:]))

                temp_length = self.myfont.render(str("%.1f" % leng), 1, blue)

                self.screen.blit(temp_length, self.P1[:])


            elif (pygame.mouse.get_pressed()[0] == False) and (self.flag == True):

                self.P2[:] = pygame.mouse.get_pos() 

                if (-10 < (self.P2[0] - self.P1[0]) < 10) :

                    self.P2[0] = self.P1[0]

                if (-10 < (self.P2[1] - self.P1[1]) < 10) :

                    self.P2[1] = self.P1[1]

                lines.append(Lines(self.P1[:], self.P2[:], black))

                leng = np.linalg.norm(np.array(self.P1[:]) - np.array(self.P2[:]))

                lengths.append(Lengths(leng, self.P1[:]))

                self.flag = False

            for k in lines:
                k.draw(self.screen)

            for k in lengths:
                k.draw(self.screen)


            pygame.display.update()
    
            pygame.event.clear()

class Lines:

    #p1 = 0
    #p2 = 0
    #color = [0,0,0]

    def __init__(self,p1,p2,color):

        self.p1 = p1
        self.p2 = p2
        self.color = color

    def draw(self,screen):
        line_create(screen, self.color, self.p1, self.p2)
        
class Lengths:

    def __init__(self,length,location):

        self.length = length
        self.location = location
        self.myfont = pygame.font.SysFont("arial", 25)

    def draw(self,screen):

        final_length = self.myfont.render(str("%.1f" % self.length), 1, black)

        screen.blit(final_length, self.location)

def line_create(location, color, pos1, pos2, linethickness=3, diameter=5, circle_thickness=0):
    pygame.draw.line(location, color, pos1,  pos2, linethickness)
    pygame.draw.circle(location, color, [pos1[0], pos1[1]], diameter, circle_thickness)
    pygame.draw.circle(location, color, [pos2[0], pos2[1]], diameter, circle_thickness)


if __name__ == '__main__':
    
    try:
        sim = Draw_Lines()
        sim.Run()
        
    except KeyboardInterrupt:
        print (" SHUTTING DOWN APP...")
        pygame.quit()
