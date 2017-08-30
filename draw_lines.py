import pygame

import matplotlib.lines as mlines

from pygame.locals import *

import numpy as np


red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
white = [255, 255, 255]
black = [0, 0, 0]

SCREENSIZE = [800, 800]  # Size of our output display

lines = []

lengths = []

running = True

class Draw_Lines:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE)
        self.screen.fill(white)
        pygame.display.set_caption("Draw Lines and Shit")

        self.myfont = pygame.font.SysFont("arial", 25)

        self.P1 = [0,0]

        self.P2 = [0,0]

        self.flag = False


    def Run(self):

        while(running):
             
            self.screen.fill(white)

            if (pygame.mouse.get_pressed()[0]) and (self.flag == False):

                self.P1[:] = pygame.mouse.get_pos()

                self.flag = True

            elif (pygame.mouse.get_pressed()[0]) and (self.flag == True):

                self.P2[:] = pygame.mouse.get_pos()

                pygame.draw.line(self.screen, red, self.P1[:],  self.P2[:], 5)

                leng = np.linalg.norm(np.array(self.P1[:]) - np.array(self.P2[:]))

                temp_length = self.myfont.render(str("%.1f" % leng), 1, red)

                self.screen.blit(temp_length, self.P1[:])


            elif (pygame.mouse.get_pressed()[0] == False) and (self.flag == True):

                self.P2[:] = pygame.mouse.get_pos() 

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

    p1 = 0
    p2 = 0
    color = [0,0,0]

    def __init__(self,p1,p2,color):

        self.p1 = p1
        self.p2 = p2
        self.color = color

    def draw(self,screen):
        pygame.draw.line(screen, self.color, self.p1,  self.p2, 3)


class Lengths:

    def __init__(self,length,location):

        self.length = length
        self.location = location
        self.myfont = pygame.font.SysFont("arial", 25)

    def draw(self,screen):

        final_length = self.myfont.render(str("%.1f" % self.length), 1, black)

        screen.blit(final_length, self.location)



if __name__ == '__main__':
    
    try:
        sim = Draw_Lines()
        sim.Run()
        
    except KeyboardInterrupt:
        print (" SHUTTING DOWN APP...")
        pygame.quit()
